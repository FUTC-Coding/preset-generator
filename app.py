import os
from flask import Flask, render_template, request, jsonify, send_file
import shutil
import main as preset_generator
from altcha import (
    ChallengeOptions,
    create_challenge,
    verify_solution,
)
import dotenv

dotenv.load_dotenv()

HMAC_KEY = os.environ.get("ALTCHA_SECRET")
if not HMAC_KEY:
    raise ValueError("ALTCHA_SECRET environment variable not set")

app = Flask(__name__)

# Get API key from environment variable
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


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
    # if not OPENAI_API_KEY:
    #     return jsonify({"error": "OpenAI API key not configured"}), 500

    # Get theme from request
    theme = request.form.get('theme')

    if not theme:
        return jsonify({"error": "No theme provided"}), 400

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

    try:
        # Generate preset
        jsonData = preset_generator.generate_preset(theme)
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


if __name__ == '__main__':
    app.run(port=8080, debug=True)