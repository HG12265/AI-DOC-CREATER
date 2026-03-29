from utils.formatting import add_main_heading, add_sub_heading, add_formatted_body
from utils.ai_engine import get_groq_content

def run(doc, data, client):
    add_main_heading(doc, "5. TESTING")
    
    add_sub_heading(doc, "5.1 TESTING STRATEGIES")
    content_s = get_groq_content(client, f"Professional Unit, Integration, and System testing strategies for {data['project_title']}", 350)
    add_formatted_body(doc, content_s)
    
    add_sub_heading(doc, "5.2 TEST CASES AND RESULTS")
    content_t = get_groq_content(client, f"Generate 5 technical test cases with Input, Expected, and Status for {data['project_title']}", 350)
    add_formatted_body(doc, content_t)