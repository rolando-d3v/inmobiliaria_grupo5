# 🔗 Python UTEC - Grupo 5: Automatización de reportes comerciales con Python en la industria inmobiliaria

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/built%20with-streamlit-orange)
![License](https://img.shields.io/badge/license-MIT-green)

This project was developed by **Grupo 1** from **UTEC** as part of a Python programming course. It provides an intuitive tool for generating deep links, QR codes, and dynamic promotional descriptions — ideal for marketing and e-commerce use cases.


---

## 🚀 Features

- ✅ Generate product **deep links** with tracking
- ✅ Create dynamic **marketing descriptions** from product images or data
- ✅ Produce and store **QR codes** for campaigns
- ✅ Save and organize all outputs in a structured format

---

## 📸 Screenshots

| Interface | QR Code Output | Text Generation |
|----------|----------------|------------------|
| ![UI Screenshot](img/screenshot_ui.png) | ![QR Output](img/screenshot_qr.png) | ![Text Output](img/screenshot_text.png) |


---

## 🗂 Project Structure

```
├── ui.py                    # UI interface using Streamlit
├── main.py                  # Main process
├── generate_deeplink.py     # Deep link generation logic
├── generate_description.py  # Description creation logic from image
├── generate_qr.py           # QR code creation logic
├── generate_text.py         # Utility to assemble content
├── content/                 # Input content/data, CSV to search data
├── img/                     # Bills to scan
├── qr/                      # Stored QR data
├── requirements.txt         # Python dependencies
```

---

## 🧪 Setup Instructions (with Virtual Environment in VS Code)

Follow these steps to set up and activate a virtual environment in your project using Visual Studio Code with the `Command Prompt` terminal:

### 1. Open the terminal in VS Code
- Open VS Code.
- Use the shortcut: `Ctrl + ` (backtick) or go to **View > Terminal**.
- Make sure you are using `Command Prompt` as the terminal. You can switch terminals from the dropdown menu in the top-right corner of the terminal panel.

### 2. Validate Python installation
Make sure you have **Python 3.8+** installed.

```bash
python
```

### 3. Create the virtual environment
Run the following command in the root of your project:

```bash
python -m venv venv
```
This will create a folder named venv containing your virtual environment.


### 4. Activate the virtual environment
In Command Prompt, run:

```bash
venv\Scripts\activate
```

### 5. Install dependencies
After activation, install the required packages in the next step.

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Use

### 1. Get a Free API Key from Groq

Create your API keys from your free account

🔗 [Groq Console – API Keys](https://console.groq.com/keys)

### 2. Create a `.env` File

Create your `.env` file with your `GROQ_API_KEY` variable. 

```bash
GROQ_API_KEY="your_api_key"
```

### 3. Launch the App

Run the main script:

```bash
streamlit run ui.py
```

You will be prompted to input or confirm product data. The tool will:

1. ✅ Generate a short deep link  
2. ✅ Create marketing text  
3. ✅ Produce and save a QR code  

---

## 📁 Output

- QR code is saved in the `qr/` directory  
- Log stored in `yape_scan.log`
- Dynamic text outputs are printed or stored depending on the function  

---

## 👨‍👩‍👧‍👦 Team Members

- Carlos Loyola [@cloyola](https://github.com/cloyola)  
- Diego Nasra  
- Ana Cecilia Zegarra 
- Brenda Zambrano  
- Mónica Saldías  
- Nicolás Nugent  