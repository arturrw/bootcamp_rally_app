# API Reference

This app has no REST/HTTP API — it's a single Streamlit process that talks to Snowflake directly.
"API" here means the two surfaces other code (or tests) actually interacts with: the **internal
Python modules** and the **UI actions**, which map 1:1 to underlying SQL.

## Internal Python API

### `db_utils.py` — data access layer

| Function | Signature | Description |
|---|---|---|
| `get_connection` | `get_connection() -> snowflake.connector.SnowflakeConnection` | Opens a new Snowflake connection using `st.secrets["snowflake"]` if present, else `SNOWFLAKE_*` env vars. |
| `fetch_df` | `fetch_df(query: str) -> pandas.DataFrame` | Runs a `SELECT`, returns the full result as a DataFrame, closes the connection. |
| `execute` | `execute(query: str, params: tuple \| None = None) -> None` | Runs an `INSERT`/`UPDATE` with parameterized values, commits, closes the connection. |

Both `fetch_df` and `execute` open a fresh connection per call and always close it — there's no
pooling or connection reuse across calls.

### `race.py` — domain logic (pure, no I/O)

| Function | Signature | Description |
|---|---|---|
| `simulate_race` | `simulate_race(cars: pandas.DataFrame) -> pandas.DataFrame` | Computes a finish time per car (`100 / max_speed` + random reliability penalty) and returns results sorted fastest-first with columns `team_id, team_name, car_name, time`. Expects `cars` to have `MAX_SPEED`, `RELIABILITY`, `TEAM_ID`, `TEAM_NAME`, `CAR_NAME` columns (Snowflake returns uppercase column names by default). |
| `pick_winner` | `pick_winner(results: pandas.DataFrame) -> pandas.Series` | Returns the first row of an already-sorted results DataFrame. |

Because this module takes a DataFrame and returns a DataFrame with no Snowflake/Streamlit calls,
it can be unit tested with a hand-built DataFrame — see
[CONTRIBUTING.md](../CONTRIBUTING.md#testing).

## UI actions → data effects

| UI action | Triggers | Reads | Writes |
|---|---|---|---|
| Page load | — | `SELECT * FROM rally_schema.teams` and a `cars JOIN teams` query | — |
| **Add Team** form submit | `execute(INSERT INTO rally_schema.teams ...)` | — | Inserts one row into `teams` (`team_name`, `members`, `budget`) |
| **Add Car** form submit | `execute(INSERT INTO rally_schema.cars ...)` | — | Inserts one row into `cars` (`team_id`, `car_name`, `max_speed`, `acceleration`, `reliability`, `fuel_consumption`) |
| **Start Race!** click | `fetch_df` + `simulate_race` + `pick_winner` + `execute` × N | `cars JOIN teams` | `-1000` budget for every entered team, `+5000` budget for the winning team |

## Database schema

See the ER diagram in [ARCHITECTURE.md](ARCHITECTURE.md#data-model). Both tables live in
`BOOTCAMP_RALLY.RALLY_SCHEMA` (configurable via `SNOWFLAKE_DATABASE` / `SNOWFLAKE_SCHEMA`).

**`teams`**

| Column | Type (inferred) | Notes |
|---|---|---|
| `team_id` | int | Primary key |
| `team_name` | string | |
| `members` | string | Comma-separated names, per the UI hint |
| `budget` | int | Starting value set from the "Add Team" form (min 1000) |

**`cars`**

| Column | Type (inferred) | Notes |
|---|---|---|
| `car_id` | int | Primary key |
| `team_id` | int | Foreign key → `teams.team_id` |
| `car_name` | string | |
| `max_speed` | int | km/h, 100–400 |
| `acceleration` | float | 0–100 km/h, seconds, 2.0–15.0 |
| `reliability` | float | 0–1 |
| `fuel_consumption` | float | l/100km, 5.0–30.0 |

## Configuration reference

| Key (`.streamlit/secrets.toml` → `[snowflake]`) | Key (env var) | Required |
|---|---|---|
| `user` | `SNOWFLAKE_USER` | yes |
| `password` | `SNOWFLAKE_PASSWORD` | yes |
| `account` | `SNOWFLAKE_ACCOUNT` | yes |
| `warehouse` | `SNOWFLAKE_WAREHOUSE` | yes |
| `database` | `SNOWFLAKE_DATABASE` | yes |
| `schema` | `SNOWFLAKE_SCHEMA` | yes |

Never commit real values for these — see
[ARCHITECTURE.md § Secrets & configuration](ARCHITECTURE.md#secrets--configuration).
