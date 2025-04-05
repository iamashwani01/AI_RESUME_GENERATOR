# 🧠 AI Resume Generator using Hugging Face

This is a simple web application built with **FastAPI** that allows users to generate a clean, well-formatted resume using **Hugging Face's Mistral-7B model**. The app accepts user input such as name, education, skills, and projects, then generates a professional resume in text format.

---

## 🚀 Features

- Generates resume content with AI (Hugging Face Inference API)
- Clean HTML interface with form input
- Well-formatted output including sections like:
  - Summary
  - Education
  - Skills
  - Projects

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **AI Model**: Mistral-7B via Hugging Face API
- **HTTP Requests**: `requests` library

---

## 🔧 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-resume-generator.git
cd ai-resume-generator
```

### 2. Create a Virtual Environment and Activate It

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variable

Create a `.env` file (if needed), or set your Hugging Face API key in the script directly like shown below:

```python
HUGGINGFACE_API_KEY = "your_huggingface_api_key"
```

You can get your API key from: https://huggingface.co/settings/tokens

### 5. Run the Application

```bash
uvicorn main:app --reload
```

Then open your browser and visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📁 Project Structure

```
.
├── main.py              # Main FastAPI app
├── requirements.txt     # Python dependencies
├── Procfile             # (Optional) For deployment on Railway or Heroku
└── README.md            # Project documentation
```

---

## 📌 Notes

- This project uses Hugging Face's free inference API, which has usage limits.
- No deployment is set up yet, but it can easily be hosted on Railway, Render, or AWS.

---

## 🧑‍💻 Author

**Ashwani Kumar**

---


