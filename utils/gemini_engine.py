import os
import google.generativeai as genai
import re, requests, io, base64, zlib
from dotenv import load_dotenv

# Load .env file (Local-la irukum pothu use aagum)
load_dotenv()

# API KEY logic
GEMINI_KEY = os.getenv("GEMINI_API_KEY") # Render Settings-la intha name-la key podu nanba
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    # 1.5-flash is very fast for diagrams
    model = genai.GenerativeModel('gemini-flash-latest') 
else:
    print("Warning: GEMINI_API_KEY not found in environment!")

def get_gemini_diagram(project_title, diag_type, code_ctx):
    """Uses Gemini to get Mermaid code and renders via Kroki"""
    try:
        prompt = f"""
        Act as a System Architect. Generate ONLY the Mermaid.js code for a {diag_type} 
        for the project '{project_title}'. 
        
        Rules:
        1. Use 'graph TD' for DFD, 'graph LR' for Use Case, 'sequenceDiagram' for Sequence.
        2. Keep it simple (Max 8 nodes).
        3. Output ONLY the raw Mermaid code block. No markdown, No text.
        4. Project Context: {code_ctx[:500]}
        """
        
        response = model.generate_content(prompt)
        m_code = response.text.strip()
        
        # --- CLEANING (MUKKIYAM) ---
        # Remove markdown code blocks if AI adds them
        m_code = re.sub(r'```mermaid|```', '', m_code).strip()
        
        # --- KROKI RENDERER ---
        # 1. Compress text using zlib
        compressed = zlib.compress(m_code.encode('utf-8'), 9)
        # 2. Base64 URL safe encode
        encoded_string = base64.urlsafe_b64encode(compressed).decode('utf-8')
        
        # 3. Kroki API URL
        url = f"https://kroki.io/mermaid/png/{encoded_string}"
        res = requests.get(url, timeout=20)
        
        if res.status_code == 200:
            return io.BytesIO(res.content)
        else:
            print(f"Kroki Error: {res.status_code}")
            return None
            
    except Exception as e:
        print(f"Gemini Diagram Logic Error: {e}")
        return None