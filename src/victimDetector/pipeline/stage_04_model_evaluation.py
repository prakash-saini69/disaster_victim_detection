from victimDetector.config.configuration import ConfigurationManager
from victimDetector.components.model_evaluation import Evaluation 
from victimDetector import logger

STAGE_NAME = "Evaluation stage"

class EvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        eval_config = config.get_evaluation_config()
        
        evaluation = Evaluation(eval_config)
        
        # This function runs validation AND saves the score internally
        evaluation.evaluation()
        evaluation.save_score()
        # This logs the results to DagsHub
        evaluation.log_into_mlflow()

if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EvaluationPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e