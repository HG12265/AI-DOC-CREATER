import os
import uuid
import shutil
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_file, after_this_request
from groq import Groq
from docx import Document

# Utils and Engine imports
from utils.formatting import setup_page_layout
from utils.ai_engine import extract_code_context, download_github_repo

# All 10 Modular Section Imports (As defined in our structure)
from sections import (s1_title_abstract, s2_intro_spec, s3_system_study, 
                      s4_system_design, s5_development, s6_testing, 
                      s7_conclusion_biblio, s8_appendices, s9_sample_coding, s10_sample_io)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Environment Variables
load_dotenv() 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def index():
    """Renders the Premium AI Doc-Gen UI"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # 1. CREATE UNIQUE SESSION DIRECTORY
    # Ithunala multiple users use pannalum files mix aagathu
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(UPLOAD_FOLDER, session_id)
    os.makedirs(session_dir, exist_ok=True)

    # 2. FORM DATA COLLECTION
    project_title = request.form.get('project_title', 'PROJECT REPORT')
    student_name = request.form.get('student_name', 'STUDENT NAME')
    github_url = request.form.get('github_url', '').strip()
    zip_file = request.files.get('file')
    
    zip_path = None

    try:
        # 3. GITHUB OR ZIP LOGIC
        if github_url:
            print(f"Nanba, downloading from GitHub: {github_url}")
            zip_path = download_github_repo(github_url, session_dir)
        
        if not zip_path and zip_file and zip_file.filename != '':
            zip_path = os.path.join(session_dir, zip_file.filename)
            zip_file.save(zip_path)

        if not zip_path or not os.path.exists(zip_path):
            shutil.rmtree(session_dir) # Cleanup if failed
            return "Please provide a valid GitHub URL or upload a ZIP file nanba!", 400

        # 4. CONTEXT EXTRACTION
        code_ctx = extract_code_context(zip_path)

        # Build data dictionary for all modular sections
        data = {
            'project_title': project_title,
            'student_name': student_name,
            'zip_path': zip_path,
            'code_ctx': code_ctx,
            'input_images': [request.files.get(f'input_img{i}') for i in range(1, 4)],
            'output_images': [request.files.get(f'output_img{i}') for i in range(1, 4)]
        }

        # 5. INITIALIZE DOCUMENT
        doc = Document()
        setup_page_layout(doc)

        # 6. EXECUTE MODULAR SECTIONS (Sequential Professional Flow)
        s1_title_abstract.run(doc, data, client)
        s2_intro_spec.run(doc, data, client)
        s3_system_study.run(doc, data, client)
        s4_system_design.run(doc, data, client)
        s5_development.run(doc, data, client)
        s6_testing.run(doc, data, client)
        s7_conclusion_biblio.run(doc, data, client)
        s8_appendices.run(doc, data, client)
        s9_sample_coding.run(doc, data, client)
        s10_sample_io.run(doc, data, client)

        # 7. SAVE FINAL DOCUMENT
        final_filename = f"{student_name.replace(' ', '_')}_Report.docx"
        final_path = os.path.join(session_dir, final_filename)
        doc.save(final_path)

        # --- SMART CLEANUP LOGIC ---
        # Ithu download mudinjathum moththa temporary folder-aiyum delete pannidum
        response = send_file(final_path, as_attachment=True)

        @response.call_on_close
        def cleanup():
            try:
                print(f"Nanba, cleaning session data: {session_id}")
                shutil.rmtree(session_dir)
            except Exception as cleanup_err:
                print(f"Cleanup Error: {str(cleanup_err)}")

        return response

    except Exception as e:
        print(f"Master Error: {str(e)}")
        # Error vanthalum memory cleanup pannanum
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)
        return f"Generation failed nanba: {str(e)}", 500

if __name__ == '__main__':
    # Dynamic port for hosting platforms like Render
    port = int(os.environ.get("PORT", 5000))
    # Threaded mode enable pannirukken for better performance
    app.run(host='0.0.0.0', port=port, threaded=True)