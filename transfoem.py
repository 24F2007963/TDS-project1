import json

# Load your scraped dict JSON file
with open('course_content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = []

for filepath, raw_text in data.items():
    filename = filepath.split('\\')[-1]
    lines = raw_text.strip().split('\n')
    title = lines[0].strip() if lines else filename
    content = ' '.join(line.strip() for line in lines[1:] if line.strip())
    
    new_data.append({
        'filename': filename,
        'title': title,
        'content': content
    })

# Save to a new JSON file
with open('cleaned_content.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
