import streamlit as st
from openai import AzureOpenAI


import streamlit as st

# Hide Streamlit menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


api_key = st.secrets["secrets"]["AZURE_OPENAI_API_KEY"]
api_version = st.secrets["secrets"]["AZURE_OPENAI_API_VERSION"]
azure_endpoint = st.secrets["secrets"]["AZURE_OPENAI_ENDPOINT"]
deployment_name = st.secrets["secrets"]["AZURE_OPENAI_DEPLOYMENT_NAME"]


if not api_key or not api_version or not azure_endpoint or not deployment_name:
    st.error("Please set the required secrets in the secrets.toml file.")
    st.stop()


client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)


DEPLOYMENT_NAME = deployment_name



st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .title {
        font-size: 48px;
        font-weight: bold;
        color: #4a90e2;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 24px;
        color: #333333;
        text-align: center;
        margin-bottom: 40px;
    }
    .feature-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .feature-card:hover {
        transform: scale(1.02);
    }
    .feature-title {
        font-size: 20px;
        font-weight: bold;
        color: #4a90e2;
        margin-bottom: 10px;
    }
    .feature-description {
        font-size: 16px;
        color: #555555;
    }
    .sidebar .sidebar-content {
        background-color: #4a90e2;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if "feature" not in st.session_state:
    st.session_state.feature = "Home"


def homepage():
    st.markdown('<div class="title">AI-Powered Multi-Tool App</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your one-stop solution for quizzes, poetry, translations, debugging, studying, and book recommendations!</div>', unsafe_allow_html=True)

   
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎯 Quiz Master"):
            st.session_state.feature = "Quiz Master"
        if st.button("📜 Poetry Generator"):
            st.session_state.feature = "Poetry Generator"
        if st.button("🌍 Language Translator"):
            st.session_state.feature = "Language Translator"

    with col2:
        if st.button("🐞 Code Debugger"):
            st.session_state.feature = "Code Debugger"
        if st.button("📚 Study Assistant"):
            st.session_state.feature = "Study Assistant"
        if st.button("📖 Book Recommender"):
            st.session_state.feature = "Book Recommender"


def quiz_master():
    st.title("🎯 Quiz Master")
    st.write("Generate trivia questions on any topic!")

    topic = st.text_input("Enter a topic:")
    num_questions = st.number_input("Number of questions:", min_value=1, max_value=10, value=5)

    if st.button("Generate Quiz"):
        prompt = f"Generate {num_questions} trivia questions about {topic} with multiple-choice answers."
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful quiz master."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        st.write(response.choices[0].message.content)

    if st.button("Back to Home"):
        st.session_state.feature = "Home"


def poetry_generator():
    st.title("📜 Poetry Generator")
    st.write("Create personalized poems!")

    theme = st.text_input("Enter a theme or emotion:")
    style = st.selectbox("Choose a style:", ["Haiku", "Sonnet", "Free Verse"])

    if st.button("Generate Poem"):
        prompt = f"Write a {style.lower()} poem about {theme}."
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a creative poet."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        st.write(response.choices[0].message.content)

    if st.button("Back to Home"):
        st.session_state.feature = "Home"


def language_translator():
    st.title("🌍 Language Translator")
    st.write("Translate text into different languages!")

    text = st.text_area("Enter text to translate:")
    target_language = st.text_input("Enter target language (e.g., French, Spanish):")

    if st.button("Translate"):
        prompt = f"Translate the following text into {target_language}: {text}"
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a skilled translator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        st.write(response.choices[0].message.content)

    if st.button("Back to Home"):
        st.session_state.feature = "Home"


def code_debugger():
    st.title("🐞 Code Debugger")
    st.write("Fix errors in your code!")

    code = st.text_area("Paste your code here:", height=200)
    error_description = st.text_area("Describe the error or issue you're facing:")

    if st.button("Debug Code"):
        prompt = f"""
        Here is some code:
        ```
        {code}
        ```

        The user is facing the following issue:
        ```
        {error_description}
        ```

        Please:
        1. Identify the error in the code.
        2. Explain the cause of the error.
        3. Provide the corrected code.
        """
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful code debugger."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        st.write(response.choices[0].message.content)

    if st.button("Back to Home"):
        st.session_state.feature = "Home"


def study_assistant():
    st.title("📚 Study Assistant")
    st.write("Get study notes or summaries on any topic!")

    topic = st.text_input("Enter a topic:")
    level = st.selectbox("Choose the level of detail:", ["High-level overview", "In-depth analysis"])

    if st.button("Generate Notes"):
        prompt = f"Provide {level.lower()} study notes on {topic}."
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a knowledgeable study assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        st.write(response.choices[0].message.content)

    if st.button("Back to Home"):
        st.session_state.feature = "Home"


def book_recommender():
    st.title("📖 Book Recommender")
    st.write("Discover your next favorite book!")

    genre = st.text_input("Enter your favorite genre or author:")
    num_recommendations = st.number_input("Number of recommendations:", min_value=1, max_value=10, value=5)

    if st.button("Get Recommendations"):
        prompt = f"Recommend {num_recommendations} books similar to {genre}."
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are a knowledgeable book recommender."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        st.write(response.choices[0].message.content)

    if st.button("Back to Home"):
        st.session_state.feature = "Home"


def main():
    if st.session_state.feature == "Home":
        homepage()
    elif st.session_state.feature == "Quiz Master":
        quiz_master()
    elif st.session_state.feature == "Poetry Generator":
        poetry_generator()
    elif st.session_state.feature == "Language Translator":
        language_translator()
    elif st.session_state.feature == "Code Debugger":
        code_debugger()
    elif st.session_state.feature == "Study Assistant":
        study_assistant()
    elif st.session_state.feature == "Book Recommender":
        book_recommender()

# Run the App
if __name__ == "__main__":
    main()