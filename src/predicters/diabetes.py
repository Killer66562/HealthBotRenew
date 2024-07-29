from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

type PredictResult = dict[str, Any]


class IPredicter(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def predict(self, values: list[Any]) -> PredictResult: ...

    @property
    @abstractmethod
    def required_values_len(self) -> int: ...

class DiabetesPredicter(IPredicter):
    RESULT_HAVE_DIABETES = "have_diabetes"
    RESULT_DIABETES_PERCENTAGE = "diabetes_percentage"

    COLUMNS = ['gender', 'age', 'bmi', 'HbA1c_level', 'blood_glucose_level']

    def __init__(self, model: Any) -> None:
        super().__init__()
        self._model = model

    def predict(self, values: list[Any]) -> PredictResult:
        user_input = pd.DataFrame(data=[values], columns=self.COLUMNS)
        have_diabetes = False if self._model.predict(user_input)[0] == 0 else True
        diabetes_precentage = round(float(self._model.predict_proba(user_input)[0][1]) * 100, 2)
        result = dict()
        result[self.RESULT_HAVE_DIABETES] = have_diabetes
        result[self.RESULT_DIABETES_PERCENTAGE] = diabetes_precentage
        return result
    
    @property
    def required_values_len(self) -> int:
        return len(self.COLUMNS)