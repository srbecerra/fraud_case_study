import random
import cPickle as pickle

class MyModel():
    def fit(self, X, y):
        pass
    def predict(self):
        return random.choice([True, False])

def get_data():
    X = []
    y = []
    return X, y

if __name__ == '__main__':
    from model import MyModel
    X, y = get_data()
    model = MyModel()
    model.fit(X, y)
    with open('model.pkl', 'w') as f:
        pickle.dump(model, f)
