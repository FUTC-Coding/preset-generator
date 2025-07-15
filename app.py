import os
from flask import Flask, render_template, request, jsonify
import main as preset_generator
from altcha import (
    ChallengeOptions,
    create_challenge,
    verify_solution,
)
import dotenv, re, time
from io import BytesIO
from random import randrange

# todo: add security headers and CSP

dotenv.load_dotenv()

HMAC_KEY = os.environ.get("ALTCHA_SECRET")
if not HMAC_KEY:
    raise ValueError("ALTCHA_SECRET environment variable not set")

app = Flask(__name__)

# Get API key from environment variable
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

cached = {"Vintage Summer": "Vintage_Summer",
          "Moody Portrait": "Moody_Portrait",
          "Bright Wedding": "Bright_Wedding",
          "Cinematic Film": "Cinematic_Film_Look",
          "B&W Drama": "Black_and_White_Drama",
          "Kodak Gold": "Kodak_Gold_Look",
          "Fujifilm Pro 400H": "Fujifilm_Pro_400H_Look"}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/challenge', methods=['GET'])
def get_challenge():
    try:
        challenge = create_challenge(
            ChallengeOptions(
                hmac_key=HMAC_KEY,
                max_number=50000,
            )
        )
        return jsonify(challenge.__dict__)
    except Exception as e:
        return jsonify({"error": f"Failed to create challenge: {str(e)}"}), 500


@app.route('/generate-preset', methods=['POST'])
def generate_preset():
    # Get theme from request
    theme = request.form.get("theme")
    model = request.form.get("model", "gpt-4o")

    # validate models
    allowed_models = ["gpt-4o", "o4-mini", "gpt-4.1-nano"]
    if model not in allowed_models:
        model = "gpt-4o"

    # Validate Input
    if not theme:
        return jsonify({"error": "No theme provided"}), 400

    # Sanitize input
    theme = sanitize_input(theme)

    if len(theme) < 3 or len(theme) > 100:
        return jsonify({"error": "Theme must be between 3 and 100 characters"}), 400

    # Check for prohibited content
    if contains_prohibited_content(theme):
        return jsonify({"error": "Input contains prohibited content"}), 400

    # Check if ALTCHA is correct
    payload = request.form.get('altcha')
    if not payload:
        return jsonify({"error": "Altcha payload missing"}), 400

    try:
        # Verify the solution
        verified, err = verify_solution(payload, HMAC_KEY, True)
        if not verified:
            return ( jsonify({"error": "Invalid Altcha payload"}), 400)
        print("altcha verification success")

    except Exception as e:
        return jsonify({"error": f"Failed to process Altcha payload: {str(e)}"}), 400


    # Disabled Caching for now

    # Check if the preset has already been cached
    # if theme in cached.keys():
    #     preset_name = cached[theme]
    #     xmp_content = get_cached_preset(preset_name)
    #
    #     print("outputting cached preset: " + preset_name)
    #     print(xmp_content)
    #
    #     # Add delay before returning cached results to make it less obvious for the user
    #     time.sleep(3)
    #
    #     if xmp_content:
    #         return jsonify({
    #             "success": True,
    #             "preset_name": preset_name,
    #             "xmp_content": xmp_content
    #         })

    try:
        # Generate preset
        jsonData = preset_generator.generate_preset(theme, model)
        print(jsonData)
        preset_name = jsonData["Name"]

        # Ensure we have a valid, safe name
        if not preset_name or len(preset_name) > 30:
            preset_name = f"{theme[:20]}_Preset"

        # Clean the name to ensure it's a valid filename
        preset_name = "".join(c for c in preset_name if c.isalnum() or c in [' ', '_', '-'])
        preset_name = preset_name.replace(' ', '_')

        xmp_content = preset_generator.create_xmp_file(jsonData)

        return jsonify({
            "success": True,
            "preset_name": preset_name,
            "xmp_content": xmp_content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def sanitize_input(text):
    """Sanitize user input to prevent prompt injection"""
    if not text:
        return ""

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    # Limit length
    text = text[:100]

    return text.strip()


def contains_prohibited_content(text):
    """Check for potentially harmful or prohibited content"""
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()

    # List of prohibited patterns or keywords
    prohibited_patterns = [
        "system:",
        "ignore previous instructions",
        "ignore all previous instructions",
        "ignore the following message",
        "ignore following message",
        "ignore above",
        "you are now",
        "you will be",
        "prompt injection",
        r"\bsql\b",
        "select * from",
        "<script>",
        "function()",
        "-->"
    ]

    # Check for prohibited patterns
    for pattern in prohibited_patterns:
        if re.search(pattern, text_lower):
            return True

    return False


def get_cached_preset(preset_name):
    # Construct the path to the cached file
    file_name = preset_name + str(randrange(1, 3))
    cache_path = os.path.join(".", "static", "cached", f"{file_name}.xmp")
    print(f"getting preset {cache_path}")
    # Check if file exists
    if not os.path.exists(cache_path):
        return None

    # Read the file into a BytesIO object
    with open(cache_path, 'rb') as f:
        xml_bytes = BytesIO(f.read())

    # Return the content as a UTF-8 string
    return xml_bytes.getvalue().decode('utf-8')


if __name__ == '__main__':
    app.run(port=8080, debug=True)