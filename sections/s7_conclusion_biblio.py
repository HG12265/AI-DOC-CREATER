from utils.formatting import add_main_heading, add_formatted_body
from utils.ai_engine import get_groq_content

def run(doc, data, client):
    # 6. CONCLUSION (Strict 1 Page)
    add_main_heading(doc, "6. CONCLUSION")
    conc = get_groq_content(client, f"Project conclusion for {data['project_title']}", 280)
    add_formatted_body(doc, conc)
    
    # 7. FUTURE ENHANCEMENTS (Strict 1 Page)
    add_main_heading(doc, "7. FUTURE ENHANCEMENTS")
    future = get_groq_content(client, f"Future scope and scaling for {data['project_title']}", 280)
    add_formatted_body(doc, future)
    
    # 8. BIBLIOGRAPHY (Strict 1 Page)
    add_main_heading(doc, "8. BIBLIOGRAPHY")
    bib = get_groq_content(client, "Standard academic references for Full Stack Development and Software Engineering", 250)
    add_formatted_body(doc, bib)