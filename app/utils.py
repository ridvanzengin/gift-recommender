import re

def format_as_list(response_text):
    # Detect both numbered (1., 2.) and bullet (•) items
    items = re.split(r'\d+\.\s|\n•\s', response_text)
    if len(items) > 1:
        html_list = "<ul>" + "".join(f"<li>{item.strip()}</li>" for item in items if item) + "</ul>"
        return html_list
    else:
        return f"<p>{response_text}</p>"  # Wrap non-listed text in paragraph tags

def format_paragraphs(response_text):
    # Split the response text into paragraphs by double line breaks or bullet points
    paragraphs = re.split(r'\n\n|\n•\s', response_text)
    formatted_text = ""
    for paragraph in paragraphs:
        # Wrap each paragraph in <p> tags, but do not add <br> tags within paragraphs
        formatted_text += f"<p>{paragraph.strip()}</p>"
    return formatted_text

def highlight_keywords(response_text, keywords=["Important", "Note"]):
    for keyword in keywords:
        response_text = re.sub(rf"\b{keyword}\b", f"<strong>{keyword}</strong>", response_text)
    return response_text

def add_emoji(response_text):
    # Add emojis to certain words for visual interest
    replacements = {"Important": "⚠️ Important", "Note": "📌 Note"}
    for key, emoji_version in replacements.items():
        response_text = response_text.replace(key, emoji_version)
    return response_text

def format_response(response_text):
    response_text = format_as_list(response_text)  # Convert lists first
    response_text = format_paragraphs(response_text)  # Format remaining paragraphs
    response_text = highlight_keywords(response_text)  # Highlight important keywords
    response_text = add_emoji(response_text)  # Add emojis
    return response_text
