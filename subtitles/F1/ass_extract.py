import pandas as pd
import re


def split_text(text):
    # 指定分隔符
    separator = r"\N{\fn微软雅黑\fs14}"

    if separator in text:
        lst = text.split(separator)
        if len(lst) == 2:
            chinese = lst[0].strip()
            english = lst[1].strip()
        else:
            chinese = text.strip()
            english = ""
    else:
        # 检查是否只有英文、数字、空格和常见标点
        if re.fullmatch(r"[A-Za-z0-9\s.,!?\"'():;\-]+", text):
            chinese = ""
            english = text.strip()
        else:
            chinese = text.strip()
            english = ""

    return chinese, english


# Load the ASS subtitle file with UTF-16 encoding
file_path = "subtitles\F1\F1.The.Movie.ass"
with open(file_path, "r", encoding="utf-16") as file:
    lines = file.readlines()

# Extract lines starting with "Dialogue:"
dialogue_lines = [line for line in lines if line.startswith("Dialogue:")]

data = []
for line in dialogue_lines:
    parts = line.strip().split(",", 9)  # Split into 10 parts, text is the last one
    if len(parts) < 10:
        continue
    start_time = parts[1].split(".")[0]
    text = parts[9]

    chinese, english = split_text(text)

    data.append((start_time, english, chinese))

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Start Time", "English Sentence", "Chinese Sentence"])

df.to_csv("subtitles.csv", index=False, encoding="utf-8-sig")
