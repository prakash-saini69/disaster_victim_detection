import os
from flask import Flask, render_template, request, url_for
from flask_cors import CORS, cross_origin
from victimDetector.pipeline.prediction import PredictionPipeline

app = Flask(__name__)
CORS(app)

# Use absolute paths for safety
BASE_DIR = os.getcwd()
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
PREDICTION_FOLDER = os.path.join(BASE_DIR, 'static', 'predictions')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREDICTION_FOLDER, exist_ok=True)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        if 'video' not in request.files:
            return render_template('index.html', error="No video file provided")
            
        video_file = request.files['video']
        if video_file.filename == '':
            return render_template('index.html', error="No selected file")

        # 1. Save Video
        filename = video_file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(file_path)
        print(f"DEBUG: Video saved to {file_path}")

        # 2. Run Pipeline
        obj = PredictionPipeline(file_path)
        output_filename = obj.predict()
        print(f"DEBUG: Pipeline returned filename: {output_filename}")
        
        if output_filename == "Error":
             return render_template('index.html', error="Prediction Failed: Check terminal logs")

        # 3. Generate URL
        # result_video_url will be something like /static/predictions/video.mp4
        result_video_url = url_for('static', filename='predictions/' + output_filename)
        print(f"DEBUG: Generated URL: {result_video_url}")

        return render_template('result.html', video_path=result_video_url)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return render_template('index.html', error=str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)