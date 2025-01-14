import nltk
nltk.download('punkt')
nltk.download('stopwords')

import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Load the vectorizer and model
tk = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("model.pkl", 'rb'))

# Language dictionary with Indian languages
languages = {
    "English": {
        "title": "SMS Spam Detection Application",
        "description": "This is a Machine Learning project to identify SMS as spam or ham.",
        "enter_sms": "Enter the SMS:",
        "predict_button": "Predict",
        "clear_button": "Clear",
        "spam_result": "Spam",
        "not_spam_result": "Not Spam",
    },
    "Hindi": {
        "title": "एसएमएस स्पैम पहचान एप्लिकेशन",
        "description": "यह एक मशीन लर्निंग प्रोजेक्ट है जो एसएमएस को स्पैम या हैम के रूप में पहचानता है।",
        "enter_sms": "एसएमएस दर्ज करें:",
        "predict_button": "भविष्यवाणी करें",
        "clear_button": "साफ़ करें",
        "spam_result": "स्पैम",
        "not_spam_result": "स्पैम नहीं",
    },
    "Tamil": {
        "title": "எஸ்.எம்.எஸ் ஸ்பாம் கண்டறிதல் பயன்பாடு",
        "description": "இது ஒரு மெஷின் லெர்னிங் திட்டம், இது எஸ்.எம்.எஸ்-ஐ ஸ்பாம் அல்லது ஹாம் என அடையாளம் காண்கிறது.",
        "enter_sms": "எஸ்.எம்.எஸ் உள்ளிடவும்:",
        "predict_button": "கணிப்பு செய்க",
        "clear_button": "அழி",
        "spam_result": "ஸ்பாம்",
        "not_spam_result": "ஸ்பாம் அல்ல",
    },
    "Telugu": {
        "title": "ఎస్ఎంఎస్ స్పామ్ గుర్తింపు అనువర్తనం",
        "description": "ఇది ఒక మెషీన్ లెర్నింగ్ ప్రాజైక్టు, ఇది ఎస్ఎంఎస్ ను స్పామ్ లేదా హామ్ గా గుర్తిస్తుంది.",
        "enter_sms": "ఎస్ఎంఎస్ నమోదు చేయండి:",
        "predict_button": "భవిష్యవాణి చేయండి",
        "clear_button": "తొలగించు",
        "spam_result": "స్పామ్",
        "not_spam_result": "స్పామ్ కాదు",
    },
    "Kannada": {
        "title": "ಎಸ್‌ಎಂಎಸ್ ಸ್ಪಾಮ್ ಗುರುತಿಸುವ ಅಪ್ಲಿಕೇಶನ್",
        "description": "ಇದು ಎಂಎಲ್ ಪ್ರಾಜೆಕ್ಟ್ ಆಗಿದ್ದು, ಇದು ಎಸ್‌ಎಂಎಸ್ ಅನ್ನು ಸ್ಪಾಮ್ ಅಥವಾ ಹ್ಯಾಮ್ ಎಂದು ಗುರುತಿಸುತ್ತದೆ.",
        "enter_sms": "ಎಸ್‌ಎಂಎಸ್ ನಮೂದಿಸಿ:",
        "predict_button": "ಭವಿಷ್ಯವಾಣಿ ಮಾಡಿ",
        "clear_button": "ತುಂಬಿಸಿ",
        "spam_result": "ಸ್ಪಾಮ್",
        "not_spam_result": "ಸ್ಪಾಮ್ ಅಲ್ಲ",
    }
}

# Initialize session state for SMS input and selected language
if "sms_input" not in st.session_state:
    st.session_state.sms_input = ""
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"
if "clear_sms" not in st.session_state:
    st.session_state.clear_sms = False  # Flag to clear input

# Language selection
language = st.sidebar.selectbox("Select Language", options=list(languages.keys()))
st.session_state.selected_language = language

# Get the translations for the selected language
current_lang = languages[st.session_state.selected_language]

# Clear input function
def clear_input():
    # Set the flag to clear the SMS input
    st.session_state.clear_sms = True

# UI Components
st.title(current_lang["title"])
st.write(current_lang["description"])

# Check if clear flag is set
if st.session_state.clear_sms:
    st.session_state.sms_input = ""  # Clear the input
    st.session_state.clear_sms = False  # Reset the flag

# Input field
input_sms = st.text_input(current_lang["enter_sms"], value=st.session_state.sms_input, key="sms_input")

# Place Predict and Clear buttons next to each other with minimal space
col1, col2 = st.columns([4, 1])  # Columns with ratio 4:1 to bring buttons closer
with col1:
    if st.button(current_lang["predict_button"]):
        # 1. Preprocess
        transformed_sms = transform_text(input_sms)
        # 2. Vectorize
        vector_input = tk.transform([transformed_sms])
        # 3. Predict
        result = model.predict(vector_input)[0]
        # 4. Display
        if result == 1:
            st.header(current_lang["spam_result"])
        else:
            st.header(current_lang["not_spam_result"])

with col2:
    if st.button(current_lang["clear_button"]):
        clear_input()

# Instructions on how to use the app
st.sidebar.subheader("How to use")
st.sidebar.write("1. Enter your SMS text or upload a file.")
st.sidebar.write("2. Click 'Predict' to check if it's spam or not.")

# Add rating slider in the sidebar
st.sidebar.subheader("Rating")
rating = st.sidebar.slider("How accurate was this prediction?", min_value=1, max_value=5)
st.sidebar.write(f"You rated the prediction: {rating}/5")
