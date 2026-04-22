import streamlit as st


def load_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at top, #07152d 0%, #020814 55%, #01040c 100%);
            color: #d9ecff;
        }

        .title {
            text-align: center;
            font-size: 3rem;
            letter-spacing: 0.25rem;
            color: #53e6ff;
            margin-bottom: 0.2rem;
            font-weight: 700;
            text-shadow: 0 0 12px rgba(83, 230, 255, 0.25);
        }

        .subtitle {
            text-align: center;
            color: #8095b3;
            letter-spacing: 0.2rem;
            margin-bottom: 1.8rem;
            text-transform: uppercase;
        }

        .section-gap {
            height: 1rem;
        }

        .panel {
            background: rgba(8, 18, 40, 0.92);
            border: 1px solid rgba(83, 230, 255, 0.22);
            border-radius: 22px;
            padding: 1.2rem 1.2rem 1rem 1.2rem;
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.08);
        }

        .panel-title {
            color: #7e93b8;
            font-size: 0.9rem;
            letter-spacing: 0.2rem;
            margin-top: 0.8rem;
            margin-bottom: 0.8rem;
        }

        .hero-card {
            background: rgba(8, 18, 40, 0.94);
            border: 1px solid rgba(83, 230, 255, 0.25);
            border-radius: 24px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 1rem;
            box-shadow: 0 0 22px rgba(0, 210, 255, 0.08);
        }

        .hero-label {
            color: #7087ab;
            font-size: 0.95rem;
            letter-spacing: 0.25rem;
            margin-bottom: 0.4rem;
        }

        .hero-value {
            color: #39ddff;
            font-size: 4rem;
            font-weight: 800;
            line-height: 1;
            text-shadow: 0 0 15px rgba(57, 221, 255, 0.22);
        }

        .hero-badge {
            float: right;
            margin-top: -0.5rem;
            color: #7bffb0;
            border: 1px solid rgba(123, 255, 176, 0.35);
            border-radius: 12px;
            padding: 0.25rem 0.8rem;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .metric-card {
            background: rgba(13, 22, 48, 0.95);
            border: 1px solid rgba(120, 145, 190, 0.18);
            border-radius: 18px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            min-height: 110px;
        }

        .metric-title {
            color: #7a8dae;
            letter-spacing: 0.18rem;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
        }

        .accent-cyan { color: #42e8ff; }
        .accent-orange { color: #ff925c; }
        .accent-purple { color: #bb8cff; }
        .accent-green { color: #66f0b5; }
        .accent-yellow { color: #f3c550; }

        .chart-block {
            background: rgba(8, 18, 40, 0.94);
            border: 1px solid rgba(83, 230, 255, 0.18);
            border-radius: 22px;
            padding: 0.8rem;
            margin-top: 1rem;
        }

        div.stButton > button {
            background: rgba(9, 17, 38, 0.95);
            color: #97a9c7;
            border: 1px solid rgba(95, 119, 163, 0.3);
            border-radius: 14px;
            padding: 0.65rem 0.8rem;
        }

        div.stButton > button:hover {
            border: 1px solid rgba(83, 230, 255, 0.45);
            color: #53e6ff;
            box-shadow: 0 0 10px rgba(83, 230, 255, 0.12);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )