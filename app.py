import streamlit as st
import pandas as pd
import random

# Risk indicator function


def get_risk_icon(score):
    if score >= 80:
        return "🔴 High"
    elif score >= 50:
        return "🟡 Medium"
    else:
        return "🟢 Low"


# Generate fake policy dataset (25 rows) with noise for realism
base_data = [
    (92, 0.25, 3, 580.25, 58),
    (88, 0.30, 6, 530.10, 62),
    (84, 0.38, 5, 495.00, 67),
    (81, 0.40, 8, 455.75, 64),
    (79, 0.45, 10, 428.60, 61),
    (76, 0.47, 12, 420.00, 59),
    (72, 0.51, 14, 410.00, 56),
    (69, 0.54, 16, 405.00, 60),
    (65, 0.58, 20, 395.00, 52),
    (61, 0.61, 24, 388.10, 49),
    (58, 0.65, 26, 370.90, 47),
    (55, 0.68, 28, 365.75, 53),
    (52, 0.71, 30, 350.00, 50),
    (49, 0.74, 34, 340.00, 46),
    (45, 0.77, 38, 330.00, 45),
    (41, 0.80, 42, 320.00, 48),
    (37, 0.83, 46, 310.00, 42),
    (33, 0.86, 50, 305.50, 40),
    (29, 0.88, 55, 290.25, 43),
    (26, 0.91, 60, 280.00, 41),
    (22, 0.93, 66, 275.00, 39),
    (18, 0.95, 70, 260.00, 36),
    (15, 0.96, 75, 250.00, 35),
    (12, 0.98, 80, 240.00, 34),
    (8,  0.99, 85, 230.00, 32),
]

data = []
for i, (score, otp, age, prem, ca) in enumerate(base_data):
    # Add noise +/- 5% to premium
    prem_noisy = prem * random.uniform(0.95, 1.05)
    # Add small noise to risk score +/- 3 points, bounded 0-100
    score_noisy = max(0, min(100, score + random.randint(-3, 3)))
    # Slight variation in On-Time Payment Ratio +/- 0.1, bounded 0-1
    otp_noisy = max(0, min(1, otp + random.uniform(-0.1, 0.1)))
    # Slight variation in Customer Age +/- 5 years, bounded minimum 18
    ca_noisy = max(18, ca + random.randint(-5, 5))

    data.append({
        "Policy ID": f"POL{1000 + i}",
        "Risk Score (%)": round(score_noisy, 1),
        "On-Time Payment Ratio": round(otp_noisy, 2),
        "Policy Age (months)": age,
        "Premium ($)": round(prem_noisy, 2),
        "Customer Age": ca_noisy
    })

df = pd.DataFrame(data)

# Add risk category icon column
df["Risk Level"] = df["Risk Score (%)"].apply(get_risk_icon)

# Display table
st.title("📊 At-Risk Insurance Policies Dashboard")
st.caption("Hackathon Demo: Predicting Customer Lapse Risk")

st.dataframe(df.style.format({
    "Risk Score (%)": "{:.0f}%",
    "Premium ($)": "${:,.2f}",
    "On-Time Payment Ratio": "{:.2f}"
}), use_container_width=True)
