import streamlit as st
import requests
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Card Fraud Detector",
    page_icon="🛡️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e8f0;
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, #1a1a3e 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 80% 100%, #0d2a1a 0%, transparent 60%),
        #0a0a0f;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 1.5rem;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #00ff88 0%, #00ccff 100%);
    color: #0a0a0f;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero h1 {
    font-size: clamp(2rem, 6vw, 3.2rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #a0a0c8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.8rem;
}
.hero p {
    color: #7070a0;
    font-size: 1rem;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}
.card-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #5050a0;
    margin-bottom: 1.2rem;
}

/* ── Result boxes ── */
.result-fraud {
    background: linear-gradient(135deg, rgba(255,50,80,0.15) 0%, rgba(255,100,50,0.08) 100%);
    border: 1px solid rgba(255,50,80,0.4);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    animation: pulse-red 2s ease-in-out infinite;
}
.result-safe {
    background: linear-gradient(135deg, rgba(0,255,136,0.12) 0%, rgba(0,200,100,0.06) 100%);
    border: 1px solid rgba(0,255,136,0.35);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    animation: pulse-green 2s ease-in-out infinite;
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 20px rgba(255,50,80,0.15); }
    50%       { box-shadow: 0 0 40px rgba(255,50,80,0.3); }
}
@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 20px rgba(0,255,136,0.1); }
    50%       { box-shadow: 0 0 40px rgba(0,255,136,0.25); }
}
.result-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.result-label {
    font-size: 1.6rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}
