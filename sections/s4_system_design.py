from utils.formatting import add_main_heading, add_sub_heading, add_formatted_body
from utils.ai_engine import get_groq_content

def run(doc, data, client):
    add_main_heading(doc, "3. SYSTEM DESIGN AND IMPLEMENTATION")
    
    add_sub_heading(doc, "3.1 ARCHITECTURAL OVERVIEW")
    add_formatted_body(doc, get_groq_content(client, f"Detailed architectural design of {data['project_title']}", 380))
    
    add_main_heading(doc, "3.2 INPUT DESIGN") # Full Page
    add_formatted_body(doc, get_groq_content(client, f"UI and Data entry design for {data['project_title']}", 380))
    
    add_main_heading(doc, "3.3 OUTPUT DESIGN") # Full Page
    add_formatted_body(doc, get_groq_content(client, f"Report generation and dashboard output design for {data['project_title']}", 380))