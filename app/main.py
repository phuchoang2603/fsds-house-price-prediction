import os
import time
import joblib
from fastapi import FastAPI, Request
from schema import HouseInfo, HousePrediction
from utils.data_processing import format_input_data
from utils.logging import logger
from utils.middleware import LogMiddleware
from utils.middleware import RequestIDMiddleware

app = FastAPI()
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LogMiddleware)

# Load model
model_path = os.environ.get("MODEL_PATH", "../models/model.pkl")
logger.debug("Loading model", extra={"model_path": model_path})
clf = joblib.load(model_path)
logger.debug("Model loaded successfully")


@app.post("/predict", response_model=HousePrediction)
def predict(data: HouseInfo, request: Request):
    start_time = time.time()

    try:
        logger.info(
            f"predict_received lotarea={data.LotArea} yearbuilt={data.YearBuilt} zoning={data.MSZoning}",
            extra={"request_id": request.state.request_id},
        )

        formatted_data = format_input_data(data)
        logger.debug(
            f"Formatted input: {formatted_data.values.tolist()}",
            extra={"request_id": request.state.request_id},
        )

        price = clf.predict(formatted_data)[0]
        duration = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"predict_success price={price:.2f} duration={duration}ms",
            extra={"duration_ms": duration, "request_id": request.state.request_id},
        )

        return HousePrediction(Price=price)

    except Exception as e:
        logger.exception(
            f"predict_failed error={str(e)}",
            extra={"request_id": request.state.request_id},
        )
        raise


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=30000, log_config=None)
