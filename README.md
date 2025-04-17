# Classical Cryptography Implementation

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Tkinter](https://img.shields.io/badge/Tkinter-%23EE4C2C.svg?style=for-the-badge&logo=python&logoColor=white)

A Python implementation of classical encryption ciphers with a modern GUI interface, developed as part of a cybersecurity course project.

## Team Members

- Khaled Sherif Eissa (221010359)
- Ahmed Samer (221005991)
- Muhammed Yasser (221006789)
- Hazem Mohamed Gamal (221006586)

**Lecturer:** Dr. Ehab Abousaif  
**TA:** Eng. Youssef Shawky

## Table of Contents

- [Features](#features)
- [Implemented Ciphers](#implemented-ciphers)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Features

- Modern GUI interface using CustomTkinter
- Five classical cipher implementations:
  - Caesar Cipher
  - Hill Cipher
  - Playfair Cipher
  - Vigenère Cipher
  - Vernam Cipher
- Both encryption and decryption functionality
- Error handling and user feedback
- Light/dark mode toggle

## Implemented Ciphers

| Cipher   | Description                                                  |
| -------- | ------------------------------------------------------------ |
| Caesar   | Shifts each letter by a fixed number down the alphabet       |
| Hill     | Uses matrix multiplication for encryption                    |
| Playfair | Encrypts digraphs using a 5×5 grid                           |
| Vigenère | Uses a repeating keyword to shift letters by varying amounts |
| Vernam   | Implements one-time pad using XOR operation with random key  |

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/classical-cryptography.git
   cd classical-cryptography
   ```
