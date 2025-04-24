import pandas as pd
import re

# Load the ASS subtitle file with UTF-16 encoding
file_path = "subtitles/Severance S01E1.ass"
with open(file_path, "r", encoding="utf-16") as file:
    lines = file.readlines()

# Extract lines starting with "Dialogue:"
dialogue_lines = [line for line in lines if line.startswith("Dialogue:")]

data = []
for line in dialogue_lines:
    parts = line.strip().split(",", 9)  # Split into 10 parts, text is the last one
    if len(parts) < 10:
        continue
    start_time = parts[1]
    text = parts[9]
    
    # Remove style tags and line breaks
    clean_text = re.sub(r"\{.*?\}", "", text)
    clean_text = clean_text.replace("\\N", " ").strip()

    # Try to split into Chinese and English parts
    # Assumes Chinese comes first followed by English
    match = re.match(r"([\u4e00-\u9fff，。“”！？：；‘’（）《》【】、·\s]+)([A-Za-z0-9 ,.'\"?!;:-]+)", clean_text)
    if match:
        chinese = match.group(1).strip()
        english = match.group(2).strip()
        data.append((start_time, english, chinese))

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Start Time", "English Sentence", "Chinese Sentence"])

# Display the DataFrame
import ace_tools as tools; tools.display_dataframe_to_user(name="Subtitle Translations", dataframe=df)
