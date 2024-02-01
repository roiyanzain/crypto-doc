import streamlit as st
from encrypt import encryptPage
from decrypt import decryptPage

st.set_page_config(
    page_title="Crypto Encryption", 
    page_icon=":lock:", 
    layout="wide",
)


# Set up the Streamlit app
st.title('Doc Encryption')
st.header('Encrypt and Decrypt your Documents')

st.write("---")

PAGES = {
    "Encrypt" : encryptPage,
    "Decrypt" : decryptPage
}

st.sidebar.title("Choose Activity")
selection = st.sidebar.radio("I want to", list(PAGES.keys()))

page = PAGES[selection]
page()