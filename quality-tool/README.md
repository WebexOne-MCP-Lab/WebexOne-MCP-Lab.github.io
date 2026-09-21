# Meeting Qualities Tool

The custom tool referenced throughout the lab guide as `get_meeting_qualities(meeting_id, from_time?, to_time?)`. It is separate from the Webex Meetings and Messaging MCP servers: it calls the Webex **Get Meeting Qualities** REST API and returns normalized, read-only telemetry as its own narrow MCP server.

Everything lives in one file, [`server.py`](server.py), so it's easy to read end-to-end: a data model, one tool, one response.

## API contract it wraps

```bash
curl -L --request GET \
  --url 'https://analytics.webexapis.com/v1/meeting/qualities?meetingId=<id>' \
  --header 'Authorization: Bearer {TOKEN}' \
  --header 'Accept: application/json'
```

## What the tool returns

The raw API response is verbose (per-participant, per-stream sampling intervals, many of them empty arrays). `get_meeting_qualities` normalizes it to:

```json
{
  "meeting_id": "<id>",
  "participants": [
    {
      "participant_id": "...",
      "display_name": "...",
      "email": "...",
      "join_time": "...",
      "leave_time": "...",
      "network_type": "...",
      "server_region": "...",
      "video_in": [{ "window_start": "...", "window_end": "...", "jitter": [170], "frame_rate": [25.94], "codec": "H.264 BP" }],
      "video_out": [],
      "audio_in": [],
      "audio_out": [],
      "data_gaps": ["video_in.packetLoss not reported", "video_out not reported", "..."]
    }
  ],
  "data_gaps": [],
  "error": null
}
```

Any metric the live API reports as an empty array is surfaced as an explicit `data_gaps` entry instead of being silently dropped, so the agent can separate observations from missing data.

## Setup

```bash
cd quality-tool
uv sync
cp .env.example .env
# edit .env and set WEBEX_DEVELOPER_TOKEN to a lab-managed, least-privilege credential
```

Run the MCP server (stdio transport):

```bash
uv run server.py
```

## Configuration (`.env`)

| Variable | Default | Purpose |
| ---------------- | ---------------- | ---------------- |
| `WEBEX_DEVELOPER_TOKEN` | *(required)* | Server-side credential. Never returned to a caller or logged. |
| `WEBEX_ANALYTICS_API_BASE` | `https://analytics.webexapis.com/v1` | Override only if the lab uses a different environment. |

## Error handling

`get_meeting_qualities` never raises to the MCP client — every failure comes back as the same `MeetingQualityReport` shape with the `error` field set:

| `error` prefix | Meaning |
| ---------------- | ---------------- |
| `WEBEX_DEVELOPER_TOKEN is not configured` | The server has no credential set. |
| `unauthorized` | API returned `401`. |
| `forbidden` | API returned `403` — credential lacks the quality/reporting scope. |
| `not_found` | API returned `404` — no quality data for that meeting ID. |
| `rate_limited` | API returned `429`. |
| `server_error` | API returned `5xx`. |
| `network_error` | The request itself failed (DNS, connection, timeout). |

## Wiring into the lab client

Add this as a second custom MCP server alongside the official Webex Meetings/Messaging servers. Resolve the meeting ID with the Meetings MCP server first, then pass it to this tool — never let the agent guess a meeting ID for a quality lookup.

!!! note
    The endpoint path, required scope, query parameters, and response schema must be reverified against the current Webex API reference before each lab delivery.
