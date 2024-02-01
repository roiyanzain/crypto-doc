import os
import streamlit as st
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad

def encryptPage():
    # Ask the user for a password
    password = st.text_input("Enter encryption password:", type="password")

    # Create a key from the password
    key = SHA256.new(password.encode('utf-8')).digest()

    # Ask the user to upload a .docx file
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "xls", "csv"])
    if uploaded_file is not None:

        # Get the file extension
        file_extension = os.path.splitext(uploaded_file.name)[1]

        # Read the file content
        plaintext = uploaded_file.read()

        # Initialize AES cipher with the key
        cipher = AES.new(key, AES.MODE_CBC)

        # Encrypt the file content
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        # Combine the IV and the ciphertext
        encrypted_data = cipher.iv + ciphertext

        # Write the encrypted content to a new file
        encrypted_file_name = 'encrypted_document' + file_extension
        with open(encrypted_file_name, 'wb') as f:
            f.write(encrypted_data)

        st.success("File encrypted successfully!")

        # Add a download button
        st.download_button(
            label="Download encrypted file",
            data=encrypted_data,
            file_name='encrypted_document' + file_extension,
            mime='application/octet-stream'
        )