import google.generativeai as genai
from backend.app.utils.src.config import GEMINI_KEY



genai.configure(api_key=GEMINI_KEY)

def build_prompt(transcript_json, preference="short-headings"):
    text = ""
    if transcript_json and len(transcript_json) > 0 and "tracks" in transcript_json[0]:
        tracks = transcript_json[0]["tracks"]
        for track in tracks:
            for seg in track.get("transcript", []):
                text += seg.get("text", "") + " "
    text = text[:60000]
    messyPrompt = """You are NoteGenie, a playful and efficient AI note-taker! dont change the content if it is unrelated to eduction just give the content of the video if meesy type not asked dont change the font family give prefect style give the out put in <div>ur html code<div> dont start from html ok

Task: Convert the given lecture transcript (in JSON format) into messy, last-minute exam notes in HTML+CSS format. The notes should list the contents using headings, keywords, formulas, and diagrams—no explanations or paragraphs. Students should be able to quickly glance and recognize what’s covered in the lecture.

Notes Purpose:

These are running notes, not full explanations.
Just mention topics, formulas, terms, diagrams—no definitions, examples, or details.
Students should glance and immediately recall what’s covered.
Notes should look like they were scribbled fast during class.

HTML Structure

Use <html>, <head>, <style>, and <body>.
Add CSS in <style> with different fonts, sizes, bold, underline, and colors to highlight key info—but not everywhere.
Use <h1>, <h2>, <h3> to loosely group sections.
Present content in bullet points (<ul><li>), with short phrases.
Use <strong>, <u> where needed, but randomly—not perfectly.

Content Style

Organize by headings and subheadings from the transcript flow.
Write short keywords, formulas, and phrases—avoid full sentences.
Include diagrams (<pre> for ASCII, Mermaid if useful) only where they quickly show structure or relationships.
Do not explain or elaborate—just mention what’s covered.
Do not include examples or analogies unless it’s one quick word or phrase.
Keep it general—do not refer to specific topics, fields, or recognizable examples. The format must work for any subject.

Appearance

Be playful but avoid too much playful language, slang, or unnecessary emojis.
Use styles to assist scanning—bold, underline, color hints—but not everywhere.
Notes should look handwritten and rushed, but still structured enough to be understood at a glance.

Final Output

Complete HTML content with headings, lists, and occasional diagrams.
Clear sections but no deep explanations.
Styling used meaningfully but randomly to mimic last-minute notes.
Notes must work for any topic or subject without field-specific examples.

Output:

Messy, glance-friendly, last-minute exam notes in HTML+CSS format.
Use headings, subheadings, bullet points, and diagrams to list covered topics.
No paragraphs, no detailed explanations—just keywords, formulas, and structure.
Styling (font size, color, bold, underline) to help scanning but applied unevenly, like hurried notes.
General format applicable to any lecture topic.

Write as if you're scribbling notes fast in class—organized enough to quickly see what’s covered but without unnecessary decoration or explanation"""

    parts = [
        "You are an expert educator and HTML author.check the color contrsat text and highlight color give the output in <div> 'ur html code'<div> dont give anything else even if the video is not a eduction content just give explanation and things for the video dont start the code from html mad make the whole dive or parent dive which contain ur code to bg white only make it messy is asked in user prefernce else dont make it color full highlight make it good add emoji and that emoji should be applicable when the htmk is downloaded as pdf and even for arrows u create usingdiv for flowchart",
        f"doont add '```html'to ur output give the output in <div> ur html code<div> dont give anything else Create well-structured semantic HTML notes from the transcript below. create flowchart using div tags as boxes its most needed and draw digrams using divelemts and csss make it relatable",
        f"normally give normal text if their prefernce change just change the font family ok see change he font family based on user preferance its very important is messy get messy type of fontfamily and import it in the html ur writing Use the following user preference to guide the notes style/format: '{preference}' the prefernce contain the fontfamily name use that ok dont use any othere thing only us messy if asked give more importance to preference friet fontstyle should be taken from preference if that font is not available in css import it to the html and make the whole page bg to white",
        "give the output in <div> ur html code<div> dont give anything else. Include a <style> block at the top so the PDF looks presentable. or use inline style",
        f"Transcript:\n{text}\n",
        "Use semantic HTML (<h1>, <h2>, <p>, <ul>, <li>, <strong>, <mark>) give ur whole code inside a div use inline css most. ude div tag and stryle it to create arrows for flowchart too or use an image that u can take from web but when convertion to pdf its hould be applicable.",
        "Add a short summary at the top.+ suggested contents based on above contents.i need more content as possible needed if possible add time tags where its said about in youtube vedio",
        "Return only HTML without commentary.",
        "is meesy is asked this is ur command--> '{messyPrompt}'"
    ]

    pref_lower = preference.lower()
    if "long" in pref_lower:
        parts.append("Produce thorough, explanatory notes with headings, examples, and definitions.")
    else:
        parts.append("Produce concise notes: bullet points + 1–2 sentence explanations.")

    if "flowchart" in pref_lower:
        parts.append("give the output in <div> ur html code<div> dont give anything elseInclude inline SVG flowcharts or <div class='flowchart'> placeholders.")
    if "chart" in pref_lower or "graph" in pref_lower:
        parts.append("Include inline SVG charts or <div class='chart'> placeholders. You can also create a flowchart using div tags with inline CSS.")

    return "\n".join(parts)

def call_gemini(prompt):
    model = genai.GenerativeModel("gemini-2.5-pro")
    resp = model.generate_content(prompt)
    if hasattr(resp, "text"):
        return resp.text.strip()
    return str(resp).strip()
