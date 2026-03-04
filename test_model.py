from model import train_model, predict_delay

# Train the model first
train_model()

# Test prediction
result = predict_delay(
    day="Fri",
    avg_delay=10,
    max_delay=35,
    delay_std=6,
    late_ratio=0.5
)

print(result)