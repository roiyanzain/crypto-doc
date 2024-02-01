import os
import streamlit as st
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad

def encryptPage():
    
    # Input password untuk user
    password = st.text_input("Enter encryption password", type="password")

    # Membuat key dari password yang telah diinputkan user
    key = SHA256.new(password.encode('utf-8')).digest()

    # Upload file user
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "docx", "xls", "csv"])
    if uploaded_file is not None:

        # Dapatkan ekstensi filenya
        file_extension = os.path.splitext(uploaded_file.name)[1]

        # Baca content atau isi filenya
        plaintext = uploaded_file.read()

        # Inisialisasi AES Chiper dengan Key
        cipher = AES.new(key, AES.MODE_CBC)

        # Enkripsi isi dari file yang diupload
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        # Kombinasikan IV dengan Chipertext
        encrypted_data = cipher.iv + ciphertext

        # Tulis file yang telah dienkripsi ke file baru
        encrypted_file_name = 'encrypted_document' + file_extension
        with open(encrypted_file_name, 'wb') as f:
            f.write(encrypted_data)

        st.success("File encrypted successfully!")

        # Tambahkan tombol unduhan
        st.download_button(
            label="Download encrypted file",
            data=encrypted_data,
            file_name='encrypted_document' + file_extension,
            mime='application/octet-stream'
        )