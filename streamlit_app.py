import datetime
import os
from typing import Any

import requests
import streamlit as st


DEFAULT_BACKEND_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT_SECONDS = 180
MAX_RECENT_TRIPS = 10
QUICK_ACTIONS = {
    "💰 Make it cheaper": "Make my current itinerary cheaper while keeping the same destination and duration.",
    "🏔️ Add more adventure": "Add more adventure activities to my current itinerary while keeping the same destination and duration.",
    "🍜 Add food experiences": "Add more local food and dining experiences to my current itinerary.",
    "🚗 Reduce travel time": "Optimize my current itinerary to reduce travel time while keeping the key experiences.",
    "🌿 Make it more relaxed": "Make my current itinerary more relaxed with fewer activities and more downtime.",
}

st.set_page_config(
    page_title="Agentic Travel Orchestrator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(ttl=15, show_spinner=False)
def backend_health(backend_url: str) -> bool:
    try:
        return requests.get(f"{backend_url}/health", timeout=3).ok
    except requests.RequestException:
        return False


def load_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap');
        :root { --bg:#0b1120; --surface:#111827; --surface-2:#172033; --border:#263449; --text:#f8fafc; --muted:#94a3b8; --blue:#3b82f6; --blue-dark:#1d4ed8; --green:#22c55e; --amber:#f59e0b; }
        html, body, [class*="css"] { font-family:'DM Sans', sans-serif; color:var(--text); font-size:16px; }
        .stApp {
            background-color:var(--bg);
            background-image:linear-gradient(rgba(11,17,32,.63), rgba(11,17,32,.78)), url("https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2400&q=85");
            background-size:cover;
            background-position:center;
            background-attachment:fixed;
        }
        .main .block-container { max-width:1450px; padding:3rem 4rem 8rem; }
        [data-testid="stSidebar"] { background:#0f172a; border-right:1px solid var(--border); }
        [data-testid="stSidebar"] * { color:var(--text); }
        [data-testid="stSidebar"] .stButton > button { background:#172033; border:1px solid #2b3a51; color:var(--text); text-align:left; }
        [data-testid="stSidebar"] .stButton > button:hover { border-color:var(--blue); background:#1d2b43; }
        h1, h2, h3 { font-family:'Manrope', sans-serif; letter-spacing:-.025em; color:var(--text) !important; }
        h1 { font-size:3.15rem !important; line-height:1.08 !important; }
        h2 { font-size:1.7rem !important; }
        p, label, .stMarkdown { color:var(--text); }
        .brand { display:flex; align-items:center; gap:.8rem; margin:.5rem 0 2.2rem; }
        .brand-logo { display:grid; place-items:center; width:43px; height:43px; border-radius:13px; background:var(--blue); font-size:1.35rem; box-shadow:0 8px 22px rgba(59,130,246,.25); }
        .brand-title { font-family:'Manrope', sans-serif; font-size:1.15rem; font-weight:800; line-height:1.1; }
        .brand-subtitle { color:var(--muted); font-size:.82rem; margin-top:.2rem; line-height:1.4; }
        .eyebrow { color:#60a5fa; font-size:.82rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; margin-bottom:.85rem; }
        .hero-copy { color:var(--muted); max-width:780px; font-size:1.12rem; line-height:1.65; }
        .hero-icon { font-size:4.2rem; margin-bottom:.65rem; }
        .input-panel { background:var(--surface); border:1px solid #38506f; border-radius:16px; padding:1.25rem 1.35rem; margin:1.7rem 0 2rem; }
        .input-label { color:var(--text); font-size:1.05rem; font-weight:700; margin-bottom:.65rem; }
        .status { display:flex; align-items:center; gap:.45rem; color:var(--muted); font-size:.95rem; }
        .status-dot { width:8px; height:8px; display:inline-block; border-radius:50%; background:var(--green); box-shadow:0 0 0 4px rgba(34,197,94,.12); }
        .status-dot.offline { background:#ef4444; box-shadow:0 0 0 4px rgba(239,68,68,.12); }
        .powered-note { color:var(--muted); font-size:.82rem; line-height:1.5; margin-top:2rem; padding-top:1rem; border-top:1px solid var(--border); }
        .section-label { color:var(--muted); font-size:.8rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; margin:2.2rem 0 .9rem; }
        .prompt { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:1rem 1.15rem; color:#cbd5e1; font-size:.98rem; line-height:1.5; margin:.6rem 0; }
        .prompt:hover { border-color:#426a9f; }
        .feature-card { background:var(--surface); border:1px solid var(--border); border-radius:15px; padding:1.25rem; min-height:150px; }
        .feature-icon { font-size:1.7rem; margin-bottom:.55rem; }
        .feature-title { color:var(--text); font-weight:700; }
        .feature-copy { color:var(--muted); font-size:.9rem; line-height:1.5; margin-top:.35rem; }
        .trip-card { background:var(--surface); border:1px solid var(--border); border-radius:11px; padding:.65rem .8rem; margin:.45rem 0; }
        .trip-title { color:var(--text); font-size:.8rem; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
        .trip-time { color:var(--muted); font-size:.7rem; }
        .chat-shell { background:rgba(17,24,39,.55); border:1px solid var(--border); border-radius:18px; padding:1.5rem 1.7rem; margin-top:2rem; }
        [data-testid="stChatMessage"] { background:transparent; border:0; padding:.9rem 0; }
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] { color:var(--text); font-size:1rem; line-height:1.7; }
        [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:.15rem 1rem; }
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] { background:#17345f; border-color:#28599c; }
        [data-testid="stChatInput"] { bottom:1.2rem; }
        [data-testid="stChatInput"] textarea { background:var(--surface); color:var(--text); border:1px solid #38506f; border-radius:14px; }
        [data-testid="stChatInput"] textarea::placeholder { color:#9fb0c4; opacity:1; }
        .result-banner { border:1px solid #275c42; background:rgba(34,197,94,.08); border-radius:13px; padding:.75rem 1rem; color:#bbf7d0; margin:1rem 0; }
        .mini-note { color:var(--muted); font-size:.86rem; line-height:1.5; }
        .stButton > button { border-radius:9px; min-height:3rem; font-size:.95rem; font-weight:600; }
        .stButton > button[kind="primary"] { background:var(--blue); border-color:var(--blue); color:#fff; }
        .stButton > button[kind="primary"]:hover { background:var(--blue-dark); border-color:var(--blue-dark); }
        .stTextInput input { background:var(--surface); color:var(--text); border-color:var(--border); }
        .stTextInput input::placeholder { color:#9fb0c4; opacity:1; }
        [data-testid="stExpander"] { background:var(--surface); border:1px solid var(--border); border-radius:12px; }
        .stAlert { border-radius:12px; }
        @media (max-width:800px) { .main .block-container { padding:1.5rem 1rem 6rem; } h1 { font-size:2.35rem !important; } .hero-copy { font-size:1rem; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "recent_trips" not in st.session_state:
        st.session_state.recent_trips = []
    if "active_trip" not in st.session_state:
        st.session_state.active_trip = None


def format_time(timestamp: str) -> str:
    try:
        return datetime.datetime.fromisoformat(timestamp).strftime("%d %b, %I:%M %p")
    except ValueError:
        return timestamp


def trip_title(question: str) -> str:
    words = question.replace("Plan a ", "").replace("plan a ", "").split()
    title = " ".join(words[:5]).rstrip(".,")
    return title[:32] + ("..." if len(title) > 32 else "")


def clear_current_trip() -> None:
    st.session_state.messages = []
    st.session_state.active_trip = None


def save_trip(question: str, messages: list[dict[str, Any]]) -> None:
    timestamp = datetime.datetime.now().isoformat()
    saved_trip = {"title": trip_title(question), "question": question, "messages": messages.copy(), "timestamp": timestamp}
    st.session_state.recent_trips = [saved_trip] + [trip for trip in st.session_state.recent_trips if trip["question"] != question]
    st.session_state.recent_trips = st.session_state.recent_trips[:MAX_RECENT_TRIPS]
    st.session_state.active_trip = saved_trip


def request_answer(question: str, backend_url: str) -> str | None:
    try:
        response = requests.post(f"{backend_url}/query", json={"question": question}, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.Timeout:
        st.error("The planner took too long to respond. Please try again with a shorter request.")
        return None
    except requests.ConnectionError:
        st.error("The planner is unavailable right now. Please start the app service and try again.")
        return None
    except requests.RequestException:
        st.error("Something went wrong while contacting the planning service. Please try again.")
        return None

    try:
        payload = response.json()
    except ValueError:
        st.error("The planning service returned an invalid response. Please try again.")
        return None
    if not response.ok:
        detail = payload.get("detail", "The planning service could not complete this request.")
        st.error(f"{detail}")
        return None
    answer = payload.get("answer")
    if not answer:
        st.error("The planner returned no itinerary. Please try again with more trip details.")
        return None
    return answer


def run_planner(question: str, backend_url: str) -> None:
    timestamp = datetime.datetime.now().isoformat()
    st.session_state.messages.append({"role": "user", "content": question, "timestamp": timestamp})
    with st.status("Planning your trip...", expanded=True) as status:
        st.write("✓ Understanding request")
        st.write("✓ Researching travel information")
        st.write("✓ Checking budget")
        st.write("✓ Checking weather")
        st.write("✓ Finalizing itinerary")
        answer = request_answer(question, backend_url)
        if answer:
            st.session_state.messages.append({"role": "assistant", "content": answer, "timestamp": datetime.datetime.now().isoformat()})
            save_trip(question, st.session_state.messages)
            status.update(label="Trip plan ready", state="complete", expanded=False)
        else:
            st.session_state.messages.pop()
            status.update(label="Planning could not be completed", state="error", expanded=True)


def render_sidebar(backend_url: str) -> None:
    with st.sidebar:
        st.markdown('<div class="brand"><div class="brand-logo">🌍</div><div><div class="brand-title">Agentic Travel<br>Orchestrator</div><div class="brand-subtitle">LLM-powered constraint-aware travel planning</div></div></div>', unsafe_allow_html=True)
        if st.button("＋  New Trip", type="primary", use_container_width=True):
            clear_current_trip()
            st.rerun()
        if backend_health(backend_url):
            st.markdown('<div class="status"><span class="status-dot"></span>Ready to plan</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status"><span class="status-dot offline"></span>Planner unavailable</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Recent Trips</div>', unsafe_allow_html=True)
        if st.session_state.recent_trips:
            for index, trip in enumerate(st.session_state.recent_trips):
                if st.button(f"🏖️ {trip['title']}\n{format_time(trip['timestamp'])}", key=f"recent_{index}", use_container_width=True):
                    st.session_state.messages = trip["messages"].copy()
                    st.session_state.active_trip = trip
                    st.rerun()
        else:
            st.markdown('<div class="mini-note">Your saved trip plans will appear here.</div>', unsafe_allow_html=True)
        if st.session_state.recent_trips and st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.recent_trips = []
            clear_current_trip()
            st.rerun()
        st.markdown('<div class="powered-note">✨ Your trip plans stay in this session.</div>', unsafe_allow_html=True)


def render_messages() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🌍" if message["role"] == "assistant" else "🧳"):
            st.markdown(message["content"])
            st.caption(format_time(message["timestamp"]))


def render_empty_state() -> None:
    st.markdown('<div class="hero-icon">🌍</div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">AI travel intelligence</div>', unsafe_allow_html=True)
    st.title("Agentic Travel Orchestrator")
    st.markdown("### Plan smarter. Travel better.")
    st.markdown('<div class="hero-copy">Describe your trip naturally and let the AI build a personalized itinerary using travel information, weather context, places and budget-aware planning.</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-panel"><div class="input-label">Where would you like to go?</div></div>', unsafe_allow_html=True)
    with st.form("first_trip_form", clear_on_submit=True):
        first_trip = st.text_area(
            "Trip request",
            placeholder="Type any destination or travel request... e.g. Plan 4 days in Bali for two people with beaches, food, and a budget of ₹80,000.",
            height=110,
            label_visibility="collapsed",
        )
        plan_button = st.form_submit_button("🌍 Plan my trip", type="primary", use_container_width=True)
    if plan_button:
        if first_trip.strip():
            run_planner(first_trip.strip(), backend_url)
            st.rerun()
        st.warning("Type a destination or trip request first.")
    feature_cols = st.columns(4)
    features = [("🗺️", "Smart routes", "Day-by-day plans built around your constraints."), ("🌤️", "Travel context", "Weather and place intelligence where available."), ("💰", "Budget aware", "Clear INR-first estimates before you commit."), ("🧳", "One conversation", "Refine the plan naturally as you go.")]
    for column, (icon, title, description) in zip(feature_cols, features):
        with column:
            st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><div class="feature-title">{title}</div><div class="feature-copy">{description}</div></div>', unsafe_allow_html=True)


def render_quick_actions(backend_url: str) -> None:
    st.markdown('<div class="section-label">Refine this itinerary</div>', unsafe_allow_html=True)
    columns = st.columns(len(QUICK_ACTIONS))
    for column, (label, question) in zip(columns, QUICK_ACTIONS.items()):
        with column:
            if st.button(label, key=f"action_{label}", use_container_width=True):
                run_planner(question, backend_url)
                st.rerun()


load_css()
init_state()
backend_url = os.getenv("BACKEND_URL", DEFAULT_BACKEND_URL).rstrip("/")
render_sidebar(backend_url)

if not st.session_state.messages:
    render_empty_state()
else:
    st.markdown('<div class="eyebrow">Active workspace</div>', unsafe_allow_html=True)
    st.title("Your travel plan, in progress.")
    st.markdown('<div class="hero-copy">Ask a follow-up, refine the constraints, or use a quick action below to shape the itinerary.</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    render_messages()
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.active_trip:
        st.markdown(f'<div class="result-banner">✨ Saved to Recent Trips · {st.session_state.active_trip["title"]}</div>', unsafe_allow_html=True)
    render_quick_actions(backend_url)
    user_input = st.chat_input("Ask a follow-up or refine your itinerary...", key="trip_chat_input")
    if user_input and user_input.strip():
        run_planner(user_input.strip(), backend_url)
        st.rerun()
