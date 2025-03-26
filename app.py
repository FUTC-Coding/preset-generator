import os
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
import shutil
import main as preset_generator

app = Flask(__name__)

TEMP_DIR = tempfile.mkdtemp()

# Get API key from environment variable
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-preset', methods=['POST'])
def generate_preset():
    # if not OPENAI_API_KEY:
    #     return jsonify({"error": "OpenAI API key not configured"}), 500

    # Get theme from request
    theme = request.form.get('theme')

    if not theme:
        return jsonify({"error": "No theme provided"}), 400

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

        # Create a temporary file to store the XMP
        temp_file_path = os.path.join(TEMP_DIR, f"{preset_name}.xmp")

        xmp_content = preset_generator.create_xmp_file(jsonData)

        return jsonify({
            "success": True,
            "preset_name": preset_name,
            "xmp_content": xmp_content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Clean up temp files when the app exits
@app.teardown_appcontext
def cleanup_temp_files(exception):
    try:
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
    except Exception as e:
        print(f"Error cleaning up temp files: {e}")

if __name__ == '__main__':
    app.run(port=8080, debug=True)