.result-fraud .result-label { color: #ff3250; }
.result-safe  .result-label { color: #00ff88; }
.result-prob {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #7070a0;
}

/* ── Metric row ── */
.metrics-row {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}
.metric-box {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: #00ccff;
}
.metric-label {
    font-size: 0.72rem;
    color: #5050a0;
    margin-top: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── Streamlit overrides ── */
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
    color: #9090c0 !important;
    font-size: 0.82rem !important;
    font-family: 'Space Mono', monospace !important;
}
div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'Space Mono', monospace !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.15) !important;
}
div[data-testid="stTabs"] [data-testid="stTab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
}
.stButton > button {
    background: linear-gradient(135deg, #00ff88 0%, #00ccff 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.05em !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stExpander {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ── API URL ───────────────────────────────────────────────────────────────────
API_URL = "https://credit-card-fraud-detection-k0gz.onrender.com/predict"

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🛡️ Real-time Detection</div>
    <h1>Credit Card<br>Fraud Detector</h1>
    <p>Enter transaction details below to instantly check if it's fraudulent using our XGBoost ML model.</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🔍  Detect Fraud", "📊  Sample Transactions"])

# ════════════════════════════════════════════════════════════════════════
# TAB 1 — Manual Input
# ════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="card"><div class="card-title">Transaction Details</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        time_val   = st.number_input("Time (seconds)", value=406.0, format="%.2f")
        amount_val = st.number_input("Amount ($)", value=149.62, min_value=0.0, format="%.2f")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">PCA Features (V1 – V28)</div>', unsafe_allow_html=True)

    defaults = [-2.31, 1.95, -1.61, 3.99, -0.52, -1.43, -2.54, 1.39,
                -2.77, -2.77,  3.20, -2.90, -0.60, -4.29,  0.39, -1.14,
                -2.83, -0.02,  0.42,  0.13,  0.52, -0.04, -0.47,  0.32,
                 0.04,  0.18,  0.26,  0.14]

    v_vals = []
    cols = st.columns(4)
    for i in range(28):
        with cols[i % 4]:
            v_vals.append(st.number_input(f"V{i+1}", value=defaults[i], format="%.4f", key=f"v{i+1}"))

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⚡  Analyze Transaction"):
        payload = {
            "Time": time_val, "Amount": amount_val,
            **{f"V{i+1}": v_vals[i] for i in range(28)}
        }
        with st.spinner("Analyzing transaction..."):
            try:
                resp = requests.post(API_URL, json=payload, timeout=60)
                data = resp.json()

                is_fraud = data.get("is_fraud", False)
                prob     = data.get("fraud_probability", 0)
                latency  = data.get("latency_ms", 0)

                if is_fraud:
                    st.markdown(f"""
                    <div class="result-fraud">
                        <div class="result-icon">🚨</div>
                        <div class="result-label">FRAUD DETECTED</div>
                        <div class="result-prob">Fraud probability: {prob:.2%}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-safe">
                        <div class="result-icon">✅</div>
                        <div class="result-label">TRANSACTION SAFE</div>
                        <div class="result-prob">Fraud probability: {prob:.2%}</div>
                    </div>""", unsafe_allow_html=True)

                st.markdown(f"""
                <div class="metrics-row">
                    <div class="metric-box">
                        <div class="metric-value">{prob:.2%}</div>
                        <div class="metric-label">Fraud Probability</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{latency:.1f}ms</div>
                        <div class="metric-label">Response Time</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{"🔴 FRAUD" if is_fraud else "🟢 SAFE"}</div>
                        <div class="metric-label">Verdict</div>
                    </div>
                </div>""", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ API Error: {str(e)}")

# ════════════════════════════════════════════════════════════════════════
# TAB 2 — Sample Transactions
# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="card"><div class="card-title">Quick Test Samples</div>', unsafe_allow_html=True)
    st.markdown("Click any sample to instantly test the model.", unsafe_allow_html=False)
    st.markdown("</div>", unsafe_allow_html=True)

    samples = {
        "🚨 Known Fraud Transaction": {
            "Time": 406, "Amount": 149.62,
            "V1": -2.3122, "V2": 1.9520, "V3": -1.6099, "V4": 3.9979,
            "V5": -0.5222, "V6": -1.4265, "V7": -2.5374, "V8": 1.3917,
            "V9": -2.7701, "V10": -2.7723, "V11": 3.2020, "V12": -2.8999,
            "V13": -0.5952, "V14": -4.2893, "V15": 0.3897, "V16": -1.1407,
            "V17": -2.8301, "V18": -0.0168, "V19": 0.4170, "V20": 0.1269,
            "V21": 0.5172, "V22": -0.0350, "V23": -0.4652, "V24": 0.3202,
            "V25": 0.0445, "V26": 0.1778, "V27": 0.2611, "V28": -0.1433
        },
        "✅ Legitimate Transaction": {
            "Time": 52000, "Amount": 25.00,
            "V1": 1.19, "V2": 0.26, "V3": 0.16, "V4": 0.45,
            "V5": -0.08, "V6": -0.08, "V7": 0.09, "V8": -0.26,
            "V9": -0.16, "V10": -0.15, "V11": -0.19, "V12": 0.05,
            "V13": -0.03, "V14": 0.05, "V15": 0.12, "V16": -0.07,
            "V17": -0.05, "V18": 0.11, "V19": -0.07, "V20": 0.02,
            "V21": 0.01, "V22": 0.04, "V23": -0.01, "V24": 0.02,
            "V25": -0.01, "V26": 0.03, "V27": 0.01, "V28": 0.00
        }
    }

    for label, payload in samples.items():
        with st.expander(label):
            st.json(payload)
            if st.button(f"Test This Transaction", key=label):
                with st.spinner("Analyzing..."):
                    try:
                        resp = requests.post(API_URL, json=payload, timeout=60)
                        data = resp.json()
                        is_fraud = data.get("is_fraud", False)
                        prob     = data.get("fraud_probability", 0)
                        latency  = data.get("latency_ms", 0)

                        if is_fraud:
                            st.markdown(f"""
                            <div class="result-fraud">
                                <div class="result-icon">🚨</div>
                                <div class="result-label">FRAUD DETECTED</div>
                                <div class="result-prob">Probability: {prob:.2%} | Latency: {latency:.1f}ms</div>
                            </div>""", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="result-safe">
                                <div class="result-icon">✅</div>
                                <div class="result-label">TRANSACTION SAFE</div>
                                <div class="result-prob">Probability: {prob:.2%} | Latency: {latency:.1f}ms</div>
                            </div>""", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"⚠️ API Error: {str(e)}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem; color: #3a3a6a; font-size: 0.75rem; font-family: 'Space Mono', monospace;">
    Powered by XGBoost + FastAPI + Streamlit &nbsp;·&nbsp; Deployed on Render
</div>
""", unsafe_allow_html=True)
