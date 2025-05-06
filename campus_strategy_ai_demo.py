# Caltech Facilities Strategy Simulator – Executive Demo Edition

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Caltech Planning AI – Demo", layout="wide")
st.title("🤖 Ask a Strategic Facilities Question")

st.markdown("""
Welcome to the future of campus planning. Use natural language to explore how investment, demolition, and growth strategies affect Caltech’s deferred maintenance trajectory.

**Try asking:**
- "What if we double our investment and demolish 1 building for every 2 we build?"
- "How much would we avoid if we increase the budget by $5 million per year?"
- "Can we reduce deferred maintenance by $300 million over 20 years?"

Soon, you'll be able to ask: _"What if we demo Watson Hall?"_
"""
)

# --- Semantic Parser ---
def parse_question(question):
    question = question.lower()
    investment = 8.65  # default
    demo_rate = 0.0
    growth_rate = 0.75

    match = re.search(r"increase.*(?:\$)?(\d+(?:\.\d+)?) ?m", question)
    if match:
        investment += float(match.group(1))
    elif "double" in question:
        investment *= 2

    if "1 demo.*2 build" in question or "one.*two" in question:
        demo_rate = 0.5
    elif "2 demo.*1 build" in question or "two.*one" in question:
        demo_rate = 2.0

    match = re.search(r"fci.*(?:under|below) (0\.\d+)", question)
    target_fci = float(match.group(1)) if match else None

    return investment, demo_rate, growth_rate, target_fci

# --- User Input ---
question = st.text_input("Ask your question:", "What if we double our investment and demolish 1 building for every 2 built?")

if question:
    investment, demo_rate, growth_rate, target_fci = parse_question(question)

    years = np.arange(2023, 2043)
    initial_dm = 429e6
    dm_growth_rate = 0.06
    dm_bau = [initial_dm]
    dm_with_strategy = [initial_dm]

    for _ in range(1, len(years)):
        prev_bau = dm_bau[-1] * (1 + dm_growth_rate)
        avoided_cost = demo_rate * 2e6
        prev_strategy = dm_with_strategy[-1] * (1 + dm_growth_rate) - (investment * 1e6 + avoided_cost)
        dm_bau.append(prev_bau)
        dm_with_strategy.append(max(prev_strategy, 0))

    # --- Output ---
    st.subheader("📊 Projected Deferred Maintenance")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(years, np.array(dm_bau)/1e6, '--', label='BAU (No Action)')
    ax.plot(years, np.array(dm_with_strategy)/1e6, label=f'Strategy (${investment:.2f}M/year + demo)')
    ax.set_ylabel("Deferred Maintenance ($M)")
    ax.set_xlabel("Year")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    final_dm = dm_with_strategy[-1]/1e6
    delta = dm_bau[-1]/1e6 - final_dm
    st.markdown("### ✅ Strategic Summary")
    st.markdown(f"- By 2042, DM would be **${final_dm:,.0f}M** under your strategy.")
    st.markdown(f"- This avoids approximately **${delta:,.0f}M** compared to doing nothing.")
    if demo_rate > 0:
        st.markdown(f"- Demo strategy assumes **${demo_rate * 2:.1f}M/year** in cost avoidance.")
    if target_fci:
        st.markdown(f"- ⚠️ *Target FCI of {target_fci} not yet directly modeled.*")

    st.caption("Demo powered by ChatGPT ✨ Live semantic interface for campus planning.")
