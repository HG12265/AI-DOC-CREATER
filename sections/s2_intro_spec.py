from utils.formatting import add_main_heading, add_sub_heading, add_formatted_body, create_pro_table
from utils.ai_engine import get_groq_content

def run(doc, data, client):
    # 3. TABLE OF CONTENTS
    add_main_heading(doc, "TABLE OF CONTENTS")
    toc_data = [
        ["S.NO", "TITLE", "PAGE"], ["1", "INTRODUCTION", "1"], ["2", "SYSTEM STUDY", "5"],
        ["3", "SYSTEM DESIGN", "10"], ["4", "SYSTEM DEVELOPMENT", "18"], ["5", "TESTING", "24"],
        ["6", "CONCLUSION", "28"], ["7", "BIBLIOGRAPHY", "30"], ["8", "APPENDICES", "32"],
        ["9", "SAMPLE CODING", "36"], ["10", "SAMPLE INPUT", "41"], ["11", "SAMPLE OUTPUT", "44"]
    ]
    create_pro_table(doc, toc_data, [0.8, 4.2, 0.8])

    # 4. INTRODUCTION (Strict 1 Page)
    add_main_heading(doc, "1. INTRODUCTION")
    intro = get_groq_content(client, f"Academic Introduction for {data['project_title']}", 300)
    add_formatted_body(doc, intro)

    # 1.1 SYSTEM SPECIFICATION (New Page)
    add_main_heading(doc, "1.1 SYSTEM SPECIFICATION")
    
    add_sub_heading(doc, "HARDWARE SPECIFICATION")
    hw = [["COMPONENT", "DETAILS"], ["Processor", "Intel Core i5 / i7"], ["RAM", "8GB / 16GB DDR4"], ["Disk", "256GB / 512GB SSD"], ["Input", "Keyboard & Mouse"]]
    create_pro_table(doc, hw, [2.5, 3.5])
    
    doc.add_paragraph("\n")
    add_sub_heading(doc, "SOFTWARE SPECIFICATION")
    sw = [["TYPE", "SPECIFICATION"], ["Operating System", "Windows 10 / 11"], ["Frontend", "HTML5, CSS3, JS"], ["Backend", "Python Flask / Node.js"], ["Database", "MySQL / SQLite"]]
    create_pro_table(doc, sw, [2.5, 3.5])