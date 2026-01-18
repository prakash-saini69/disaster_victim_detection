
import os
from victimDetector.constants import *
from victimDetector.utils.common import read_yaml, create_directories
from pathlib import Path

from victimDetector.entity.config_entity import (DataIngestionConfig, PrepareBaseModelConfig , TrainingConfig , EvaluationConfig)




class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

    

        create_directories([self.config.artifacts_root])

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url =config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )

        return data_ingestion_config
    



    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            params_model_type=self.params.yolo_params.model_type
        )

        return prepare_base_model_config
    



    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        params = self.params.yolo_params
        
        # Pointing to the Unzipped Data from Data Ingestion
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "C2A_Dataset")
        
        create_directories([Path(training.root_dir)])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            base_model_path=Path(prepare_base_model.base_model_path),
            training_data=Path(training_data),
            params_epochs=params.epochs,
            params_batch_size=params.batch_size,
            params_imgsz=params.imgsz,
            params_model_type=params.model_type
        )

        return training_config
    




    def get_evaluation_config(self) -> EvaluationConfig:
        # 1. Get configurations from config.yaml
        training = self.config.training
        evaluation = self.config.evaluation  # <--- Now reading the evaluation section
        
        # 2. Get params
        params = self.params.yolo_params

        # 3. Locate data.yaml (Priority: Artifacts -> Root)
        data_yaml_path = os.path.join(self.config.artifacts_root, "training", "data.yaml")
        if not os.path.exists(data_yaml_path):
             data_yaml_path = os.path.join(os.getcwd(), "data.yaml")

        # 4. Create Config Object
        eval_config = EvaluationConfig(
            path_of_model=Path(training.trained_model_path),
            training_data=Path(data_yaml_path),
            
            # ✅ UPDATED: Reads dynamically from config.yaml
            mlflow_uri=evaluation.mlflow_uri,
            
            all_params=params,
            params_imgsz=params.imgsz,
            params_batch_size=params.batch_size
        )
        
        return eval_config