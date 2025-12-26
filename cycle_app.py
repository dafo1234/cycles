import streamlit as st
import datetime
import pandas as pd
import plotly.express as px

st.title("📅 Calculateur de cycle menstruel")

# Entrées utilisateur
last_period = st.date_input("Date du premier jour des dernières règles")
cycle_length = st.number_input("Durée moyenne du cycle (jours)", min_value=20, max_value=40, value=28)
period_length = st.number_input("Durée moyenne des règles (jours)", min_value=3, max_value=10, value=5)
months_to_predict = st.slider("Nombre de cycles à prévoir", 1, 6, 3)

# Construire la timeline pour plusieurs cycles
phases = []
for i in range(months_to_predict):
    start_cycle = last_period + datetime.timedelta(days=i * cycle_length)
    next_cycle = start_cycle + datetime.timedelta(days=cycle_length)
    ovulation_day = start_cycle + datetime.timedelta(days=cycle_length - 14)

    phases.append({"Cycle": f"Cycle {i+1}", "Phase": "Menstruation", 
                   "Start": start_cycle, "End": start_cycle + datetime.timedelta(days=period_length)})
    phases.append({"Cycle": f"Cycle {i+1}", "Phase": "Phase folliculaire", 
                   "Start": start_cycle + datetime.timedelta(days=period_length), "End": ovulation_day})
    phases.append({"Cycle": f"Cycle {i+1}", "Phase": "Ovulation", 
                   "Start": ovulation_day, "End": ovulation_day + datetime.timedelta(days=1)})
    phases.append({"Cycle": f"Cycle {i+1}", "Phase": "Phase lutéale", 
                   "Start": ovulation_day + datetime.timedelta(days=1), "End": next_cycle})

df = pd.DataFrame(phases)

# Visualisation avec Plotly
fig = px.timeline(df, x_start="Start", x_end="End", y="Cycle", color="Phase",
                  color_discrete_map={
                      "Menstruation": "red",
                      "Phase folliculaire": "blue",
                      "Ovulation": "green",
                      "Phase lutéale": "orange"
                  })

fig.update_yaxes(autorange="reversed")  # Pour que la timeline soit lisible
st.plotly_chart(fig)
st.success("Application lancée avec succès 🎉")
