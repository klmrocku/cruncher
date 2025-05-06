# This is the foundation for an AI-powered scenario simulator for facilities planning
# It uses user-adjustable levers like budget, growth, and demolition strategy to model deferred maintenance

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Caltech Facilities Planning AI Demo", layout="wide")

st.title("🔧 Caltech Facilities Strategy Simulator")
st.markdown("Use the sliders below to explore the impact of investment strategies on Deferred Maintenance (DM) over 20 years.")

# User inputs
annual_investment = st.slider("Annual Infrastructure Investment ($M)", min_value=0.0, max_value=50.0, value=8.65, step=0.25)
demo_rate = st.slider("Demo-to-New Build Ratio (e.g., 2:1 means demo 2 for every new)", min_value=0.0, max_value=2.0, value=0.0, step=0.1)
growth_rate = st.slider("Annual Campus GSF Growth (%)", min_value=0.0, max_value=2.0, value=0.75, step=0.05)

dm_growth_rate = 0.06  # Base growth of DM without action
initial_dm = 429e6  # $429M backlog

# Timeline
years = np.arange(2023, 2043)
dm_bau = [initial_dm]
dm_with_strategy = [initial_dm]

# Simulation loop
for _ in range(1, len(years)):
    prev_bau = dm_bau[-1] * (1 + dm_growth_rate)
    avoided_cost = demo_rate * 2e6  # assume $2M saved per building demo'd
    prev_strategy = dm_with_strategy[-1] * (1 + dm_growth_rate) - (annual_investment * 1e6 + avoided_cost)
    dm_bau.append(prev_bau)
    dm_with_strategy.append(max(prev_strategy, 0))

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years, np.array(dm_bau) / 1e6, '--', label='BAU (No Additional Investment)')
ax.plot(years, np.array(dm_with_strategy) / 1e6, label=f'With Strategy (${annual_investment}M/year + demo effect)')
ax.set_title("Projected Deferred Maintenance (2023–2042)")
ax.set_ylabel("Deferred Maintenance ($M)")
ax.set_xlabel("Year")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Summary
final_dm = dm_with_strategy[-1] / 1e6
delta = dm_bau[-1] / 1e6 - final_dm
st.markdown(f"### ✅ Result Summary")
st.markdown(f"- **Final Deferred Maintenance**: ${final_dm:,.0f}M")
st.markdown(f"- **Avoided DM Compared to BAU**: ${delta:,.0f}M")

if demo_rate > 0:
    st.markdown(f"- **Annual Demo Savings Assumed**: ${demo_rate * 2:.1f}M")

st.markdown("---")
st.caption("Prototype created with ChatGPT – powered by your data and strategy.")
