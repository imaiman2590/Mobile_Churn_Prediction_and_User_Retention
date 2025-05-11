from core.model_trainer import train_model
from core.predictor import ChurnPredictor

if __name__ == "__main__":
    model, scaler = train_model()
    predictor = ChurnPredictor(model, scaler)
    print("Model initialized and ready for predictions.")
