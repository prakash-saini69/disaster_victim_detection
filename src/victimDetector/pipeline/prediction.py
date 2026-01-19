import os
import glob
import cv2
import shutil
from ultralytics import YOLO
from victimDetector import logger

class PredictionPipeline:
    def __init__(self, filename):
        self.filename = filename

    def predict(self):
        try:
            # 1. SETUP PATHS
            cwd = os.getcwd()
            model_path = os.path.join(cwd, "artifacts", "training", "model.pt")
            
            # Base folder where we want the final result
            base_output_dir = os.path.join(cwd, "static", "predictions")
            
            # Temp folder for YOLO to play in
            yolo_run_dir = os.path.join(base_output_dir, "yolo_runs")
            
            # Clean up previous runs
            if os.path.exists(yolo_run_dir):
                shutil.rmtree(yolo_run_dir)
            
            # 2. LOAD MODEL
            if not os.path.exists(model_path):
                logger.error(f"Model not found at {model_path}")
                return "Error"
            
            model = YOLO(model_path)

            # 3. RUN PREDICTION
            # Uses confidence 0.25 to catch more victims
            results = model.predict(
                source=self.filename, 
                save=True, 
                conf=0.25,
                project=yolo_run_dir,
                name="run",
                exist_ok=True
            )

            # 4. FIND THE AVI FILE
            search_pattern = os.path.join(yolo_run_dir, "**", "*.avi")
            list_of_avis = glob.glob(search_pattern, recursive=True)
            
            if not list_of_avis:
                logger.error(f"YOLO finished but no .avi found in {yolo_run_dir}")
                return "Error"

            avi_file_path = list_of_avis[0]
            logger.info(f"Found AVI file at: {avi_file_path}")

            # 5. DEFINE FINAL MP4 PATH
            input_filename = os.path.basename(self.filename)
            name_no_ext = os.path.splitext(input_filename)[0]
            final_mp4_path = os.path.join(base_output_dir, name_no_ext + ".mp4")

            # 6. CONVERT AVI -> MP4
            logger.info(f"Converting to MP4 at: {final_mp4_path}")
            
            # CALLING THE FUNCTION (This line was failing before)
            self.convert_avi_to_mp4(avi_file_path, final_mp4_path)

            # 7. CLEANUP
            if os.path.exists(final_mp4_path):
                shutil.rmtree(yolo_run_dir) # Delete temp folder
                return name_no_ext + ".mp4"
            else:
                return "Error"

        except Exception as e:
            logger.exception(f"Prediction failed: {e}")
            return "Error"

    # --- IMPORTANT: THIS FUNCTION MUST BE ALIGNED WITH def predict() ---
    def convert_avi_to_mp4(self, input_path, output_path):
        try:
            cap = cv2.VideoCapture(input_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)

            # STRATEGY 1: Try 'avc1' (H.264) - Best for Web Browsers
            fourcc = cv2.VideoWriter_fourcc(*'avc1') 
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            # CRITICAL CHECK: Did the codec initialize?
            if not out.isOpened():
                logger.warning("⚠️ H.264 (avc1) codec failed. Falling back to 'mp4v'...")
                # STRATEGY 2: Try 'mp4v' - Works on almost all Windows PCs
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)

            cap.release()
            out.release()
        except Exception as e:
            logger.error(f"Conversion Error: {e}")