
import os
from pathlib import Path
from src.victimDetector.constants import *
from src.victimDetector.entity.config_entity import PrepareBaseModelConfig
from ultralytics import YOLO

import shutil

class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config


    def get_base_model(self):
        # This downloads yolov8n.pt from Ultralytics servers
        print(f"Downloading base model: {self.config.params_model_type}")
        model = YOLO(self.config.params_model_type) 
        
        # Save it to our artifacts folder
        # YOLO download logic is a bit implicit, so we save explicitly
        model.save(self.config.base_model_path)
        print(f"Base model saved at: {self.config.base_model_path}")