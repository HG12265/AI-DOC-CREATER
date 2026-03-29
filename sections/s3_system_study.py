from utils.formatting import add_main_heading, add_sub_heading, add_formatted_body
from utils.ai_engine import get_groq_content

def run(doc, data, client):
    add_main_heading(doc, "2. SYSTEM STUDY")
    
    # Continuous flow, no page breaks between these
    add_sub_heading(doc, "2.1 EXISTING SYSTEM")
    add_formatted_body(doc, get_groq_content(client, f"Existing manual system drawbacks for {data['project_title']}", 180))
    
    add_sub_heading(doc, "2.2 DRAWBACKS")
    add_formatted_body(doc, get_groq_content(client, "General drawbacks of manual paper-based systems", 150))
    
    add_sub_heading(doc, "2.3 PROPOSED SYSTEM")
    add_formatted_body(doc, get_groq_content(client, f"Proposed digital solution benefits for {data['project_title']}", 180))
    
    add_sub_heading(doc, "2.4 FEATURES")
    add_formatted_body(doc, get_groq_content(client, f"Technical features of {data['project_title']}", 180))