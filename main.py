from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from xhtml2pdf import pisa
import requests
import os

app = FastAPI()

# Hugging Face API Details
HUGGINGFACE_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

# Serve HTML Form
@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content="""
    <html>
    <head><title>Resume Generator</title>
                        <style>
      body {
      background: #f4f7f8;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }

    .container {
      background: white;
      padding: 40px 50px;
      border-radius: 15px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
      max-width: 600px;
      width: 100%;
    }

    h2 {
      text-align: center;
      margin-bottom: 30px;
      color: #333;
    }

    label {
      font-weight: bold;
      display: block;
      margin-bottom: 8px;
      margin-top: 20px;
      color: #444;
    }

    input, textarea {
      width: 100%;
      padding: 12px 15px;
      border-radius: 8px;
      border: 1px solid #ccc;
      font-size: 14px;
      resize: vertical;
      background: #fafafa;
      transition: border-color 0.3s;
    }

    input:focus, textarea:focus {
      border-color: #0077ff;
      outline: none;
      background: #fff;
    }

    button {
      margin-top: 30px;
      width: 100%;
      background: #0077ff;
      color: white;
      padding: 15px;
      font-size: 16px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      transition: background 0.3s;
    }

    button:hover {
      background: #005ec2;
    }
    </style>
 </head>
    <body>
  <div class="container">
    <h2>Generate Your Resume</h2>
    <form action="http://127.0.0.1:8000/generate_resume" method="POST">
      <label for="name">Full Name</label>
      <input type="text" id="name" name="name" required>

      <label for="education">Education</label>
      <textarea id="education" name="education" rows="3" required></textarea>

      <label for="skills">Skills</label>
      <textarea id="skills" name="skills" rows="3" required></textarea>

      <label for="projects">Projects</label>
      <textarea id="projects" name="projects" rows="4" required></textarea>

      <button type="submit">Generate Resume</button>
    </form>
  </div>
</body>
    </html>
    """)

# Resume Generation Logic
def generate_resume_ai(name, education, skills, projects):
    prompt = f"""
      Create a professional resume using the following information:
      Do not show University name and graduation year.
      Add a Brief description for project.

      Name: {name}
      Education: {education}
      Skills: {skills}
      Projects: {projects}

      Use only the provided information. Do not add any extra suggestions, fictional content, placeholders, or notes.
      Do not include any disclaimers or warnings.
      Format the resume with proper headings: Summary, Education, Skills, Projects.
      Return only the resume content.
    """

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            full_output = result[0]["generated_text"]
            cleaned_output = full_output.replace(prompt.strip(), "").strip()
            return cleaned_output
        elif "error" in result:
            return f"⚠️ Error: {result['error']}"
        else:
            return "⚠️ Unexpected response format."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Convert HTML to PDF
def convert_html_to_pdf(source_html, output_filename):
    with open(output_filename, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(source_html, dest=result_file)
    return not pisa_status.err

# Handle Resume Form Submission
@app.post("/generate_resume", response_class=HTMLResponse)
async def generate_resume(
    name: str = Form(...),
    education: str = Form(...),
    skills: str = Form(...),
    projects: str = Form(...)
):
    resume_text = generate_resume_ai(name, education, skills, projects)

    # Simple formatting into HTML
    formatted_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 30px; }}
            h1, h2 {{ text-align: center; }}
            section {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>{name}</h1>
        <section><h2>Resume</h2><pre>{resume_text}</pre></section>
    </body>
    </html>
    """

    pdf_filename = f"{name.replace(' ', '_')}_resume.pdf"
    convert_html_to_pdf(formatted_html, pdf_filename)

    return HTMLResponse(content=f"""
    <html>
    <head><title>{name}'s Resume</title></head>
    <body style="font-family:sans-serif; padding:30px;">
        <h2>{name}'s AI-Generated Resume</h2>
        <a href="/download/{pdf_filename}" download>
            <button style="padding:10px 20px; font-size:16px;">Download PDF</button>
        </a>
        <br><br>
        <pre style="background:#f4f4f4; padding:20px; border-radius:10px; white-space:pre-wrap;">{resume_text}</pre>
        <br><a href="/">← Back to Form</a>
    </body>
    </html>
    """)

# Serve the PDF file for download
@app.get("/download/{pdf_filename}", response_class=FileResponse)
async def download_pdf(pdf_filename: str):
    return FileResponse(path=pdf_filename, filename=pdf_filename, media_type='application/pdf')
