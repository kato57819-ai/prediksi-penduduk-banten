with open("explanation.html", "r", encoding="utf-8") as f:
    content = f.read()
    print(f"File size: {len(content)} characters")
    print(f"Closes with body and html tags: {content.strip().endswith("</html>")}")
    print(f"No duplicate closing tags: {content.count("</html>") == 1}")
    print(f"✅ File structure OK" if content.count("</html>") == 1 and content.strip().endswith("</html>") else "❌ File has issues")
