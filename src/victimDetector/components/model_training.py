import os
import shutil
import yaml
from ultralytics import YOLO, settings  # <--- IMPORT settings
from victimDetector.entity.config_entity import TrainingConfig

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def create_data_yaml(self):
        # ... (keep this part exactly the same) ...
        data_path = self.config.training_data
        yaml_content = {
            'path': str(data_path),
            'train': 'train/images',
            'val': 'val/images',
            'test': 'test/images',
            'names': {0: 'human'}
        }
        yaml_save_path = os.path.join(self.config.root_dir, "data.yaml")
        with open(yaml_save_path, 'w') as f:
            yaml.dump(yaml_content, f)
        return yaml_save_path

    def train(self):
        # ---------------------------------------------------------
        # 1. DISABLE AUTO MLFLOW LOGGING
        # ---------------------------------------------------------
        # This prevents YOLO from creating the 'runs/mlflow' folder
        settings.update({'mlflow': False}) 
        
        # ---------------------------------------------------------
        # 2. START TRAINING
        # ---------------------------------------------------------
        data_yaml_path = self.create_data_yaml()
        
        # Load base model
        model = YOLO(self.config.base_model_path)
        
        print(f"🚀 Starting YOLO Training (MLflow auto-log disabled)...")
        
        results = model.train(
            data=data_yaml_path,
            epochs=self.config.params_epochs,
            imgsz=self.config.params_imgsz,
            batch=self.config.params_batch_size,
            name="yolo_model",
            project=str(self.config.root_dir),
            device="cpu"
        )
        
        # ---------------------------------------------------------
        # 3. SAVE MODEL (Copy best.pt -> model.pt)
        # ---------------------------------------------------------
        yolo_save_dir = results.save_dir
        best_model_generated = os.path.join(yolo_save_dir, "weights", "best.pt")
        target_path = self.config.trained_model_path
        
        if os.path.exists(best_model_generated):
            shutil.copy(best_model_generated, target_path)
            print(f"✅ Best model copied to {target_path}")
            
            # Optional: Now you can safely delete the raw runs folder if you want
            # shutil.rmtree(yolo_save_dir, ignore_errors=True)
        else:
            print(f"⚠️ Error: Could not find {best_model_generated}")