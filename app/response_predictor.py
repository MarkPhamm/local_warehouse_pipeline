from pathlib import Path

import joblib
import numpy as np
import pandas as pd


class ResponsePredictor:
    def __init__(self):
        # Current file is in: project_root/app/
        # We need to go to:   project_root/src/model/
        self.base_path = Path(__file__).parent.parent / "src" / "models"

        self.model = None
        self.preprocessor = None
        self.encoder = None

        self.load_artifacts()

    def load_artifacts(self):
        """Load the trained XGBoost model, Preprocessor, and Label Encoder."""
        try:
            self.model = joblib.load(self.base_path / "xgboost.pkl")
            self.preprocessor = joblib.load(self.base_path / "preprocessor.pkl")
            self.encoder = joblib.load(self.base_path / "target_label_encoder.pkl")
        except FileNotFoundError:
            # Fallback specifically for debugging if paths are slightly different
            raise FileNotFoundError(
                f"Could not find model files in {self.base_path}. Check your 'src/models' folder."
            )

    def predict(self, input_data: dict):
        """
        Args:
            input_data (dict): Dictionary containing raw user inputs
        Returns:
            str: The predicted class label (decoded)
        """
        # 1. Convert dict to DataFrame
        df = pd.DataFrame([input_data])

        # 2. Transform features using the saved pipeline
        X_transformed = self.preprocessor.transform(df)

        # 3. Predict
        prediction_index = self.model.predict(X_transformed)

        # XGBoost clean up (handle nested arrays)
        if isinstance(prediction_index, np.ndarray):
            prediction_index = prediction_index.ravel()

        # 4. Decode the label
        prediction_label = self.encoder.inverse_transform(prediction_index)

        return prediction_label[0]
