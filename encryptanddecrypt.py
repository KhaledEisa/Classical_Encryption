import string
import customtkinter as ctk
from tkinter import messagebox
import numpy as np

# Initialize customtkinter appearance
ctk.set_appearance_mode("System")  # Can be toggled
ctk.set_default_color_theme("blue")

class CipherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Encryption/Decryption GUI")
        self.geometry("800x700")

        self.theme = "light"

        self.title_label = ctk.CTkLabel(self, text="Welcome to Encryption/Decryption World",
                                        font=("Helvetica", 28, "bold"))
        self.title_label.pack(pady=20)

        self.algorithm_option = ctk.CTkOptionMenu(self, values=["Caesar", "Hill", "Vigenère", "Playfair", "Vernam"])
        self.algorithm_option.pack(pady=10)

        self.input_entry = ctk.CTkEntry(self, placeholder_text="Enter text", width=500, height=50, font=("Helvetica", 16))
        self.input_entry.pack(pady=10)

        self.key_entry = ctk.CTkEntry(self, placeholder_text="Enter key", width=500, height=50, font=("Helvetica", 16))
        self.key_entry.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, width=600, height=200, font=("Helvetica", 14))
        self.output_box.pack(pady=10)

        self.encrypt_button = ctk.CTkButton(self, text="Encrypt", command=self.encrypt_text, width=200, height=50)
        self.encrypt_button.pack(pady=5)

        self.decrypt_button = ctk.CTkButton(self, text="Decrypt", command=self.decrypt_text, width=200, height=50)
        self.decrypt_button.pack(pady=5)

        self.theme_button = ctk.CTkButton(self, text="Toggle Theme", command=self.toggle_theme, width=200, height=40)
        self.theme_button.pack(pady=20)

    def toggle_theme(self):
        if self.theme == "light":
            ctk.set_appearance_mode("dark")
            self.theme = "dark"
        else:
            ctk.set_appearance_mode("light")
            self.theme = "light"

    def encrypt_text(self):
        text = self.input_entry.get()
        key = self.key_entry.get()
        algo = self.algorithm_option.get()

        try:
            if algo == "Caesar":
                result = caesar_cipher(text, int(key))
            elif algo == "Hill":
                result = hill_cipher(text, key, encrypt=True)
            elif algo == "Vigenère":
                result = vigenere_cipher(text, key)
            elif algo == "Playfair":
                result = playfair_cipher(text, key)
            elif algo == "Vernam":
                result = vernam_cipher(text, key)
            else:
                result = "Unknown algorithm"
        except Exception as e:
            result = f"Error: {str(e)}"

        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", result)

    def decrypt_text(self):
        text = self.input_entry.get()
        key = self.key_entry.get()
        algo = self.algorithm_option.get()

        try:
            if algo == "Caesar":
                result = caesar_cipher(text, int(key), encrypt=False)
            elif algo == "Hill":
                result = hill_cipher(text, key, encrypt=False)
            elif algo == "Vigenère":
                result = vigenere_cipher(text, key, encrypt=False)
            elif algo == "Playfair":
                result = playfair_cipher(text, key, encrypt=False)
            elif algo == "Vernam":
                result = vernam_cipher(text, key)
            else:
                result = "Unknown algorithm"
        except Exception as e:
            result = f"Error: {str(e)}"

        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", result)

# ---------------------- CIPHER ALGORITHMS ----------------------

def caesar_cipher(text, shift, encrypt=True):
    result = ""
    shift = shift % 26
    if not encrypt:
        shift = -shift
    for char in text:
        if char.isalpha():
            start = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def generate_playfair_square(key):
    key = "".join(sorted(set(key.upper()), key=lambda x: key.index(x)))
    alphabet = string.ascii_uppercase.replace("J", "")
    square = key + "".join(char for char in alphabet if char not in key)
    return [square[i:i + 5] for i in range(0, 25, 5)]

def playfair_cipher(text, key, encrypt=True):
    square = generate_playfair_square(key)
    text = text.replace("J", "I").upper()
    
    # Prepare text pairs
    formatted_text = []
    i = 0
    while i < len(text):
        if i == len(text) - 1:
            formatted_text.append(text[i] + "X")
            i += 1
        elif text[i] == text[i+1]:
            formatted_text.append(text[i] + "X")
            i += 1
        else:
            formatted_text.append(text[i] + text[i+1])
            i += 2

    def find_position(char):
        for i, row in enumerate(square):
            if char in row:
                return i, row.index(char)
        return None

    result = []
    for pair in formatted_text:
        if len(pair) == 1:
            pair += "X"
        r1, c1 = find_position(pair[0])
        r2, c2 = find_position(pair[1])

        if r1 == r2:
            if encrypt:
                result.append(
                    square[r1][(c1 + 1) % 5] + square[r2][(c2 + 1) % 5]
                )
            else:
                result.append(
                    square[r1][(c1 - 1) % 5] + square[r2][(c2 - 1) % 5]
                )
        elif c1 == c2:
            if encrypt:
                result.append(
                    square[(r1 + 1) % 5][c1] + square[(r2 + 1) % 5][c2]
                )
            else:
                result.append(
                    square[(r1 - 1) % 5][c1] + square[(r2 - 1) % 5][c2]
                )
        else:
            result.append(square[r1][c2] + square[r2][c1])

    return "".join(result)

def hill_cipher(text, key, encrypt=True):
    # Convert key to matrix
    key = key.replace(" ", "").upper()
    size = int(len(key)**0.5)
    if size * size != len(key):
        raise ValueError("Key length must be a perfect square (e.g., 4, 9, 16 characters)")
    
    key_matrix = np.array([ord(c) - ord('A') for c in key]).reshape((size, size))
    
    # Check if matrix is invertible
    det = int(round(np.linalg.det(key_matrix)))
    if det == 0:
        raise ValueError("Key matrix is not invertible (determinant is 0)")
    
    # Prepare text
    text = text.upper().replace(" ", "")
    if len(text) % size != 0:
        text += "X" * (size - (len(text) % size))
    
    # If decrypting, compute the inverse of the key matrix
    if not encrypt:
        try:
            det_inv = pow(det, -1, 26)
        except ValueError:
            raise ValueError("Matrix determinant has no modular inverse for modulus 26")
        
        adj = np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
        key_matrix = (det_inv * adj) % 26
    
    # Process text in blocks
    result = ""
    for i in range(0, len(text), size):
        block = np.array([ord(c) - ord('A') for c in text[i:i+size]])
        processed_block = np.dot(key_matrix, block) % 26
        result += "".join(chr(n + ord('A')) for n in processed_block)
    
    return result

def vigenere_cipher(text, key, encrypt=True):
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            shift = ord(key_char.upper()) - ord('A')
            if not encrypt:
                shift = -shift
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
            key_index += 1
        else:
            result += char
    return result

def vernam_cipher(text, key):
    if len(text) != len(key):
        raise ValueError("Text and key must be of equal length for Vernam cipher")
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i]))
    return result

if __name__ == "__main__":
    app = CipherApp()
    app.mainloop()