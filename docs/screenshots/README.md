# Screenshots

This folder holds the images referenced from the main [README.md](../../README.md).

No screenshots are committed yet — the app talks to a real Snowflake database, and the
credentials that used to be in this repo's history are being rotated (see
[ARCHITECTURE.md § Secrets](../ARCHITECTURE.md#secrets--configuration)). Once you have your own
`.streamlit/secrets.toml` configured, run the app locally and capture:

| File | What to capture |
|---|---|
| `dashboard.png` | The top of the page: title, **Teams** table, **Cars** table |
| `add-team.png` | The "Add Team" form expanded |
| `add-car.png` | The "Add Car" form expanded |
| `race-result.png` | The result of clicking **Start Race!**, showing the winner banner and results table |

Save images at a reasonable width (~1200px) and reference them from `README.md` with e.g.
`![Dashboard](docs/screenshots/dashboard.png)`.
