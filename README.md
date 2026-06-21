💊 Medicine Safety Assistant
A Python-based web application that helps users verify and search medicine information by extracting text directly from prescription images. Built as part of academic learning to strengthen logic-building and deployment workflow skills.
🔍 Overview
Medicine Safety Assistant takes a prescription image as input, extracts the medicine names using OCR, and matches them against a medicine database using a custom match-score algorithm — helping users quickly verify what's been prescribed.
✨ Features
Prescription OCR & Text Extraction — Reads medicine names directly from prescription images
Medicine Search with Match Score Logic — Returns the closest matching medicines with a confidence/match score
CSV-Based Data Handling — Lightweight, file-based medicine database (no external DB required)
Simple Web Interface — Built with Streamlit for an interactive, easy-to-use experience
Live Deployment — Hosted and accessible online
🛠️ Tech Stack
Category
Tools
Language
Python
Web Framework
Streamlit
OCR
pytesseract
Image Processing
Pillow
Data Storage
CSV
Version Control
Git, GitHub
