import sys
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.ggl_estimator import GGLEstimator

class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        """
        :param model_evaluation_artifact: Output reference of data evaluation artifact stage
        :param model_pusher_config: Configuration for model pusher
        """
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.ggl_estimator = GGLEstimator()
        
    def push(self):
        try:
            if self.model_evaluation_artifact.is_model_accepted:
                self.ggl_estimator.save_model(local_path = self.model_evaluation_artifact.trained_model_path,
                                              drive_filename = self.model_evaluation_artifact.ggl_model_path)
                logging.info(f"Model saved to the cloud as {self.model_evaluation_artifact.ggl_model_path}")
            else:
                logging.info("Model is not eligable to be pushed")
        except Exception as e:
            logging.error("Unexpected error occured while pushing the model to the cloud : %s",e)
            raise MyException(e, sys) from e
            
           
if __name__=='__main__':
    mea = ModelEvaluationArtifact(is_model_accepted=True,
                                  changed_accuracy=0.9090382765736911,
                                  ggl_model_path='model.pkl',
                                  trained_model_path='artifact\\05_28_2025_17_21_21\\model_trainer\\trained_model\\model.pkl')
    mpc = ModelPusherConfig()
    obj = ModelPusher(model_evaluation_artifact=mea, model_pusher_config=mpc)
    obj.push()
                                  
