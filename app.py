
import html
import streamlit as st

from dotenv import load_dotenv
from services.gnani_service import (
    transcribe_audio,
    synthesize_speech,
    get_api_status
)
from services.assistant import answer_query
from services.database import (
    init_db,
    save_interaction,
    save_grievance,
    recent_interactions
)
from services.language import LANGUAGES


# --------------------------------------------------
# INITIAL SETUP
# --------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="Sahaaya AI | Citizen Services",
    page_icon="🇮🇳",
    layout="wide"
)


# --------------------------------------------------
# COMPLETE CSS STYLING
# --------------------------------------------------

CSS = """
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+Tamil:wght@400;500;600;700&family=Noto+Sans+Telugu:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');

:root {
    --ink: #1e2933;
    --muted: #526071;
    --line: #e6e9ec;
    --green: #28594b;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', 'Noto Sans Telugu',
    'Noto Sans Devanagari', 'Noto Sans Tamil', sans-serif;
}

.stApp {
    background: #f5f7f6 !important;
    color: var(--ink) !important;
}

.block-container {
    max-width: 1180px;
    padding: 1.4rem 1.5rem 3rem;
}

/* Main page text */

[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] label,
[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4 {
    color: var(--ink);
}

/* Sidebar */

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: #22211e !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #ffffff !important;
}

/* Sidebar navigation */

[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stRadio"] p,
[data-testid="stSidebar"] [data-testid="stRadio"] span {
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 5px 2px;
}

/* Sidebar dropdown */

[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] *,
[data-testid="stSidebar"] [data-testid="stSelectbox"] input {
    color: #1e2933 !important;
    -webkit-text-fill-color: #1e2933 !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] svg {
    fill: #1e2933 !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] {
    color: #1e2933 !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] * {
    color: inherit;
}

/* Brand */

.brand {
    display: flex;
    align-items: center;
    gap: 13px;
    border-bottom: 1px solid var(--line);
    padding: 4px 0 17px;
    margin-bottom: 25px;
}

.brand-icon {
    width: 44px;
    height: 44px;
    flex-shrink: 0;
    border-radius: 12px;
    background: #28594b;
    color: #ffffff !important;
    display: grid;
    place-items: center;
    font-weight: 800;
    font-size: 20px;
}

.brand-name {
    font-size: 22px;
    font-weight: 700;
    color: #1e2933 !important;
}

.brand-sub {
    font-size: 12px;
    color: #667085 !important;
    margin-top: 2px;
}

.eyebrow {
    font-size: 11px;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #557267 !important;
    font-weight: 700;
}

.hero {
    font-size: 32px;
    line-height: 1.18;
    font-weight: 700;
    letter-spacing: -1px;
    margin: 7px 0;
    color: #1e2933 !important;
}

.hero-copy {
    max-width: 760px;
    color: #526071 !important;
    line-height: 1.65;
    font-size: 15px;
}

/* Cards */

.panel {
    background: #ffffff;
    border: 1px solid #e6e9ec;
    border-radius: 15px;
    padding: 19px 20px;
    margin: 8px 0 14px;
}

.panel-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 5px;
    color: #1e2933 !important;
}

.panel-copy {
    font-size: 13px;
    color: #526071 !important;
    line-height: 1.6;
}

/* Buttons */

div[data-testid="stButton"] button,
div[data-testid="stFormSubmitButton"] button {
    border-radius: 9px;
    background: #28594b !important;
    border: 1px solid #28594b !important;
    color: #ffffff !important;
    font-weight: 600;
    min-height: 42px;
}

div[data-testid="stButton"] button *,
div[data-testid="stFormSubmitButton"] button * {
    color: #ffffff !important;
}

div[data-testid="stButton"] button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    background: #20483d !important;
    border-color: #20483d !important;
}

/* Inputs */

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border-radius: 9px;
    color: #1e2933 !important;
    -webkit-text-fill-color: #1e2933 !important;
    background: #ffffff !important;
}

input::placeholder,
textarea::placeholder {
    color: #667085 !important;
    -webkit-text-fill-color: #667085 !important;
}

/* Answer area */

.answer {
    background: #ffffff;
    color: #1e2933 !important;
    border: 1px solid #e1e9e5;
    border-left: 4px solid #28594b;
    border-radius: 10px;
    padding: 17px 19px;
    line-height: 1.75;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.small-note {
    font-size: 11px;
    color: #667085 !important;
    line-height: 1.55;
}

/* Mobile layout */

@media screen and (max-width: 768px) {

    .block-container {
        padding: 1rem 1rem 2rem !important;
        max-width: 100% !important;
    }

    .hero {
        font-size: 25px;
        line-height: 1.3;
        letter-spacing: -0.5px;
    }

    .hero-copy {
        font-size: 14px;
        line-height: 1.6;
    }

    .brand {
        gap: 10px;
        margin-bottom: 18px;
    }

    .brand-icon {
        width: 38px;
        height: 38px;
    }

    .brand-name {
        font-size: 19px;
    }

    .panel {
        padding: 15px;
        margin-bottom: 12px;
    }

    .panel-title {
        font-size: 15px;
    }

    .panel-copy {
        font-size: 13px;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 0.8rem !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"] > div {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    div[data-testid="stButton"] button,
    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 46px;
    }

    .answer {
        padding: 14px;
        font-size: 14px;
    }

    [data-testid="stSidebar"] {
        min-width: 0;
    }
}

/* Hide Streamlit branding */

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# --------------------------------------------------
# DATABASE AND SESSION STATE
# --------------------------------------------------

init_db()

for key, default in [
    ("last_topic", ""),
    ("last_response", "")
]:
    if key not in st.session_state:
        st.session_state[key] = default


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

PAGES = [
    "Voice Assistant",
    "Government Schemes",
    "Application Guide",
    "Grievance Assistant",
    "Farmer Assistant",
    "Activity"
]

MODULES = {
    "Voice Assistant": "general",
    "Government Schemes": "schemes",
    "Application Guide": "application",
    "Grievance Assistant": "grievance",
    "Farmer Assistant": "farmer"
}


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("### 🇮🇳 Sahaaya AI")
    st.caption("Multilingual citizen assistance")

    language = st.selectbox(
        "Response language",
        list(LANGUAGES.keys()),
        index=0
    )

    lang_code = LANGUAGES[language]

    st.divider()

    page = st.radio(
        "Choose a service",
        PAGES
    )

    st.divider()

    st.markdown("**Voice languages**")
    st.caption("తెలుగు · हिन्दी · English · தமிழ்")

    ok, status = get_api_status()

    if ok:
        st.success("Gnani API key detected")
    else:
        st.warning("Gnani API key not configured")
        st.caption(status)

    st.markdown(
        '<div class="small-note">'
        'Guidance prototype only. Verify current details '
        'with the relevant department.'
        '</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    '<div class="brand">'
    '<div class="brand-icon">S</div>'
    '<div>'
    '<div class="brand-name">SAHAAYA AI</div>'
    '<div class="brand-sub">'
    'Multilingual · Voice-first · Citizen services'
    '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="eyebrow">'
    'PUBLIC SERVICE ACCESS · VOICE FIRST'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero">How can we help you today?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-copy">'
    'Ask about government schemes, application steps, '
    'public grievances or farming information. Speak or type '
    'in Telugu, Hindi, English or Tamil. Sahaaya can read '
    'the answer aloud.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# RESPONSE FUNCTION
# --------------------------------------------------

def respond(query, module):

    query = query.strip()

    if not query:
        st.warning("Please enter a question or record your voice.")
        return

    with st.spinner("Preparing a clear answer..."):

        answer, sources = answer_query(
            query,
            language,
            module,
            context=st.session_state.last_topic
        )

    st.session_state.last_topic = (
        query if len(query) > 10
        else (st.session_state.last_topic or query)
    )

    st.session_state.last_response = answer

    st.markdown("#### Sahaaya response")

    st.markdown(
        '<div class="answer">'
        + html.escape(str(answer))
        + '</div>',
        unsafe_allow_html=True
    )

    if sources:

        st.markdown("**Official reference links**")

        for title, url in sources:
            st.markdown(f"- [{title}]({url})")

    try:

        audio = synthesize_speech(answer, lang_code)

        st.audio(
            audio,
            format="audio/wav"
        )

        st.caption("Spoken response · Gnani Timbre")

    except Exception as exc:

        st.info(
            "The text answer is ready, but speech playback failed. "
            "Check Gnani TTS configuration."
        )

        with st.expander("Technical detail"):
            st.code(str(exc))

    save_interaction(
        module,
        language,
        query,
        answer
    )


# --------------------------------------------------
# VOICE INPUT
# --------------------------------------------------

def voice_input(module):

    st.markdown("#### Ask by voice")

    st.caption(
        "Record in your selected language. Gnani Prisma "
        "transcribes your speech; Sahaaya answers and reads "
        "the response aloud."
    )

    audio = st.audio_input(
        "Record your question",
        key=f"audio_{module}"
    )

    if audio is not None:

        if st.button(
            "Transcribe and answer",
            key=f"voice_go_{module}",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner("Recognising your speech..."):

                    transcript, detected = transcribe_audio(
                        audio.getvalue(),
                        lang_code
                    )

                st.success("Recognised: " + transcript)

                st.caption(
                    "Detected language: "
                    + str(detected or language)
                )

                respond(transcript, module)

            except Exception as exc:

                st.error(
                    f"Voice processing failed: {exc}"
                )

    st.divider()


# --------------------------------------------------
# TYPED INPUT
# --------------------------------------------------

def typed_input(
    module,
    label="Type your question",
    placeholder="Type your question here..."
):

    value = st.text_area(
        label,
        placeholder=placeholder,
        height=100,
        key=f"typed_{module}"
    )

    if st.button(
        "Get answer",
        key=f"typed_go_{module}",
        type="primary",
        use_container_width=True
    ):

        respond(value, module)


# --------------------------------------------------
# VOICE ASSISTANT PAGE
# --------------------------------------------------

if page == "Voice Assistant":

    left, right = st.columns(
        [1.35, 0.85],
        gap="large"
    )

    with left:

        st.markdown(
            '<div class="panel">'
            '<div class="panel-title">Talk to Sahaaya</div>'
            '<div class="panel-copy">'
            'Ask naturally about schemes, applications, '
            'complaints or farming support.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        voice_input("general")

        typed_input(
            "general",
            "Or type your question",
            "Example: Explain PM-KISAN eligibility and how to apply."
        )

    with right:

        st.markdown(
            '<div class="panel">'
            '<div class="panel-title">What you can ask</div>'
            '<div class="panel-copy">'
            'Government schemes<br><br>'
            'Application guidance<br><br>'
            'Grievance drafting<br><br>'
            'Farmer support'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel">'
            '<div class="panel-title">Accessible by design</div>'
            '<div class="panel-copy">'
            'A simple voice-first experience for citizens who '
            'find long forms and English-only websites difficult '
            'to use.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


# --------------------------------------------------
# GOVERNMENT SCHEMES PAGE
# --------------------------------------------------

elif page == "Government Schemes":

    st.markdown(
        '<div class="panel">'
        '<div class="panel-title">Government Scheme Finder</div>'
        '<div class="panel-copy">'
        'Explore Central Government and Telangana schemes. '
        'Ask what a scheme does, who may qualify, benefits, '
        'documents and application steps.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    voice_input("schemes")

    typed_input(
        "schemes",
        "What support are you looking for?",
        "Example: Explain PM-KISAN and Rythu Bharosa for a farmer in Telangana."
    )


# --------------------------------------------------
# APPLICATION GUIDE PAGE
# --------------------------------------------------

elif page == "Application Guide":

    st.markdown(
        '<div class="panel">'
        '<div class="panel-title">Application Guide</div>'
        '<div class="panel-copy">'
        'Understand the steps before visiting a portal or '
        'service centre. Exact documents depend on the current '
        'official notification.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    voice_input("application")

    scheme = st.text_input(
        "Scheme or service name",
        placeholder="Example: Telangana ePASS / PM-KISAN"
    )

    details = st.text_area(
        "What do you need help with?",
        placeholder="Explain eligibility, application steps and documents.",
        height=90
    )

    if st.button(
        "Prepare application guidance",
        type="primary",
        use_container_width=True
    ):

        respond(
            f"{scheme}. {details}".strip(),
            "application"
        )


# --------------------------------------------------
# GRIEVANCE ASSISTANT PAGE
# --------------------------------------------------

elif page == "Grievance Assistant":

    st.markdown(
        '<div class="panel">'
        '<div class="panel-title">Grievance Assistant</div>'
        '<div class="panel-copy">'
        'Describe a public-service issue. Sahaaya prepares '
        'a complaint draft for your review; it does not submit it.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    voice_input("grievance")

    with st.form("grievance_form"):

        issue = st.text_area(
            "Describe the problem",
            placeholder="Example: Drinking water has not been supplied for three days.",
            height=100
        )

        location = st.text_input(
            "Village / town / ward / district"
        )

        department = st.selectbox(
            "Related service",
            [
                "Water supply",
                "Roads",
                "Electricity",
                "Sanitation",
                "Ration / PDS",
                "Agriculture",
                "Other / Not sure"
            ]
        )

        submitted = st.form_submit_button(
            "Create complaint draft",
            type="primary"
        )

    if submitted:

        if not issue.strip() or not location.strip():

            st.warning(
                "Please provide the problem and its location."
            )

        else:

            prompt = (
                f"Draft a complaint in {language}. "
                f"Department: {department}. "
                f"Problem: {issue}. "
                f"Location: {location}. "
                "Include a subject, facts and requested action. "
                "Do not invent details."
            )

            with st.spinner("Preparing complaint draft..."):

                draft, sources = answer_query(
                    prompt,
                    language,
                    "grievance"
                )

            st.markdown("#### Review your complaint")

            st.text_area(
                "Complaint draft — edit before submitting",
                draft,
                height=220
            )

            try:

                st.audio(
                    synthesize_speech(draft, lang_code),
                    format="audio/wav"
                )

            except Exception:

                st.caption(
                    "Draft is ready as text; speech could not be generated."
                )

            st.caption(
                "Draft only. Review and submit it yourself through "
                "the relevant official channel."
            )

            save_grievance(
                language,
                department,
                location,
                issue,
                draft
            )

            st.markdown(
                "[CPGRAMS](https://pgportal.gov.in/) · "
                "[Telangana MeeSeva](https://ts.meeseva.telangana.gov.in/)"
            )


# --------------------------------------------------
# FARMER ASSISTANT PAGE
# --------------------------------------------------

elif page == "Farmer Assistant":

    st.markdown(
        '<div class="panel">'
        '<div class="panel-title">Farmer Assistant</div>'
        '<div class="panel-copy">'
        'Ask about agricultural schemes, crop insurance, credit, '
        'irrigation, weather resources or crop concerns. For '
        'diagnosis and chemical decisions, consult a local KVK '
        'or agriculture officer.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    voice_input("farmer")

    crop = st.text_input(
        "Crop (optional)",
        placeholder="Paddy, cotton, chilli"
    )

    district = st.text_input(
        "District (optional)",
        placeholder="Warangal"
    )

    question = st.text_area(
        "Your farming question",
        placeholder="Describe crop stage, symptoms or the support you need.",
        height=95
    )

    if st.button(
        "Get farming guidance",
        type="primary",
        use_container_width=True
    ):

        if question.strip():

            respond(
                f"Crop: {crop}. District: {district}. "
                f"Question: {question}. "
                "Do not prescribe pesticides or exact chemical doses.",
                "farmer"
            )

        else:

            st.warning(
                "Please enter your farming question."
            )


# --------------------------------------------------
# ACTIVITY PAGE
# --------------------------------------------------

elif page == "Activity":

    st.markdown(
        '<div class="panel">'
        '<div class="panel-title">Recent activity</div>'
        '<div class="panel-copy">'
        'Questions and answers saved locally on this device.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    rows = recent_interactions(30)

    if rows:

        for row in rows:

            with st.expander(
                f"{row[1]} · {row[2]} · {row[5]}"
            ):

                st.markdown("**Question**")
                st.write(row[3])

                st.markdown("**Response**")
                st.write(row[4])

    else:

        st.info("No interactions yet.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    '<div class="small-note">'
    'Sahaaya AI is an independent prototype, not an official '
    'government website. It does not determine eligibility, '
    'approve applications or submit grievances. Verify important '
    'details with the relevant department. Do not share OTPs, '
    'passwords, Aadhaar numbers or bank details in chat.'
    '</div>',
    unsafe_allow_html=True
)
