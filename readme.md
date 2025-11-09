# 🔗 Python UTEC - Grupo 5: Automatización de reportes comerciales con Python en la industria inmobiliaria

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/built%20with-streamlit-orange)
![License](https://img.shields.io/badge/license-MIT-green)

Este proyecto fue desarrollado por el **Grupo 5** de **UTEC** como parte de un curso de programación en Python. Este proyecto propone desarrollar una solución en Python que integre automatización de datos y técnicas de aprendizaje automático, con el objetivo de estimar la probabilidad de conversión de leads y generar reportes comerciales confiables.

---

## 🚀 Características

- ✅ Generar enlaces profundos **con seguimiento**
- ✅ **Flujo de datos reproducible**: ingesta programada de fuentes operativas (por canal y proyecto), limpieza, estandarización y anonimización bajo buenas prácticas.
- ✅ **Modelado supervisado**: construcción de un conjunto de variables, entrenamiento de modelos base y avanzados .
- ✅ **Entrega accionable**: un dashboard interactivo que muestre la data actualizada, predicciones por lead y KPI operativos para priorización diaria, además de reportes automáticos con frecuencia definida.

---

## 📸 Capturas de pantalla

| Interfaz | QR Code Output | Text Generation |
|----------|----------------|------------------|
| ![UI Screenshot](img/screenshot_ui.png) | ![QR Output](img/screenshot_qr.png) | ![Text Output](img/screenshot_text.png) |


---

## 🗂  Estructura del Proyecto

```
├── ui.py                    # UI interface using Streamlit
├── main.py                  # Main process
├── generate_text.py         # Utility to assemble content
├── img/                     # imagenes del proyecto
├── requirements.txt         # dependencias del proyecto
```

---

## 🧪 Instrucciones de Instalación (con Entorno Virtual en VS Code)

Siga estos pasos para configurar y activar un entorno virtual en su proyecto usando Visual Studio Code con el terminal `Command Prompt`:

### 1. Abrir el terminal en VS Code
- Abra VS Code.
- Use the shortcut: `Ctrl + ` (backtick) or go to **View > Terminal**.
- Make sure you are using `Command Prompt` as the terminal. You can switch terminals from the dropdown menu in the top-right corner of the terminal panel.

### 2. Validate Python installation
Make sure you have **Python 3.8+** installed.

```bash
python
```

### 3. Crear el entorno virtual
Ejecutar el siguiente comando en la raíz de su proyecto:

```bash
python -m venv venv
```
This will create a folder named venv containing your virtual environment.


### 4. Activar el entorno virtual
En Command Prompt, ejecutar:

```bash
venv\Scripts\activate
```

### 5. Instalar dependencias
Después de activar, instalar los paquetes requeridos en el siguiente paso.

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Use

### 1. Obtener una clave API gratuita de Groq

Cree sus claves de API desde su cuenta gratuita

🔗 [Groq Console – API Keys](https://console.groq.com/keys)

### 2. Crear un archivo `.env`

Cree su archivo `.env` con su variable `GROQ_API_KEY`. 

```bash
GROQ_API_KEY="your_api_key"
```

### 3. Ejecute la App con:

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