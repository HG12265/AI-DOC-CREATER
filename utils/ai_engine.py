import re, zipfile, os, requests # <-- Requests import sethurukken nanba

def get_groq_content(client, prompt, words):
    """Fetches text from Groq AI"""
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"{prompt}. Strictly write around {words} words. No markdown like ** or ##."}],
            temperature=0.4
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error fetching content: {str(e)}"

def extract_code_context(zip_path, max_lines=450):
    """Extracts code from zip for AI context"""
    code_text = ""
    try:
        if not os.path.exists(zip_path):
            return "Zip path does not exist."
            
        with zipfile.ZipFile(zip_path, 'r') as z:
            valid_files = [f for f in z.namelist() if any(f.endswith(ext) for ext in ['.py', '.js', '.html', '.css', '.java', '.sql'])]
            for f in valid_files:
                code_text += f"\nFILE: {f}\n{z.read(f).decode('utf-8', errors='ignore')}\n"
    except Exception as e:
        return f"Zip Extraction Error: {str(e)}"
    
    lines = code_text.split('\n')
    return '\n'.join(lines[:max_lines])

def download_github_repo(github_url, upload_folder):
    """Downloads GitHub repo as a ZIP file and returns the local path"""
    print(f"Nanba, downloading from GitHub: {github_url}") # Debugging info
    try:
        # 1. Clean URL: Remove .git and trailing slashes
        base_url = github_url.strip().rstrip('/')
        if base_url.endswith('.git'):
            base_url = base_url[:-4]
        
        # 2. Try 'main' branch first
        zip_url = f"{base_url}/archive/refs/heads/main.zip"
        response = requests.get(zip_url, stream=True, timeout=20)
        
        # 3. If 'main' fails, try 'master' branch
        if response.status_code != 200:
            zip_url = f"{base_url}/archive/refs/heads/master.zip"
            response = requests.get(zip_url, stream=True, timeout=20)

        if response.status_code == 200:
            file_name = "github_download.zip"
            file_path = os.path.join(upload_folder, file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print("Download Success nanba!")
            return file_path
        else:
            print(f"GitHub Error: Branch not found (404) on {github_url}")
            return None
            
    except Exception as e:
        print(f"GitHub Download Error: {str(e)}")
        return None