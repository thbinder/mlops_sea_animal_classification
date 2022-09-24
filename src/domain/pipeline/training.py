import warnings

from absl import logging as absl_logging
from dotenv import load_dotenv
from zenml.pipelines import pipeline

from src.domain.steps.data_loader import train_data_loader
from src.domain.steps.mlflow_evaluator import evaluate_classifier
from src.domain.steps.mlflow_trainer import train_classifier

# Configure warnings
warnings.filterwarnings("ignore")
absl_logging.set_verbosity(-10000)


@pipeline
def training_pipeline(
    load_data,
    train_model,
    evaluate_model,
):

    load_dotenv()
    train_df, test_df = load_data()
    model = train_model(train_df)
    test_acc = evaluate_model(model, test_df)

    return test_acc


if __name__ == "__main__":

    pipeline = training_pipeline(
        load_data=train_data_loader(),
        train_model=train_classifier(),
        evaluate_model=evaluate_classifier(),
    )
    pipeline.run()
