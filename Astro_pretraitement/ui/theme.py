import streamlit as st
import base64
from pathlib import Path



def load_css():

    css_path = Path("ui/style.css")


    if css_path.exists():

        st.markdown(
            f"""
            <style>

            {css_path.read_text(
                encoding="utf-8"
            )}

            </style>
            """,

            unsafe_allow_html=True
        )



def set_background():

    img_path = Path("ui/background.jpg")


    if not img_path.exists():

        return


    with open(
        img_path,
        "rb"
    ) as f:

        encoded = base64.b64encode(
            f.read()
        ).decode()



    st.markdown(
        f"""
        <style>

        .stApp {{

            background-image:

            linear-gradient(
                rgba(0,0,0,0.25),
                rgba(0,0,0,0.25)
            ),

            url(
            "data:image/jpg;base64,{encoded}"
            );


            background-size: cover;

            background-position:center;

            background-attachment:fixed;

        }}


        /* Transparence des blocs Streamlit */

        .block-container {{

            background-color:
            rgba(0,0,0,0.15);

            border-radius:15px;

            padding:2rem;

        }}


        </style>
        """,

        unsafe_allow_html=True
    )



def load_theme():

    load_css()

    set_background()