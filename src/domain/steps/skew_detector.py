from typing import List

import pandas as pd
from evidently.model_profile import Profile  # type: ignore[import]
from zenml.integrations.evidently.steps import (
    EvidentlyProfileConfig,
    EvidentlyProfileStep,
    evidently_profile_step,
)
from zenml.steps import BaseStepConfig, Output, step


class EvidentlySkewDetectorConfig(BaseStepConfig):
    """Prediction Loading params"""

    step_name: str = "evidently_skew_detector"
    ignored_cols: List[str] = ["Filepath"]
    profile_sections: List[str] = ["datadrift"]


@step
def evidently_skew_detector(
    config: EvidentlySkewDetectorConfig, train_df: pd.DataFrame, test_df: pd.DataFrame
) -> Output(  # type:ignore[valid-type]
    profile=Profile, dashboard=str
):

    evidently_profile_config = EvidentlyProfileConfig(
        ignored_cols=config.ignored_cols, profile_sections=config.profile_sections
    )
    profile, dashboard = EvidentlyProfileStep().entrypoint(
        reference_dataset=train_df,
        comparison_dataset=test_df,
        config=evidently_profile_config,
    )

    return profile, dashboard
