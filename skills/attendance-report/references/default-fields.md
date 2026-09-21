# Attendance Report — Default Fields

## Columns

- **Meeting title, ID, and date** — identifies the meeting
- **Participant display name** — as returned by the Webex API
- **Participant email** — included only when authorized
- **Join time** — timestamp when the participant joined, or `not available`
- **Leave time** — timestamp when the participant left, or `not available`
- **Attendance duration** — calculated from join and leave times, or `not available`
- **Data availability note** — indicates which fields were unavailable or restricted

## Formatting notes

- Use `not available` rather than inference for missing fields.
- Attendance duration is not proof of attention, contribution, or comprehension.
- Use markdown tables when posting to a Webex space.
- Restrict the recipient list and request approval before sharing.
