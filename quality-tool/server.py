"""Webex Meeting Qualities tool — a single MCP tool for meeting media-quality telemetry.

This is separate from the official Webex Meetings and Messaging MCP servers.
Resolve the meeting_id with the Meetings MCP server first, then call the tool
below for quality telemetry. It wraps one REST endpoint:

    GET https://analytics.webexapis.com/v1/meeting/qualities?meetingId=<id>

Run it:
    uv run server.py
"""

import os

import httpx
from fastmcp import FastMCP
from pydantic import BaseModel

WEBEX_API_BASE = os.environ.get(
    "WEBEX_ANALYTICS_API_BASE", "https://analytics.webexapis.com/v1"
)
WEBEX_DEVELOPER_TOKEN = os.environ.get(
    "WEBEX_DEVELOPER_TOKEN"
)  # server-side only, never returned to callers

mcp = FastMCP("webex-meeting-qualities")


class StreamWindow(BaseModel):
    """One sampling interval for a single media direction, e.g. video_in."""

    window_start: str | None = None
    window_end: str | None = None
    codec: str | None = None
    packet_loss: list[float] = []
    latency: list[float] = []
    jitter: list[float] = []
    frame_rate: list[float] = []


class ResourceUsage(BaseModel):
    """One CPU utilization sample set for the participant's device."""

    process_average_cpu: list[float] = []
    process_max_cpu: list[float] = []
    system_average_cpu: list[float] = []
    system_max_cpu: list[float] = []


class ParticipantQuality(BaseModel):
    """Normalized quality telemetry for one meeting participant."""

    participant_id: str | None = None
    display_name: str | None = None
    email: str | None = None
    join_time: str | None = None
    leave_time: str | None = None
    network_type: str | None = None
    server_region: str | None = None
    video_in: list[StreamWindow] = []
    video_out: list[StreamWindow] = []
    audio_in: list[StreamWindow] = []
    audio_out: list[StreamWindow] = []
    share_in: list[StreamWindow] = []
    share_out: list[StreamWindow] = []
    resources: list[ResourceUsage] = []
    data_gaps: list[str] = []


class MeetingQualityReport(BaseModel):
    """The normalized shape returned by the get_meeting_qualities tool."""

    meeting_id: str
    participants: list[ParticipantQuality] = []
    data_gaps: list[str] = []
    error: str | None = None


def _extract_metric(
    interval: dict, api_key: str, stream_name: str, gaps: list[str]
) -> list[float]:
    values = interval.get(api_key) or []
    if not values:
        # the live API commonly reports empty arrays for unsupported metrics
        gaps.append(f"{stream_name}.{api_key} not reported")
        return values
    # the live API uses -1 as a per-sample "not measured" sentinel; undocumented in the schema
    unmeasured = sum(1 for value in values if value == -1)
    if unmeasured == len(values):
        gaps.append(f"{stream_name}.{api_key} all samples unmeasured (-1)")
    elif unmeasured:
        gaps.append(
            f"{stream_name}.{api_key} {unmeasured}/{len(values)} samples unmeasured (-1)"
        )
    return values


def _stream_window(interval: dict, stream_name: str, gaps: list[str]) -> StreamWindow:
    window = StreamWindow(
        window_start=interval.get("startTime"),
        window_end=interval.get("endTime"),
        codec=interval.get("codec"),
    )
    for field, api_key in (
        ("packet_loss", "packetLoss"),
        ("latency", "latency"),
        ("jitter", "jitter"),
        ("frame_rate", "frameRate"),
    ):
        setattr(window, field, _extract_metric(interval, api_key, stream_name, gaps))
    return window


def _resource_usage(entry: dict, gaps: list[str]) -> ResourceUsage:
    usage = ResourceUsage()
    for field, api_key in (
        ("process_average_cpu", "processAverageCPU"),
        ("process_max_cpu", "processMaxCPU"),
        ("system_average_cpu", "systemAverageCPU"),
        ("system_max_cpu", "systemMaxCPU"),
    ):
        setattr(usage, field, _extract_metric(entry, api_key, "resources", gaps))
    return usage


def _participant_quality(raw: dict) -> ParticipantQuality:
    gaps: list[str] = []
    streams: dict[str, list[StreamWindow]] = {}
    for api_key, field in (
        ("videoIn", "video_in"),
        ("videoOut", "video_out"),
        ("audioIn", "audio_in"),
        ("audioOut", "audio_out"),
        ("shareIn", "share_in"),
        ("shareOut", "share_out"),
    ):
        intervals = raw.get(api_key) or []
        streams[field] = [
            _stream_window(interval, field, gaps) for interval in intervals
        ]
        if not intervals:
            gaps.append(f"{field} not reported")

    resource_entries = raw.get("resources") or []
    resources = [_resource_usage(entry, gaps) for entry in resource_entries]
    if not resource_entries:
        gaps.append("resources not reported")

    return ParticipantQuality(
        participant_id=raw.get("participantId"),
        display_name=raw.get("webexUserName"),
        email=raw.get("webexUserEmail"),
        join_time=raw.get("joinTime"),
        leave_time=raw.get("leaveTime"),
        network_type=raw.get("networkType"),
        server_region=raw.get("serverRegion"),
        resources=resources,
        data_gaps=gaps,
        **streams,
    )


@mcp.tool()
def get_meeting_qualities(
    meeting_id: str, from_time: str | None = None, to_time: str | None = None
) -> MeetingQualityReport:
    """Retrieve normalized, read-only media-quality telemetry for one Webex meeting.

    Resolve meeting_id with the Webex Meetings MCP server first. This tool never
    guesses a meeting ID from a title and never returns the underlying credential.
    """
    if not WEBEX_DEVELOPER_TOKEN:
        return MeetingQualityReport(
            meeting_id=meeting_id, error="WEBEX_DEVELOPER_TOKEN is not configured"
        )

    params = {"meetingId": meeting_id}
    if from_time:
        params["from"] = from_time
    if to_time:
        params["to"] = to_time

    try:
        response = httpx.get(
            f"{WEBEX_API_BASE}/meeting/qualities",
            params=params,
            headers={
                "Authorization": f"Bearer {WEBEX_DEVELOPER_TOKEN}",
                "Accept": "application/json",
            },
            timeout=10,
        )
    except httpx.HTTPError as exc:
        return MeetingQualityReport(
            meeting_id=meeting_id, error=f"network_error: {exc}"
        )

    error_by_status = {
        401: "unauthorized: credential was rejected (401)",
        403: "forbidden: credential lacks the quality scope (403)",
        404: "not_found: no quality data for this meeting (404)",
        429: "rate_limited: try again later (429)",
    }
    if response.status_code in error_by_status:
        return MeetingQualityReport(
            meeting_id=meeting_id, error=error_by_status[response.status_code]
        )
    if response.status_code >= 500:
        return MeetingQualityReport(
            meeting_id=meeting_id,
            error=f"server_error: quality API returned {response.status_code}",
        )
    if response.status_code != 200:
        return MeetingQualityReport(
            meeting_id=meeting_id, error=f"unexpected_status: {response.status_code}"
        )

    items = response.json().get("items") or []
    participants = [_participant_quality(item) for item in items]
    meeting_gaps = (
        [] if items else ["No participant quality records returned for this meeting"]
    )

    return MeetingQualityReport(
        meeting_id=meeting_id, participants=participants, data_gaps=meeting_gaps
    )


if __name__ == "__main__":
    mcp.run()
