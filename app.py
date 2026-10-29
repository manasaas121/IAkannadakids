import random
import streamlit as st

st.set_page_config(
    page_title="ಸ್ಮಾರ್ಟ್ ಕನ್ನಡ ಕಲಿಕೆ",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Styling --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Kannada:wght@400;500;600;700&display=swap');
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Noto Sans Kannada', sans-serif;
}
.stApp { background: #F4F8FF; }
[data-testid="stSidebar"] { background: #E3F2FD; }
.hero {
    background: linear-gradient(120deg, #0D47A1, #1976D2);
    padding: 1.5rem 1.7rem;
    border-radius: 18px;
    color: white;
    margin-bottom: 1rem;
}
.hero h1 { color: white; margin: 0; font-size: 2rem; }
.hero p { color: #EAF3FF; margin: .4rem 0 0 0; }
.module-card {
    background: white; border: 1px solid #D6E7FF; border-radius: 16px;
    padding: 1rem; min-height: 145px; box-shadow: 0 3px 12px rgba(21,101,192,.07);
}
.module-card h3 { color: #1565C0; margin-top: 0; font-size: 1.1rem; }
.module-card p { color: #455A64; font-size: .92rem; }
div.stButton > button {
    background: #1565C0; color: white; border: 0; border-radius: 10px;
    min-height: 2.7rem; font-weight: 600; width: 100%;
}
div.stButton > button:hover { background: #0D47A1; color: white; border: 0; }
h1, h2, h3 { color: #123D73; }
.small-note { color: #526579; font-size: .9rem; }
</style>
""", unsafe_allow_html=True)

# -------------------- Sample content --------------------
VOWELS = ["ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ", "ಋ", "ಎ", "ಏ", "ಐ", "ಒ", "ಓ", "ಔ", "ಅಂ", "ಅಃ"]
CONSONANT_GROUPS = {
    "ಕ ವರ್ಗ": ["ಕ", "ಖ", "ಗ", "ಘ", "ಙ"],
    "ಚ ವರ್ಗ": ["ಚ", "ಛ", "ಜ", "ಝ", "ಞ"],
    "ಟ ವರ್ಗ": ["ಟ", "ಠ", "ಡ", "ಢ", "ಣ"],
    "ತ ವರ್ಗ": ["ತ", "ಥ", "ದ", "ಧ", "ನ"],
    "ಪ ವರ್ಗ": ["ಪ", "ಫ", "ಬ", "ಭ", "ಮ"],
    "ಅಂತಸ್ಥ": ["ಯ", "ರ", "ಲ", "ವ"],
    "ಉಷ್ಮ": ["ಶ", "ಷ", "ಸ", "ಹ", "ಳ"],
}
GUNITAKSHARA = ["ಕ", "ಕಾ", "ಕಿ", "ಕೀ", "ಕು", "ಕೂ", "ಕೃ", "ಕೆ", "ಕೇ", "ಕೈ", "ಕೊ", "ಕೋ", "ಕೌ", "ಕಂ", "ಕಃ"]

WORD_SETS = {
    "ಎರಡು ಅಕ್ಷರದ ಪದಗಳು": [
        ("ಮನೆ", "ವಾಸಿಸುವ ಸ್ಥಳ"), ("ಹಸು", "ಒಂದು ಸಾಕುಪ್ರಾಣಿ"), ("ಮರ", "ಸಸ್ಯದ ಒಂದು ರೂಪ"),
        ("ಕಿವಿ", "ಕೇಳಲು ಸಹಾಯ ಮಾಡುವ ಅಂಗ"), ("ಹಣ", "ವಿನಿಮಯಕ್ಕೆ ಬಳಸುವದು"),
        ("ಹಣ್ಣು", "ಸಸ್ಯದಿಂದ ದೊರೆಯುವ ಆಹಾರ"), ("ಕವಿ", "ಕವಿತೆ ಬರೆಯುವವರು")
    ],
    "ಮೂರು ಅಕ್ಷರದ ಪದಗಳು": [
        ("ಕಮಲ", "ಒಂದು ಹೂವು"), ("ನಗರ", "ಜನರು ವಾಸಿಸುವ ದೊಡ್ಡ ಸ್ಥಳ"),
        ("ಅಡಿಗೆ", "ಆಹಾರ ತಯಾರಿಸುವ ಕೆಲಸ"), ("ಮಗು", "ಚಿಕ್ಕ ವಯಸ್ಸಿನ ವ್ಯಕ್ತಿ"),
        ("ಕಡಲೆ", "ಒಂದು ದ್ವಿದಳ ಧಾನ್ಯ"), ("ಬಾಳೆ", "ಒಂದು ಹಣ್ಣು")
    ],
    "ಸಜಾತಿ ಒತ್ತಕ್ಷರಗಳು": [
        ("ಅಕ್ಕ", "ಅಕ್ಕ ಎಂಬ ಸಂಬಂಧದ ಪದ"), ("ಅಪ್ಪ", "ತಂದೆಯನ್ನು ಕರೆಯುವ ಪದ"),
        ("ಅಣ್ಣ", "ಅಣ್ಣ ಎಂಬ ಸಂಬಂಧದ ಪದ"), ("ಕಲ್ಲು", "ಗಟ್ಟಿಯಾದ ನೈಸರ್ಗಿಕ ವಸ್ತು"),
        ("ಮಲ್ಲಿಗೆ", "ಸುಗಂಧದ ಹೂವು")
    ],
    "ವಿಜಾತಿ ಒತ್ತಕ್ಷರಗಳು": [
        ("ಅಕ್ಷರ", "ಬರಹದ ಒಂದು ಘಟಕ"), ("ಭಕ್ತಿ", "ಶ್ರದ್ಧೆ"), ("ಶಕ್ತಿ", "ಸಾಮರ್ಥ್ಯ"),
        ("ವಿದ್ಯೆ", "ಜ್ಞಾನ ಅಥವಾ ಶಿಕ್ಷಣ"), ("ಮಿತ್ರ", "ಸ್ನೇಹಿತ")
    ],
    "ಬಹು ಒತ್ತಕ್ಷರದ ಪದಗಳು": [
        ("ಸ್ವಾತಂತ್ರ್ಯ", "ಸ್ವತಂತ್ರವಾಗಿರುವ ಸ್ಥಿತಿ"), ("ವಿದ್ಯಾರ್ಥಿ", "ಕಲಿಯುವ ವ್ಯಕ್ತಿ"),
        ("ಪ್ರಶ್ನೆ", "ಉತ್ತರ ನಿರೀಕ್ಷಿಸುವ ವಿಚಾರ"), ("ಸಂಸ್ಕೃತಿ", "ಸಮಾಜದ ಜೀವನ ಪದ್ಧತಿ"),
        ("ವ್ಯಕ್ತಿತ್ವ", "ವ್ಯಕ್ತಿಯ ಗುಣಗಳ ಸಮೂಹ")
    ],
}
PROVERBS = [
    ("ಅತಿ ಆಸೆ ______", ["ಗತಿ ಕೇಡು", "ಮನೆ ಹಾಳು", "ಕೆಲಸ ಸುಲಭ", "ಮಾತು ಸಿಹಿ"], "ಗತಿ ಕೇಡು", "ಅತಿಯಾದ ಆಸೆ ತೊಂದರೆಗೆ ಕಾರಣವಾಗಬಹುದು."),
    ("ಒಗ್ಗಟ್ಟಿನಲ್ಲಿ ______", ["ಬಲವಿದೆ", "ಭಯವಿದೆ", "ಸೋಲಿದೆ", "ನಷ್ಟವಿದೆ"], "ಬಲವಿದೆ", "ಒಟ್ಟಾಗಿ ಕೆಲಸ ಮಾಡಿದರೆ ಶಕ್ತಿ ಹೆಚ್ಚುತ್ತದೆ."),
    ("ಹನಿ ಹನಿ ಕೂಡಿದರೆ ______", ["ಹಳ್ಳ", "ಬೆಟ್ಟ", "ಮರ", "ಮನೆ"], "ಹಳ್ಳ", "ಸಣ್ಣ ಪ್ರಯತ್ನಗಳು ಸೇರಿ ದೊಡ್ಡ ಫಲಿತಾಂಶ ನೀಡುತ್ತವೆ."),
    ("ಮಾತು ಬೆಳ್ಳಿ, ಮೌನ ______", ["ಬಂಗಾರ", "ಕಬ್ಬಿಣ", "ತಾಮ್ರ", "ಮಣ್ಣು"], "ಬಂಗಾರ", "ಕೆಲವೊಮ್ಮೆ ಮೌನವೇ ಹೆಚ್ಚು ಮೌಲ್ಯಯುತ.")
]
GK = [
    ("ಭಾರತದ ರಾಷ್ಟ್ರೀಯ ಪ್ರಾಣಿ ಯಾವುದು?", ["ಹುಲಿ", "ಸಿಂಹ", "ಆನೆ", "ಚಿರತೆ"], "ಹುಲಿ", "ಭಾರತದ ರಾಷ್ಟ್ರೀಯ ಪ್ರಾಣಿ ಬೆಂಗಾಲ್ ಹುಲಿ."),
    ("ಭಾರತದ ರಾಷ್ಟ್ರೀಯ ಪಕ್ಷಿ ಯಾವುದು?", ["ನವಿಲು", "ಗಿಳಿ", "ಹದ್ದು", "ಪಾರಿವಾಳ"], "ನವಿಲು", "ಭಾರತದ ರಾಷ್ಟ್ರೀಯ ಪಕ್ಷಿ ಭಾರತೀಯ ನವಿಲು."),
    ("ಭಾರತದ ರಾಷ್ಟ್ರೀಯ ಹೂವು ಯಾವುದು?", ["ಕಮಲ", "ಗುಲಾಬಿ", "ಮಲ್ಲಿಗೆ", "ಸೂರ್ಯಕಾಂತಿ"], "ಕಮಲ", "ಕಮಲವು ಭಾರತದ ರಾಷ್ಟ್ರೀಯ ಹೂವು."),
    ("ಭಾರತದ ರಾಜಧಾನಿ ಯಾವುದು?", ["ನವದೆಹಲಿ", "ಮುಂಬೈ", "ಚೆನ್ನೈ", "ಕೋಲ್ಕತ್ತಾ"], "ನವದೆಹಲಿ", "ಭಾರತದ ರಾಜಧಾನಿ ನವದೆಹಲಿ."),
    ("ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ ಯಾವುದು?", ["ಬೆಂಗಳೂರು", "ಮೈಸೂರು", "ಹುಬ್ಬಳ್ಳಿ", "ಬೆಳಗಾವಿ"], "ಬೆಂಗಳೂರು", "ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ ಬೆಂಗಳೂರು."),
    ("ಭಾರತದ ರಾಷ್ಟ್ರಗೀತೆ ಯಾವುದು?", ["ಜನ ಗಣ ಮನ", "ವಂದೇ ಮಾತರಂ", "ಸಾರೆ ಜಹಾಂ ಸೇ ಅಚ್ಚಾ", "ಏಕಲವ್ಯ"], "ಜನ ಗಣ ಮನ", "ಜನ ಗಣ ಮನ ಭಾರತದ ರಾಷ್ಟ್ರಗೀತೆ; ವಂದೇ ಮಾತರಂ ರಾಷ್ಟ್ರೀಯ ಗೀತೆಯಾಗಿದೆ."),
    ("ಭಾರತದ ರಾಷ್ಟ್ರೀಯ ಮರ ಯಾವುದು?", ["ಆಲದ ಮರ", "ಬೇವಿನ ಮರ", "ತೆಂಗಿನ ಮರ", "ಮಾವು"], "ಆಲದ ಮರ", "ಆಲದ ಮರವು ಭಾರತದ ರಾಷ್ಟ್ರೀಯ ಮರ.")
]
MATCH_PAIRS = [
    ("ಹುಲಿ", "ಪ್ರಾಣಿ"), ("ನವಿಲು", "ಪಕ್ಷಿ"), ("ಕಮಲ", "ಹೂವು"),
    ("ಮಾವು", "ಹಣ್ಣು"), ("ಬೆಂಗಳೂರು", "ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ"), ("ಆಲದ ಮರ", "ರಾಷ್ಟ್ರೀಯ ಮರ")
]
PICTURE_PAIRS = [
    ("🐅", "ಹುಲಿ"), ("🦚", "ನವಿಲು"), ("🌸", "ಹೂವು"),
    ("🥭", "ಮಾವು"), ("🐄", "ಹಸು"), ("🌳", "ಮರ"),
    ("🍌", "ಬಾಳೆಹಣ್ಣು"), ("📚", "ಪುಸ್ತಕ"), ("🚲", "ಸೈಕಲ್"), ("🐘", "ಆನೆ")
]
JUMBLED = [
    ("ನೆಮ", "ಮನೆ"), ("ಸುಹ", "ಹಸು"), ("ಲಮಕ", "ಕಮಲ"),
    ("ಲಗರ", "ನಗರ"), ("ಕ್ಷರಅ", "ಅಕ್ಷರ"), ("ಕ್ತಿ ಭ", "ಭಕ್ತಿ")
]

def init_state():
    defaults = {
        "page": "ಮುಖಪುಟ", "points": 0, "completed": set(),
        "answered": set(), "quiz_feedback": {}, "daily_done": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

def go(page):
    st.session_state.page = page

def award_once(key, points=10):
    if key not in st.session_state.answered:
        st.session_state.answered.add(key)
        st.session_state.points += points

def section_title(title, subtitle=None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## 📘 ಸ್ಮಾರ್ಟ್ ಕನ್ನಡ ಕಲಿಕೆ")
    st.caption("ಅಕ್ಷರದಿಂದ ಜ್ಞಾನದೆಡೆಗೆ")
    menu = [
        "ಮುಖಪುಟ", "ಸ್ವರಗಳು ಮತ್ತು ವ್ಯಂಜನಗಳು", "ಗುಣಿತಾಕ್ಷರಗಳು",
        "ಪದಗಳ ಕಲಿಕೆ", "ಒತ್ತಕ್ಷರಗಳ ಕಲಿಕೆ", "ಗಾದೆಮಾತುಗಳು",
        "ಪದಗಳ ಜೋಡಣೆ", "ಚಿತ್ರಗಳ ಹೊಂದಾಣಿಕೆ", "Jumbled Words",
        "ಸಾಮಾನ್ಯ ಜ್ಞಾನ", "ಕನ್ನಡ ರಸಪ್ರಶ್ನೆ", "ನನ್ನ ಕಲಿಕಾ ಪ್ರಗತಿ"
    ]
    for item in menu:
        if st.button(item, key="nav_" + item, use_container_width=True):
            go(item)
    st.divider()
    st.metric("⭐ ಒಟ್ಟು ಅಂಕಗಳು", st.session_state.points)
    st.caption("ಆವೃತ್ತಿ 1.0 · ಸ್ಥಳೀಯ ಕಲಿಕಾ ಮಾದರಿ")

# -------------------- Header --------------------
st.markdown("""
<div class="hero">
  <h1>ಸ್ಮಾರ್ಟ್ ಕನ್ನಡ ಕಲಿಕೆ 📘</h1>
  <p>ಅಕ್ಷರದಿಂದ ಜ್ಞಾನದೆಡೆಗೆ – ಕನ್ನಡ ಕಲಿಯೋಣ, ಆನಂದಿಸೋಣ!</p>
</div>
""", unsafe_allow_html=True)

page = st.session_state.page

# -------------------- Home --------------------
if page == "ಮುಖಪುಟ":
    st.subheader("ನಿಮ್ಮ ಕಲಿಕಾ ಪ್ರಯಾಣವನ್ನು ಆರಂಭಿಸಿ")
    st.write("ಕೆಳಗಿನ ಪಾಠಗಳಲ್ಲಿ ಒಂದನ್ನು ಆಯ್ಕೆ ಮಾಡಿ. ಅಭ್ಯಾಸಗಳ ಮೂಲಕ ಅಂಕಗಳನ್ನು ಗಳಿಸಿ.")
    cards = [
        ("🔤", "ಸ್ವರಗಳು ಮತ್ತು ವ್ಯಂಜನಗಳು", "ಕನ್ನಡ ವರ್ಣಮಾಲೆಯ ಮೂಲಭೂತ ಪಾಠ"),
        ("🧩", "ಗುಣಿತಾಕ್ಷರಗಳು", "ಕ ಅಕ್ಷರದ ವಿವಿಧ ರೂಪಗಳನ್ನು ಕಲಿಯಿರಿ"),
        ("📖", "ಪದಗಳ ಕಲಿಕೆ", "ಎರಡು, ಮೂರು ಅಕ್ಷರದ ಪದಗಳು"),
        ("🔠", "ಒತ್ತಕ್ಷರಗಳ ಕಲಿಕೆ", "ಸಜಾತಿ, ವಿಜಾತಿ ಮತ್ತು ಬಹು ಒತ್ತಕ್ಷರಗಳು"),
        ("💬", "ಗಾದೆಮಾತುಗಳು", "ಗಾದೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ"),
        ("🔗", "ಪದಗಳ ಜೋಡಣೆ", "ಪದ ಮತ್ತು ಅರ್ಥ ಹೊಂದಿಸಿ"),
        ("🖼️", "ಚಿತ್ರಗಳ ಹೊಂದಾಣಿಕೆ", "ಚಿತ್ರವನ್ನು ಸರಿಯಾದ ಕನ್ನಡ ಪದಕ್ಕೆ ಹೊಂದಿಸಿ"),
        ("🔀", "Jumbled Words", "ಅಕ್ಷರಗಳನ್ನು ಸರಿಯಾದ ಕ್ರಮದಲ್ಲಿ ಜೋಡಿಸಿ"),
        ("🌏", "ಸಾಮಾನ್ಯ ಜ್ಞಾನ", "ಭಾರತ ಮತ್ತು ಕರ್ನಾಟಕದ ಮಾಹಿತಿ"),
        ("🏆", "ಕನ್ನಡ ರಸಪ್ರಶ್ನೆ", "ನಿಮ್ಮ ಜ್ಞಾನವನ್ನು ಪರೀಕ್ಷಿಸಿ"),
    ]
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(cards):
        with cols[i % 2]:
            st.markdown(f'<div class="module-card"><h3>{icon} {title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"{title} ಆರಂಭಿಸಿ", key=f"home_{i}"):
                go(title)
                st.rerun()
    st.info("ಸಲಹೆ: ಪ್ರತಿದಿನ 10 ನಿಮಿಷ ಅಭ್ಯಾಸ ಮಾಡಿ. ತಪ್ಪಾದ ಉತ್ತರಗಳನ್ನು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.")

# -------------------- Alphabet --------------------
elif page == "ಸ್ವರಗಳು ಮತ್ತು ವ್ಯಂಜನಗಳು":
    section_title("ಸ್ವರಗಳು ಮತ್ತು ವ್ಯಂಜನಗಳು", "ಅಕ್ಷರದ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿ ಅಥವಾ ಆಯ್ಕೆ ಮಾಡಿ ಅಭ್ಯಾಸ ಮಾಡಿ.")
    tab1, tab2 = st.tabs(["ಸ್ವರಗಳು", "ವ್ಯಂಜನಗಳು"])
    with tab1:
        st.write("### ಕನ್ನಡ ಸ್ವರಗಳು")
        cols = st.columns(5)
        for i, letter in enumerate(VOWELS):
            with cols[i % 5]:
                st.button(letter, key=f"vowel_{i}", help=f"ಸ್ವರ: {letter}")
        st.success("ಸ್ವರಗಳನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಓದಿ, ನಂತರ ನಿಮ್ಮ ನೋಟ್‌ಬುಕ್‌ನಲ್ಲಿ ಬರೆಯಿರಿ.")
    with tab2:
        for group, letters in CONSONANT_GROUPS.items():
            st.markdown(f"**{group}**")
            st.write("　".join(letters))
        st.info("ವ್ಯಂಜನಗಳನ್ನು ವರ್ಗಗಳಾಗಿ ಕಲಿತರೆ ನೆನಪಿಡಲು ಸುಲಭ.")

# -------------------- Gunithakshara --------------------
elif page == "ಗುಣಿತಾಕ್ಷರಗಳು":
    section_title("ಗುಣಿತಾಕ್ಷರಗಳು", "ಕ ಅಕ್ಷರದೊಂದಿಗೆ ಸ್ವರಗಳ ಸಂಯೋಜನೆ.")
    st.markdown("### ಕ ಅಕ್ಷರದ ಗುಣಿತಾಕ್ಷರಗಳು")
    st.markdown(" ".join([f"`{x}`" for x in GUNITAKSHARA]))
    selected = st.selectbox("ಅಭ್ಯಾಸಕ್ಕೆ ಒಂದು ರೂಪ ಆಯ್ಕೆಮಾಡಿ", GUNITAKSHARA)
    st.markdown(f"<div class='module-card'><h1 style='text-align:center;color:#1565C0;font-size:4rem'>{selected}</h1><p style='text-align:center'>ಈ ಅಕ್ಷರವನ್ನು ಮೂರು ಬಾರಿ ಓದಿ ಮತ್ತು ಬರೆಯಿರಿ.</p></div>", unsafe_allow_html=True)
    if st.button("ಈ ಪಾಠ ಪೂರ್ಣಗೊಳಿಸಿದೆ", key="complete_gun"):
        st.session_state.completed.add("ಗುಣಿತಾಕ್ಷರಗಳು")
        st.success("ಪಾಠ ಪೂರ್ಣಗೊಂಡಿದೆ!")

# -------------------- Word learning --------------------
elif page == "ಪದಗಳ ಕಲಿಕೆ":
    section_title("ಪದಗಳ ಕಲಿಕೆ", "ಪದ ಓದಿ, ಅದರ ಅರ್ಥ ತಿಳಿದುಕೊಳ್ಳಿ.")
    category = st.selectbox("ಪದಗಳ ವಿಭಾಗ ಆಯ್ಕೆಮಾಡಿ", list(WORD_SETS.keys()))
    words = WORD_SETS[category]
    for idx, (word, meaning) in enumerate(words):
        with st.expander(f"{word} — ಪದ {idx+1}"):
            st.markdown(f"### {word}")
            st.write(f"**ಅರ್ಥ:** {meaning}")
            st.write("ಅಭ್ಯಾಸ: ಈ ಪದವನ್ನು ಜೋರಾಗಿ ಓದಿ ಮತ್ತು ಬರೆಯಿರಿ.")
    if st.button("ಪದಗಳ ಪಾಠ ಪೂರ್ಣಗೊಳಿಸಿದೆ"):
        st.session_state.completed.add(category)
        st.success("ಚೆನ್ನಾಗಿದೆ! ಪಾಠ ಪೂರ್ಣಗೊಂಡಿದೆ.")

# -------------------- Ottakshara --------------------
elif page == "ಒತ್ತಕ್ಷರಗಳ ಕಲಿಕೆ":
    section_title("ಒತ್ತಕ್ಷರಗಳ ಕಲಿಕೆ", "ಉದಾಹರಣೆಗಳನ್ನು ಓದಿ, ಅಕ್ಷರ ಸಂಯೋಜನೆಯನ್ನು ಗಮನಿಸಿ.")
    category = st.radio("ವಿಭಾಗ", list(WORD_SETS.keys())[2:], horizontal=True)
    for word, meaning in WORD_SETS[category]:
        st.markdown(f"- **{word}** — {meaning}")
    st.info("ಸೂಚನೆ: ಪದಗಳ ಅಕ್ಷರ ಎಣಿಕೆ ಮತ್ತು ಒತ್ತಕ್ಷರಗಳ ವರ್ಗೀಕರಣವನ್ನು ಕಲಿಕೆಯ ಮಟ್ಟಕ್ಕೆ ತಕ್ಕಂತೆ ಶಿಕ್ಷಕರು ಪರಿಶೀಲಿಸಬಹುದು.")

# -------------------- Proverbs --------------------
elif page == "ಗಾದೆಮಾತುಗಳು":
    section_title("ಗಾದೆಮಾತುಗಳನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ", "ಸರಿಯಾದ ಉತ್ತರ ಆಯ್ಕೆ ಮಾಡಿ ಅಂಕ ಗಳಿಸಿ.")
    idx = st.selectbox("ಪ್ರಶ್ನೆ ಸಂಖ್ಯೆ", list(range(len(PROVERBS))), format_func=lambda x: f"ಪ್ರಶ್ನೆ {x+1}")
    question, options, answer, meaning = PROVERBS[idx]
    st.markdown(f"### {question}")
    choice = st.radio("ಸರಿಯಾದ ಪದ ಆಯ್ಕೆಮಾಡಿ", options, key=f"proverb_choice_{idx}")
    if st.button("ಉತ್ತರ ಪರಿಶೀಲಿಸಿ", key=f"proverb_submit_{idx}"):
        if choice == answer:
            award_once(f"proverb_{idx}", 10)
            st.success(f"ಸರಿಯಾದ ಉತ್ತರ: {answer}")
        else:
            st.error(f"ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ. ಸರಿಯಾದ ಉತ್ತರ: {answer}")
        st.info(f"ಅರ್ಥ: {meaning}")

# -------------------- Matching --------------------
elif page == "ಪದಗಳ ಜೋಡಣೆ":
    section_title("ಪದಗಳ ಜೋಡಣೆ", "ಪ್ರತಿ ಪದಕ್ಕೆ ಸರಿಯಾದ ವರ್ಗವನ್ನು ಹೊಂದಿಸಿ.")
    pair = random.choice(MATCH_PAIRS)
    st.write("**ಈ ಸುತ್ತಿನ ಪದ:**", pair[0])
    options = list(dict.fromkeys([p[1] for p in MATCH_PAIRS]))
    random.shuffle(options)
    selected = st.selectbox("ಇದು ಯಾವುದಕ್ಕೆ ಸೇರಿದೆ?", options, key="match_select")
    if st.button("ಹೊಂದಾಣಿಕೆ ಪರಿಶೀಲಿಸಿ"):
        if selected == pair[1]:
            award_once("match_" + pair[0], 5)
            st.success("ಸರಿಯಾದ ಹೊಂದಾಣಿಕೆ! +5 ಅಂಕಗಳು")
        else:
            st.error(f"ಸರಿಯಾದ ಉತ್ತರ: {pair[1]}")
    st.caption("ಪ್ರತಿ ಬಾರಿ ಹೊಸ ಪದ ಆಯ್ಕೆ ಮಾಡಲು ಪುಟವನ್ನು ಮರುಚಾಲನೆ ಮಾಡಿ.")

# -------------------- Picture matching --------------------
elif page == "ಚಿತ್ರಗಳ ಹೊಂದಾಣಿಕೆ":
    section_title("ಚಿತ್ರಗಳ ಹೊಂದಾಣಿಕೆ", "ಚಿತ್ರ ನೋಡಿ ಸರಿಯಾದ ಕನ್ನಡ ಪದವನ್ನು ಆಯ್ಕೆಮಾಡಿ.")
    item = random.choice(PICTURE_PAIRS)
    st.markdown(f"<div class='module-card' style='text-align:center'><div style='font-size:5rem'>{item[0]}</div><h3>ಈ ಚಿತ್ರಕ್ಕೆ ಸರಿಯಾದ ಪದ ಯಾವುದು?</h3></div>", unsafe_allow_html=True)
    options = list(dict.fromkeys([x[1] for x in PICTURE_PAIRS]))
    random.shuffle(options)
    selected = st.selectbox("ಪದ ಆಯ್ಕೆಮಾಡಿ", options, key="picture_select")
    if st.button("ಉತ್ತರ ಪರಿಶೀಲಿಸಿ", key="picture_check"):
        if selected == item[1]:
            award_once("picture_" + item[1], 5)
            st.success("ಸರಿಯಾಗಿದೆ! +5 ಅಂಕಗಳು")
        else:
            st.error(f"ಸರಿಯಾದ ಪದ: {item[1]}")

# -------------------- Jumbled words --------------------
elif page == "Jumbled Words":
    section_title("Jumbled Words – ಪದ ಜೋಡಣೆ", "ಕೊಟ್ಟಿರುವ ಅಕ್ಷರಗಳನ್ನು ಸರಿಯಾದ ಪದವಾಗಿ ಬರೆಯಿರಿ.")
    item = random.choice(JUMBLED)
    st.markdown(f"<div class='module-card' style='text-align:center'><h2>{item[0]}</h2><p>ಈ ಅಕ್ಷರಗಳನ್ನು ಸರಿಯಾದ ಕ್ರಮದಲ್ಲಿ ಜೋಡಿಸಿ.</p></div>", unsafe_allow_html=True)
    answer = st.text_input("ಸರಿಯಾದ ಕನ್ನಡ ಪದವನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ", key="jumble_answer")
    if st.button("ಪದ ಪರಿಶೀಲಿಸಿ", key="jumble_check"):
        if answer.strip().replace(" ", "") == item[1].replace(" ", ""):
            award_once("jumble_" + item[1], 10)
            st.success("ಅದ್ಭುತ! ಸರಿಯಾದ ಪದ. +10 ಅಂಕಗಳು")
        else:
            st.error("ಇನ್ನೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ.")
            st.caption(f"ಸುಳಿವು: ಪದದ ಮೊದಲ ಅಕ್ಷರ “{item[1][0]}”")
    st.caption("ಇದು ಸರಳ ಮಾದರಿ ಆಟ. ಮುಂದಿನ ಆವೃತ್ತಿಯಲ್ಲಿ Unicode-aware ಅಕ್ಷರ ಘಟಕಗಳ ಜೋಡಣೆ ಸೇರಿಸಬಹುದು.")

# -------------------- General Knowledge --------------------
elif page == "ಸಾಮಾನ್ಯ ಜ್ಞಾನ":
    section_title("ಸಾಮಾನ್ಯ ಜ್ಞಾನ", "ಭಾರತ ಮತ್ತು ಕರ್ನಾಟಕದ ಕುರಿತು ತಿಳಿದುಕೊಳ್ಳಿ.")
    for q, opts, ans, explanation in GK:
        with st.expander(q):
            user_answer = st.radio("ಉತ್ತರ ಆಯ್ಕೆಮಾಡಿ", opts, key="gk_" + q)
            if st.button("ಪರಿಶೀಲಿಸಿ", key="gk_submit_" + q):
                if user_answer == ans:
                    award_once("gk_" + q, 5)
                    st.success("ಸರಿಯಾದ ಉತ್ತರ! +5 ಅಂಕಗಳು")
                else:
                    st.error(f"ಸರಿಯಾದ ಉತ್ತರ: {ans}")
                st.write(explanation)
    st.caption("ಸಾಮಾನ್ಯ ಜ್ಞಾನ ವಿಭಾಗದಲ್ಲಿ ಪ್ರಸ್ತುತ ಹುದ್ದೆದಾರರು ಮತ್ತು ಬದಲಾಗುವ ಮಾಹಿತಿಯನ್ನು ಕಾಲಕಾಲಕ್ಕೆ ನವೀಕರಿಸಬೇಕು.")

# -------------------- Quiz --------------------
elif page == "ಕನ್ನಡ ರಸಪ್ರಶ್ನೆ":
    section_title("ಕನ್ನಡ ರಸಪ್ರಶ್ನೆ", "ಪ್ರತಿ ಪ್ರಶ್ನೆಗೆ ಸರಿಯಾದ ಉತ್ತರ ಆಯ್ಕೆಮಾಡಿ.")
    quiz_items = [
        ("ಕನ್ನಡದ ಮೊದಲ ಸ್ವರ ಯಾವುದು?", ["ಅ", "ಕ", "ಮ", "ಯ"], "ಅ"),
        ("‘ಅಕ್ಕ’ ಪದದಲ್ಲಿ ಯಾವ ರೀತಿಯ ಒತ್ತಕ್ಷರ ಇದೆ?", ["ಸಜಾತಿ", "ವಿಜಾತಿ", "ಒತ್ತಕ್ಷರ ಇಲ್ಲ", "ಬಹು ಒತ್ತಕ್ಷರ"], "ಸಜಾತಿ"),
        ("‘ಕಮಲ’ ಎಂದರೆ ಏನು?", ["ಹೂವು", "ಪಕ್ಷಿ", "ನದಿ", "ಮರ"], "ಹೂವು"),
        ("ಭಾರತದ ರಾಷ್ಟ್ರೀಯ ಪಕ್ಷಿ ಯಾವುದು?", ["ನವಿಲು", "ಗಿಳಿ", "ಹದ್ದು", "ಕಾಗೆ"], "ನವಿಲು"),
    ]
    score = 0
    for i, (q, opts, ans) in enumerate(quiz_items):
        st.markdown(f"**{i+1}. {q}**")
        selected = st.radio("ಉತ್ತರ", opts, key=f"quiz_{i}", horizontal=True)
        if selected == ans:
            score += 1
    if st.button("ರಸಪ್ರಶ್ನೆ ಫಲಿತಾಂಶ ನೋಡಿ"):
        st.success(f"ನಿಮ್ಮ ಅಂಕ: {score}/{len(quiz_items)} ({round(score/len(quiz_items)*100)}%)")
        st.session_state.completed.add("ಕನ್ನಡ ರಸಪ್ರಶ್ನೆ")

# -------------------- Progress --------------------
elif page == "ನನ್ನ ಕಲಿಕಾ ಪ್ರಗತಿ":
    section_title("ನನ್ನ ಕಲಿಕಾ ಪ್ರಗತಿ", "ಈ ಬ್ರೌಸರ್ ಅಧಿವೇಶನದಲ್ಲಿ ನಿಮ್ಮ ಸಾಧನೆ.")
    c1, c2, c3 = st.columns(3)
    c1.metric("ಒಟ್ಟು ಅಂಕಗಳು", st.session_state.points)
    c2.metric("ಪೂರ್ಣಗೊಳಿಸಿದ ಪಾಠಗಳು", len(st.session_state.completed))
    c3.metric("ಸರಿಯಾದ ಉತ್ತರಗಳ ದಾಖಲೆ", len(st.session_state.answered))
    st.progress(min(st.session_state.points / 100, 1.0), text="ಅಂಕಗಳ ಗುರಿ: 100")
    if st.session_state.completed:
        st.markdown("### ಪೂರ್ಣಗೊಂಡ ಪಾಠಗಳು")
        for lesson in sorted(st.session_state.completed):
            st.write(f"✅ {lesson}")
    else:
        st.info("ಪಾಠ ಪೂರ್ಣಗೊಳಿಸಿದಾಗ ನಿಮ್ಮ ಪ್ರಗತಿ ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತದೆ.")
    st.warning("ಗಮನಿಸಿ: ಈ MVP ಆವೃತ್ತಿಯಲ್ಲಿ ಪ್ರಗತಿ Streamlit session ನಲ್ಲಿ ಮಾತ್ರ ಉಳಿಯುತ್ತದೆ. ಶಾಶ್ವತ ಪ್ರಗತಿಗಾಗಿ SQLite/database ಸೇರಿಸಬೇಕು.")

st.divider()
st.markdown(
    "<div style='text-align:center;color:#526579;font-size:.85rem'>"
    "ಸ್ಮಾರ್ಟ್ ಕನ್ನಡ ಕಲಿಕೆ · ಕಲಿಯೋಣ, ಅಭ್ಯಾಸ ಮಾಡೋಣ, ಸಾಧಿಸೋಣ!"
    "</div>",
    unsafe_allow_html=True
)
