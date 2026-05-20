import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
        /* Sidebar border */
        [data-testid="stSidebar"] {
            border-right: 2px solid #000926 !important;
        }

        /* Input boxes border (text_input, number_input, text_area, selectbox) */
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stSelectbox"] > div > div {
            border: 2px solid #000926 !important;
            border-radius: 6px !important;
        }

        /* File uploader box */
        [data-testid="stFileUploader"] > div {
            border: 2px solid #000926 !important;
            border-radius: 6px !important;
        }

        /* Focus state - highlight when clicked */
        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border: 2px solid #000926 !important;
            box-shadow: 0 0 0 2px rgba(0, 9, 38, 0.2) !important;
        }

        /* Remove slider min/max label borders */
        .stSlider [data-testid="stTickBarMin"],
        .stSlider [data-testid="stTickBarMax"] {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)