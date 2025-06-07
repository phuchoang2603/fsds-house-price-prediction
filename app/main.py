import os

import joblib
from fastapi import FastAPI
from schema import HouseInfo, HousePrediction
from utils.data_processing import format_input_data
from utils.logging import logger
import time

# Creating FastAPI instance
app = FastAPI()


# Loading model with default path models/model.pkl
clf = joblib.load(os.environ.get("MODEL_PATH", "../models/model.pkl"))


# Creating an endpoint to receive the data
# to make prediction on
@app.post("/predict", response_model=HousePrediction)
def predict(data: HouseInfo):
    start_time = time.time()
    try:
        # Log input summary
        logger.info(
            f"predict_received LotArea={data.LotArea} YearBuilt={data.YearBuilt} Zoning={data.MSZoning}"
        )

        formatted_data = format_input_data(data)
        price = clf.predict(formatted_data)[0]
        duration = round((time.time() - start_time) * 1000, 2)  # in ms

        # Log prediction result
        logger.info(f"predict_success price={price:.2f} duration_ms={duration}")

        return HousePrediction(Price=price)

    except Exception as e:
        logger.exception(f'predict_failed error="{str(e)}"')
        raise
