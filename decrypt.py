import os
import streamlit as st
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad

def decrypt_file(uploaded_file, password):
    
    # Buat key dari password
    key = SHA256.new(password.encode('utf-8')).digest()

    # Baca data enkripsi dari file yang diupload
    encrypted_data = uploaded_file.read()

    # 16 byte pertama merupakan IV
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    # Inisialisasi AES Chiper dengan key dan IV
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # Dekripsi chipertext
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return plaintext

def decryptPage():
    # Inputkan password dari file yang didekripsi
    password = st.text_input("Enter decryption password:", type="password")

    # Upload file user
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "xls", "csv", "docx"])

    if uploaded_file is not None:
        # Dapatkan ekstensi file yang diupload
        file_extension = os.path.splitext(uploaded_file.name)[1]

        # Dekripsi konten dari file
        plaintext = decrypt_file(uploaded_file, password)

        # Tulis file yang telah didekripsi ke dalam file baru
        decrypted_file_name = 'decrypted_document' + file_extension
        with open(decrypted_file_name, 'wb') as f:
            f.write(plaintext)

        st.success("File decrypted successfully!")

        # Tambahkan tombol unduhan
        st.download_button(
            label="Download decrypted file",
            data=plaintext,
            file_name='decrypted_document' + file_extension,
            mime='application/octet-stream'
        )