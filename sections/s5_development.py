from utils.formatting import add_main_heading, add_sub_heading, add_formatted_body
from utils.ai_engine import get_groq_content

def run(doc, data, client):
    add_main_heading(doc, "4. SYSTEM DEVELOPMENT", force_break=True)
    
    add_sub_heading(doc, "4.1 METHODOLOGY")
    method = get_groq_content(client, "Detailed Agile Software Development Life Cycle (SDLC) methodology", 350)
    add_formatted_body(doc, method)
    
    add_sub_heading(doc, "4.2 MODULE DESCRIPTION")
    # Word count 1200 = Approx 4 pages in standard formatting
    prompt = f"""Identify 5 major modules in {data['project_title']} based on this code: {data['code_ctx'][:1500]}. 
    For each module, write a 'Title: Comprehensive Explanation' format. 
    Explain the internal logic, functions used, and data handling in depth. 
    Total length should be exactly around 1200 words to cover 4 pages."""
    
    modules_content = get_groq_content(client, prompt, 1200)
    add_formatted_body(doc, modules_content)
    
    add_sub_heading(doc, "4.3 IMPLEMENTATION HIGHLIGHTS")
    highlights = get_groq_content(client, f"Technical implementation highlights and key code logic for {data['project_title']}", 300)
    add_formatted_body(doc, highlights)