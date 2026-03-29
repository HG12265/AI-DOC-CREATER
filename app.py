import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_file
from groq import Groq
from docx import Document

# Utils and Engine imports
from utils.formatting import setup_page_layout
from utils.ai_engine import extract_code_context, download_github_repo

# All 12 Sections Modular Imports
from sections import (s1_title_abstract, s2_intro_spec, s3_system_study, 
                      s4_system_design, s5_development, s6_testing, 
                      s7_conclusion_biblio, s8_appendices, s9_sample_coding, s10_sample_io)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

load_dotenv() # .env file-ah load pannum
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def index():
    """Renders the Premium AI Doc-Gen UI"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # 1. FORM DATA COLLECTION
    project_title = request.form.get('project_title', 'PROJECT REPORT')
    student_name = request.form.get('student_name', 'STUDENT NAME')
    github_url = request.form.get('github_url', '').strip()
    zip_file = request.files.get('file')
    
    zip_path = None

    # 2. GITHUB OR ZIP LOGIC
    # Priority 1: GitHub Link
    if github_url:
        print(f"Nanba, downloading from GitHub: {github_url}")
        zip_path = download_github_repo(github_url, UPLOAD_FOLDER)
    
    # Priority 2: Uploaded File (if GitHub fails or not provided)
    if not zip_path and zip_file and zip_file.filename != '':
        zip_path = os.path.join(UPLOAD_FOLDER, zip_file.filename)
        zip_file.save(zip_path)

    # Error handling if no source found
    if not zip_path:
        return "Please provide a GitHub URL or upload a Project ZIP file nanba!", 400

    # 3. CONTEXT EXTRACTION (AI-Engine)
    # Extracts code logic and sample code for the document
    code_ctx = extract_code_context(zip_path)

    # Data dictionary for all sections
    data = {
        'project_title': project_title,
        'student_name': student_name,
        'zip_path': zip_path,
        'code_ctx': code_ctx,
        'input_images': [request.files.get(f'input_img{i}') for i in range(1, 4)],
        'output_images': [request.files.get(f'output_img{i}') for i in range(1, 4)]
    }

    # 4. INITIALIZE PROFESSIONAL DOCUMENT
    doc = Document()
    setup_page_layout(doc) # A4 size, Double Borders, Global Styles

    # 5. EXECUTE ALL 12 SECTIONS (Sequential Professional Flow)
    try:
        # S1: Title Page & Abstract
        s1_title_abstract.run(doc, data, client)
        
        # S2: TOC, Introduction, System Specification
        s2_intro_spec.run(doc, data, client)
        
        # S3: System Study (Existing, Drawbacks, Proposed, Features)
        s3_system_study.run(doc, data, client)
        
        # S4: System Design (Architecture, Input Design, Output Design)
        s4_system_design.run(doc, data, client)
        
        # S5: System Development (Methodology, Modules)
        s5_development.run(doc, data, client)
        
        # S6: Testing Strategies & Test Cases
        s6_testing.run(doc, data, client)
        
        # S7: Conclusion, Future Scope, Bibliography
        s7_conclusion_biblio.run(doc, data, client)
        
        # S8: Appendices (DFD, Use Case, Sequence Diagrams via Gemini)
        s8_appendices.run(doc, data, client)
        
        # S9: Sample Coding (Real Code from Source)
        s9_sample_coding.run(doc, data, client)
        
        # S10: Sample Input & Output Screenshots with AI explanations
        s10_sample_io.run(doc, data, client)

    except Exception as e:
        print(f"Error during document generation: {str(e)}")
        return f"Generation failed nanba: {str(e)}", 500

    # 6. SAVE AND DOWNLOAD
    final_filename = f"{student_name.replace(' ', '_')}_Project_Report.docx"
    final_path = os.path.join(UPLOAD_FOLDER, final_filename)
    doc.save(final_path)

    # Cleanup temporary zip if it was downloaded from GitHub
    if github_url and os.path.exists(zip_path):
        # Optional: os.remove(zip_path) 
        pass

    return send_file(final_path, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)