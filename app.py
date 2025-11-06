from flask import Flask, request, render_template, flash, redirect, url_for
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in environment (.env file)")

# Configure Gemini
genai.configure(api_key=API_KEY)

app = Flask(__name__)
app.secret_key = os.urandom(24)


def call_gemini(prompt_text):
    try:
        # ✅ Use available model from your API
        model = genai.GenerativeModel("gemini-2.0-flash")  # This will work!
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {str(e)}")


@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    code_value = ""
    language = "python"

    if request.method == "POST":
        language = request.form.get("language", "python")
        file = request.files.get("file")

        if file and file.filename:
            code_value = file.read().decode("utf-8", errors="ignore")
        else:
            code_value = request.form.get("code", "").strip()

        if not code_value:
            flash("Please provide code (paste or upload).", "warning")
            return redirect(url_for("index"))

        # ✅ Correct indentation (8 spaces)
        prompt = f"""You are a concise and professional software code reviewer.
Analyze the following {language} code and respond briefly (max 4-5 lines per section).

Format your response exactly like this:
Summary:
(1 short line about what the code does)

Potential Issues:
(2-3 bullet points only)

Suggestions:
(2-3 short improvement ideas)

Code:
{code_value}
"""

        try:
            output = call_gemini(prompt)
        except Exception as e:
            flash(str(e), "danger")

    return render_template("index.html", output=output,
                           code_value=code_value, language=language)


if __name__ == "__main__":
    app.run(debug=True)
