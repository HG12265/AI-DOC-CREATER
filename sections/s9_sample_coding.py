from utils.formatting import add_main_heading
from docx.shared import Pt

def run(doc, data, client):
    add_main_heading(doc, "10. SAMPLE CODING")
    
    # Extract code context directly from data
    # Courier New font makes it look like professional code
    p = doc.add_paragraph()
    run_code = p.add_run(data['code_ctx'])
    run_code.font.name = 'Courier New'
    run_code.font.size = Pt(8.5)