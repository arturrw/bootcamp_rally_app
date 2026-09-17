# Screenshots

This folder holds the images referenced from the main [README.md](../../README.md).

`dashboard.png` and `race-result.png` were captured by running the app locally against
**sample/mock data**, not the real Snowflake database — that avoided using the credentials that
were rotated after the leak described in
[ARCHITECTURE.md § Secrets](../ARCHITECTURE.md#secrets--configuration). If you'd rather show your
actual data, configure `.streamlit/secrets.toml`, run the app, and re-capture:

| File | What to capture | Status |
|---|---|---|
| `dashboard.png` | Title, **Teams** table, **Cars** table, and the top of the "Add Team"/"Add Car" forms | ✅ captured |
| `race-result.png` | The result of clicking **Start Race!** — winner banner and results table | ✅ captured |
| `add-team.png` | The "Add Team" form expanded | optional, not yet captured |
| `add-car.png` | The "Add Car" form expanded | optional, not yet captured |

Save images at a reasonable width (~1200px) and reference them from `README.md` with e.g.
`![Dashboard](docs/screenshots/dashboard.png)`.
