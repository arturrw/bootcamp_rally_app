import streamlit as st
import pandas as pd
import random
from db_utils import fetch_df, execute

st.set_page_config(page_title="Bootcamp Rally Racing App", layout="centered")

st.title("Bootcamp Rally Racing App")

# Show teams
st.header("Teams")
teams = fetch_df("SELECT * FROM rally_schema.teams;")
st.dataframe(teams)

# Show cars
st.header("Cars")
cars = fetch_df("""
    SELECT c.car_id, c.car_name, c.max_speed, c.acceleration, c.reliability,
           t.team_name, t.budget
    FROM rally_schema.cars c
    JOIN rally_schema.teams t ON c.team_id = t.team_id;
""")
st.dataframe(cars)

# Add new team
st.subheader("Add Team")
with st.form("add_team"):
    team_name = st.text_input("Team name")
    members = st.text_input("Members ,")
    budget = st.number_input("Budget", min_value=1000, value=10000, step=500)
    submitted = st.form_submit_button("Add Team")
    if submitted:
        execute(
            "INSERT INTO rally_schema.teams (team_name, members, budget) VALUES (%s, %s, %s)",
            (team_name, members, budget),
        )
        st.success(f"Team {team_name} added!")

# Add car
st.subheader("Add Car")
with st.form("add_car"):
    team_id = st.number_input("Team ID", min_value=1, step=1)
    car_name = st.text_input("Car name")
    max_speed = st.number_input("Max Speed km/h", min_value=100, max_value=400, step=10)
    acceleration = st.number_input("Acceleration (0-100 km/h, sec)", min_value=2.0, max_value=15.0, step=0.1)
    reliability = st.slider("Reliability (0–1)", 0.0, 1.0, 0.9)
    fuel = st.number_input("Fuel consumption (l/100km)", min_value=5.0, max_value=30.0, step=0.1)
    submitted_car = st.form_submit_button("Add Car")
    if submitted_car:
        execute(
            """INSERT INTO rally_schema.cars 
               (team_id, car_name, max_speed, acceleration, reliability, fuel_consumption) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (team_id, car_name, max_speed, acceleration, reliability, fuel),
        )
        st.success(f"Car {car_name} added!")

# Race simulation
st.header("Start Race")
if st.button("Start Race!"):
    cars = fetch_df("""
        SELECT c.car_id, c.car_name, c.max_speed, c.acceleration, c.reliability,
               c.team_id, t.team_name, t.budget
        FROM rally_schema.cars c
        JOIN rally_schema.teams t ON c.team_id = t.team_id;
    """)

    results = []
    for _, row in cars.iterrows():
        base_time = 100 / row["MAX_SPEED"]
        penalty = random.uniform(0, (1 - row["RELIABILITY"]))
        total_time = base_time + penalty
        results.append((row["TEAM_ID"], row["TEAM_NAME"], row["CAR_NAME"], total_time))

    # Winner result
    results_df = pd.DataFrame(results, columns=["team_id", "team_name", "car_name", "time"])
    winner = results_df.sort_values("time").iloc[0]

    # Budgets and winner
    for _, row in cars.iterrows():
        execute("UPDATE rally_schema.teams SET budget = budget - 1000 WHERE team_id = %s", (row["TEAM_ID"],))
    execute("UPDATE rally_schema.teams SET budget = budget + 5000 WHERE team_id = %s", (int(winner["team_id"]),))

    st.success(f"Winner: {winner['team_name']} with {winner['car_name']} (time={winner['time']:.2f})")
    st.dataframe(results_df.sort_values("time"))
