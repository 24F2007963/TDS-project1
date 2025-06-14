import os
import json
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

# Path to your cloned course repo and target project directory
source_dir = Path(r"C:\Users\smriti.rani\Documents\New folder\iitm\Tools in DS\Course Source")
target_file = Path(r"C:\Users\smriti.rani\Documents\New folder\iitm\Tools in DS\Project1\course_content.json")

def extract_markdown_text(md_path):
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n").strip()

def collect_course_content():
    content = {}
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                rel_path = file_path.relative_to(source_dir)
                try:
                    text = extract_markdown_text(file_path)
                    if text:
                        content[str(rel_path)] = text
                except Exception as e:
                    print(f"❌ Failed to process {file_path}: {e}")
    return content

def save_content_to_json(data):
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Course content saved to {target_file}")

if __name__ == "__main__":
    content = collect_course_content()
    save_content_to_json(content)
