
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from pathlib import Path


class LearningTimeEstimator:
    """
    ML model to estimate learning time (days) for a skill
    """

    def __init__(self):
        base_path = Path(__file__).resolve().parents[2]
        self.data_path = base_path / "data" / "skills" / "learning_time_data.csv"

        self.model = LinearRegression()
        self.encoders = {}

        self._train_model()

    def _train_model(self):
        df = pd.read_csv(self.data_path)

        # Encode categorical columns
        for col in ["category"]:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.encoders[col] = le

        X = df[["category", "difficulty", "popularity", "is_core"]]
        y = df["days"]

        self.model.fit(X, y)

    def predict_days(self, category, difficulty, popularity, is_core):
        category_encoded = self.encoders["category"].transform([category])[0]

        X = [[category_encoded, difficulty, popularity, is_core]]
        days = self.model.predict(X)[0]

        return max(1, int(days))  # minimum 1 day
