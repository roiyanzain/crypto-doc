import os
import streamlit as st
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad

def decrypt_file(uploaded_file, password):
    # Create a key from the password
    key = SHA256.new(password.encode('utf-8')).digest()

    # Read the encrypted data from the uploaded file
    encrypted_data = uploaded_file.read()

    # The first 16 bytes of the encrypted data is the IV
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    # Initialize AES cipher with the key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # Decrypt the ciphertext
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return plaintext

def decryptPage():
    # Ask the user for the decryption password
    password = st.text_input("Enter decryption password:", type="password")

    # Create a key from the password
    key = SHA256.new(password.encode('utf-8')).digest()

    # Ask the user to upload the encrypted .docx file
    uploaded_file = st.file_uploader("Choose an encrypted .docx file", type=["txt", "xls", "csv", "docx"])

    if uploaded_file is not None:
        # Get the file extension
        file_extension = os.path.splitext(uploaded_file.name)[1]

        # Decrypt the file content
        plaintext = decrypt_file(uploaded_file, password)

        # Write the decrypted content to a new file
        decrypted_file_name = 'decrypted_document' + file_extension
        with open(decrypted_file_name, 'wb') as f:
            f.write(plaintext)

        st.success("File decrypted successfully!")

        # Add a download button
        st.download_button(
            label="Download decrypted file",
            data=plaintext,
            file_name='decrypted_document' + file_extension,
            mime='application/octet-stream'
        )