import os
import mlflow
import dagshub
from urllib.parse import urlparse
from pathlib import Path
from ultralytics import YOLO
from victimDetector.utils.common import save_json
from victimDetector.entity.config_entity import EvaluationConfig

class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    def evaluation(self):
        """
        Loads the trained model and evaluates it on the TEST set.
        """
        # 1. Load the model trained in the previous step
        print(f"Loading model from: {self.config.path_of_model}")
        self.model = YOLO(self.config.path_of_model)
        
        # 2. Run Validation on the TEST split (Unseen Data)
        # This calculates true performance metrics
        self.metrics = self.model.val(
            data=self.config.training_data,
            imgsz=self.config.params_imgsz,
            batch=self.config.params_batch_size,
            split='test'  # <--- Ensures we are testing on unseen data
        )
        
        # 3. Save local JSON score for DVC tracking
        self.save_score()

    def save_score(self):
        scores = {
            "map50": self.metrics.box.map50,
            "map": self.metrics.box.map,
            "precision": self.metrics.box.mp,
            "recall": self.metrics.box.mr
        }
        save_json(path=Path("scores.json"), data=scores)
        print("Scores saved to scores.json")

    def log_into_mlflow(self):
        # 1. Initialize DagsHub Connection
        # This automatically sets up the environment for MLflow
        dagshub.init(
            repo_owner='prakashmali6556', 
            repo_name='disaster_victim_detection', 
            mlflow=True
        )
        
        # 2. Set Tracking URI explicitly (Good practice)
        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        
        print(f"Logging metrics to DagsHub: {self.config.mlflow_uri}")
        
        # 3. Start Run
        with mlflow.start_run():
            # A. Log Hyperparameters
            mlflow.log_params(self.config.all_params)
            
            # B. Log Metrics
            mlflow.log_metrics({
                "map50": self.metrics.box.map50,
                "map": self.metrics.box.map,
                "precision": self.metrics.box.mp,
                "recall": self.metrics.box.mr
            })
            
            # C. Log the Model File
            # We log the best.pt file so you can download it from DagsHub later
            if tracking_url_type_store != "file":
                mlflow.log_artifact(self.config.path_of_model, artifact_path="model")
            else:
                mlflow.log_artifact(self.config.path_of_model, artifact_path="model")
                
        print("✅ Logging Complete! Check your DagsHub dashboard.")