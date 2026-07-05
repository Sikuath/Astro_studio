import streamlit as st


def fits_upload(label):
    """
    Upload a FITS file (Streamlit wrapper)
    """
    return st.file_uploader(label, type=["fit", "fits"])
