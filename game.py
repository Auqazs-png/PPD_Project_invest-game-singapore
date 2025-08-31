# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 02:47:36 2025

@author: seowr
"""
import streamlit as st
import random
import pandas as pd

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Invest Game - Singapore Economics", layout="centered")
st.title("💰 Spend, Save, Invest - Singapore Economics (2010–2020)")

# -------------------------------
# Initialize session state
# -------------------------------
if "money" not in st.session_state:
    st.session_state.money = 1000
if "round" not in st.session_state:
    st.session_state.round = 1
if "history" not in st.session_state:
    st.session_state.history = []
if "money_history" not in st.session_state:
    st.session_state.money_history = [st.session_state.money]
if "rounds_data" not in st.session_state:
    st.session_state.rounds_data = []

# -------------------------------
# Real Singapore data 2010-2020
# -------------------------------
singapore_data = [
    {"Year": 2010, "GDP": 14.81, "Inflation": 2.8},
    {"Year": 2011, "GDP": 5.2, "Inflation": 5.2},
    {"Year": 2012, "GDP": 1.3, "Inflation": 4.6},
    {"Year": 2013, "GDP": 2.1, "Inflation": 2.4},
    {"Year": 2014, "GDP": 2.9, "Inflation": 1.0},
    {"Year": 2015, "GDP": -0.5, "Inflation": -0.5},
    {"Year": 2016, "GDP": 2.0, "Inflation": -0.5},
    {"Year": 2017, "GDP": 3.6, "Inflation": 0.6},
    {"Year": 2018, "GDP": 3.1, "Inflation": 0.4},
    {"Year": 2019, "GDP": 0.7, "Inflation": 0.6},
    {"Year": 2020, "GDP": -3.8, "Inflation": -0.2},
]

# -------------------------------
# Function to determine economic situation and tip
# -------------------------------
def get_situation_and_tip(gdp, inflation):
    if gdp > 2 and inflation < 3:
        return "Healthy Economy", "Good time to invest or save for the future."
    elif (1 < gdp <= 2) or (3 <= inflation <= 5):
        return "Moderate Growth", "Consider balancing spending with saving."
    elif gdp <= 1 or inflation > 5:
        return "Recession / Stagflation", "Be cautious with spending; focus on saving and budgeting."
    else:
        return "Normal Economy", "A stable period; make wise financial choices."

# -------------------------------
# Pre-generate 10 rounds with unique years
# -------------------------------
if not st.session_state.rounds_data:
    available_years = singapore_data.copy()
    random.shuffle(available_years)
    for i in range(10):
        year_data = available_years[i % len(available_years)]
        situation, tip = get_situation_and_tip(year_data["GDP"], year_data["Inflation"])
        st.session_state.rounds_data.append({
            "Year": year_data["Year"],
            "GDP": year_data["GDP"],
            "Inflation": year_data["Inflation"],
            "Situation": situation,
            "Tip": tip
        })

# -------------------------------
# Current round
# -------------------------------
if st.session_state.round <= 10:
    scenario = st.session_state.rounds_data[st.session_state.round - 1]

    st.subheader(f"Round {st.session_state.round}")
    st.write(f"Year: {scenario['Year']}")
    st.write(f"GDP Growth: {scenario['GDP']}% | Inflation: {scenario['Inflation']}%")
    st.write(f"Economic Situation: {scenario['Situation']}")

    # Player choice
    choice = st.radio("Choose your action:", ["Spend", "Save", "Invest"])

    if st.button("Submit Choice"):
        money_change = 0
        outcome_text = ""

        if choice == "Spend":
            money_change = -random.randint(50, 150) - scenario['Inflation'] * 5
            outcome_text = f"You spent money. Lost ${-money_change}."
        elif choice == "Save":
            money_change = random.randint(20, 50)
            outcome_text = f"You saved money. Gained ${money_change}."
        elif choice == "Invest":
            if scenario['GDP'] > 2:
                money_change = random.randint(100, 200)
                outcome_text = f"Your investment succeeded! Gained ${money_change}."
            else:
                money_change = -random.randint(50, 150)
                outcome_text = f"Your investment failed. Lost ${-money_change}."

        st.session_state.money += money_change
        st.session_state.money_history.append(st.session_state.money)

        st.session_state.history.append({
            "Round": st.session_state.round,
            "Year": scenario['Year'],
            "Choice": choice,
            "MoneyChange": money_change,
            "GDP": scenario['GDP'],
            "Inflation": scenario['Inflation'],
            "Situation": scenario['Situation'],
            "Tip": scenario['Tip']
        })

        st.write(outcome_text)
        st.info(f"Learning Tip: {scenario['Tip']}")
        st.session_state.round += 1
        st.rerun()

# -------------------------------
# End of game
# -------------------------------
else:
    st.subheader("🏁 Game Over")
    st.write(f"Your final money: ${st.session_state.money}")

    # Summary table
    df = pd.DataFrame(st.session_state.history)
    st.write("### Summary of your choices:")
    st.dataframe(df[['Round','Year','Choice','MoneyChange','GDP','Inflation','Situation','Tip']])

    # Money progression chart
    st.write("### Money Progression Over Rounds")
    chart_data = pd.DataFrame(st.session_state.money_history, columns=["Money"])
    st.line_chart(chart_data)

    # Restart button
    if st.button("Restart Game"):
        st.session_state.money = 1000
        st.session_state.round = 1
        st.session_state.history = []
        st.session_state.money_history = [1000]
        st.session_state.rounds_data = []
        st.rerun()
