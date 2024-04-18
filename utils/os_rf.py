import pickle

# Load the model from the file
with open('models\\random_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

def tcp_os(row):
    return model.predict(row)