from typing import List

import pandas as pd
from evidently.model_profile import Profile  # type: ignore[import]
from zenml.integrations.evidently.steps import (
    EvidentlyProfileParameters,
    EvidentlyProfileStep
)
from zenml.steps import BaseParameters, Output, step


class EvidentlySkewDetectorConfig(BaseParameters):
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

    evidently_profile_config = EvidentlyProfileParameters(
        ignored_cols=config.ignored_cols, profile_sections=config.profile_sections
    )
    profile, dashboard = EvidentlyProfileStep().entrypoint(
        reference_dataset=train_df,
        comparison_dataset=test_df,
        params=evidently_profile_config,
    )

    return profile, dashboard
