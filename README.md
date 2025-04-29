# 📘 AI Words Book

**AI Words Book** 是一个轻量级的英语学习辅助工具，旨在帮助学习者从字幕或文章中筛选出超出自己词汇范围的单词，并可手动标记值得学习的表达方式，最终导出学习清单，构建属于你自己的单词书（Word Book）。

该项目完全基于 HTML + JavaScript 实现，无需安装、无需部署，直接本地打开网页即可使用。

---

## ✨ 项目特点

- ✅ **词汇识别辅助**：结合 Python 分析脚本，标出字幕中你可能不认识的词汇；
- ✅ **人工标记单词**：支持点击英文单词进行高亮，构建你自己的词汇清单；
- ✅ **句子表达收藏**：每行字幕前的复选框允许你收藏值得学习的表达方式；
- ✅ **拟物化设计**：全局采用拟物风格 UI，按钮与交互控件具有真实质感；
- ✅ **无需部署**：纯前端实现，支持离线运行。
- ✅ **AI生成单词书**：GPT直接输出LaTeX代码，可编译成单词书

---

## 🛠 使用方法

### 第一步：准备字幕文件和生词列表

1. 将字幕（如 `.ass`）转为 `.csv` 格式，包含以下三列（含表头）：

```
   | Start Time | Chinese Sentence | English Sentence |
   |------------|------------------|------------------|
```

程序需要根据字幕格式和字幕组风格调整。


2. 使用你自己的 Python 脚本（或参考我们提供的样例）输出 `unknown_words.txt`，其中包含你不认识的单词，每行一个词。

### 第二步：打开网页进行交互

1. 打开 `index.html` 文件（即本项目主页）；
2. 点击 `Choose CSV File` 导入字幕；
3. 点击 `Upload Unknown Words` 上传不认识的单词列表；
4. 页面将自动以虚线标出较难单词，点击任意单词可进行高亮标记；
5. 若某句整体值得学习，可勾选行首复选框。

### 第三步：导出学习清单

点击 `Export CSV with Hard Words` 按钮，导出仅包含你标记过内容的 `.csv` 文件。该文件会包含原始字幕内容和你选择的难词列表（JSON 格式）：

```csv
Start Time,Chinese Sentence,English Sentence,Hard Words
0:00:14.13,你是谁,Who are you?,["Who"]
```

### 第四步：AI释义并排版电子书

访问[ChatGPT](https://chatgpt.com/g/g-680a05e7e40c819188f661e74f64e938-aidan-ci-shu-zhu-shou)，将生成的学习清单CSV文件内容直接复制并发送给ChatGPT，ChatGPT会直接添加单词释义并生成电子书LaTeX代码。使用Overleaf选择`xelatex`编译即可生成电子单词书。

## 📁 文件结构
```bash

AI-Words-Book/
├── index.html              # 主网页（打开即可使用）
├── sample.csv              # 示例字幕CSV
├── unknown_words.txt       # 示例生词列表
├── README.md               # 当前说明文档
```

## 📌 注意事项
本项目不会上传或储存你的数据，完全在浏览器本地执行；

请使用 UTF-8 或 UTF-16 编码保存你的字幕文件；

建议使用 Chrome 或 Firefox 浏览器获得最佳体验；


## 💡 适合人群
想提升词汇量的英语学习者；

喜欢从真实语境中学习单词和表达的用户；


## 📜 License
This project is licensed under the MIT License. Feel free to use and modify.
