from utils.formatting import add_main_heading, add_sub_heading, add_formatted_body
from utils.ai_engine import get_groq_content
from docx.shared import Inches
import io

def run(doc, data, client):
    # --- 11. SAMPLE INPUT ---
    # Heading starts on a new page
    add_main_heading(doc, "11. SAMPLE INPUT", force_break=True)
    
    first_input = True
    for i, img in enumerate(data['input_images'], 1):
        if img and img.filename != '':
            # First image should NOT have a page break to avoid empty space under main heading
            if not first_input:
                doc.add_page_break()
            
            add_sub_heading(doc, f"Input Screenshot - Screen {i}")
            
            # Reset stream and add picture
            img.seek(0)
            doc.add_picture(io.BytesIO(img.read()), width=Inches(5.0))
            
            # AI Description (Reduced word count slightly to keep it neat)
            expl = get_groq_content(client, f"Technical 8-line explanation for Input Screen {i} of {data['project_title']}", 100)
            add_formatted_body(doc, expl)
            
            first_input = False # From 2nd image onwards, it will add page break

    # --- 12. SAMPLE OUTPUT ---
    # Heading starts on a new page
    add_main_heading(doc, "12. SAMPLE OUTPUT", force_break=True)
    
    first_output = True
    for i, img in enumerate(data['output_images'], 1):
        if img and img.filename != '':
            # First image should NOT have a page break under main heading
            if not first_output:
                doc.add_page_break()
            
            add_sub_heading(doc, f"Output Screenshot - Result {i}")
            
            # Reset stream and add picture
            img.seek(0)
            doc.add_picture(io.BytesIO(img.read()), width=Inches(5.0))
            
            # AI Description
            expl = get_groq_content(client, f"Technical 8-line explanation for Output Screen {i} of {data['project_title']}", 100)
            add_formatted_body(doc, expl)
            
            first_output = False