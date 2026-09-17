# Contributing

Thanks for helping out with the Bootcamp Rally Racing App. This is a small bootcamp project —
the process below is intentionally lightweight.

## Getting set up

1. Clone the repo and create a virtualenv:
   ```bash
   git clone https://github.com/arturrw/bootcamp_rally_app.git
   cd bootcamp_rally_app
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Configure Snowflake credentials **locally only** — never commit them. Create
   `.streamlit/secrets.toml` (git-ignored):
   ```toml
   [snowflake]
   user = "..."
   password = "..."
   account = "..."
   warehouse = "..."
   database = "..."
   schema = "..."
   ```
   Alternatively, copy `.env.example` (if present) to `.env` and fill in `SNOWFLAKE_*` values —
   `db_utils.py` falls back to env vars when `st.secrets` isn't populated.
3. Run the app:
   ```bash
   streamlit run app.py
   ```
   It opens at `http://localhost:8501`.

## Security

- `secrets.toml` and `.env` are git-ignored — keep it that way. Real credentials belong in
  `.streamlit/secrets.toml` or your local `.env`, never in a tracked file.
- If you ever commit a secret by accident, don't just delete it in a follow-up commit — the
  value stays readable in git history. Rotate the credential immediately and flag it so history
  can be rewritten (see [ARCHITECTURE.md § Secrets](docs/ARCHITECTURE.md#secrets--configuration)
  for the incident this project has already had).
- Don't add `print()`/logging statements that include credentials, tokens, or account
  identifiers.

## Branching & commits

- Branch off `main`: `feature/<short-description>` or `fix/<short-description>`.
- Keep commits focused; write commit messages that explain *why*, not just *what*.
- Open a PR against `main` and describe what changed and how you tested it.

## Code style

- Follow standard PEP 8 formatting (4-space indents, `snake_case` for functions/variables).
- Keep the layering in [ARCHITECTURE.md](docs/ARCHITECTURE.md): UI code stays in `app.py`,
  business/domain logic that doesn't need Streamlit or Snowflake belongs in its own module (like
  `race.py`), and all SQL/connection handling stays in `db_utils.py`.
- Prefer parameterized queries (`execute(query, params)`) over string-formatted SQL to avoid
  injection.

## Testing

There's no test suite yet. When adding one, start with `race.py` — it's pure Python (no
Streamlit, no network), so it can be tested directly:

```python
import pandas as pd
from race import simulate_race, pick_winner

def test_simulate_race_picks_fastest_by_time():
    cars = pd.DataFrame([
        {"TEAM_ID": 1, "TEAM_NAME": "A", "CAR_NAME": "Fast", "MAX_SPEED": 300, "RELIABILITY": 1.0},
        {"TEAM_ID": 2, "TEAM_NAME": "B", "CAR_NAME": "Slow", "MAX_SPEED": 100, "RELIABILITY": 1.0},
    ])
    results = simulate_race(cars)
    winner = pick_winner(results)
    assert winner["car_name"] == "Fast"
```

Anything that touches `db_utils.py` needs a real (or mocked) Snowflake connection and isn't
covered here yet — mocking `snowflake.connector.connect` is the recommended approach rather than
running tests against the live database.

## Reporting issues

Open a GitHub issue with steps to reproduce, what you expected, and what happened instead.
