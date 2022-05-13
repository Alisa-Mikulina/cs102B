# type: ignore
import csv
import string
from collections import defaultdict
import numpy as np
from sklearn.metrics import accuracy_score

class NaiveBayesClassifier:
    def __init__(self, alpha=0):
        self.alpha = alpha
        self.class_freq = defaultdict(lambda: 0)
        self.feat_freq = defaultdict(lambda: 0)

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        for titles, label in zip(X, y):
            self.class_freq[label] += 1
            for title in titles:
                self.feat_freq[(title, label)] += 1

        num_samples = len(X)
        for k in self.class_freq:
            self.class_freq[k] /= num_samples

        for title, label in self.feat_freq:
            self.feat_freq[(title, label)] /= self.class_freq[label]

        return self

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        return [
            max(self.class_freq.keys(), key=lambda c: self.calculate_class_freq(x, c))
            for x in X
        ]

    def calculate_class_freq(self, X, clss):
        freq = -np.log(self.class_freq[clss])

        for feat in X:
            freq += -np.log(self.feat_freq.get((feat, clss), 10 ** (-7)))
        return freq

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        predictions = self.predict(X_test)
        return accuracy_score(predictions, y_test)


# def clean(s):
#     translator = str.maketrans("", "", string.punctuation)
#     return s.translate(translator)


# with open('C:\\Users\\ASUS\\Desktop\\VK\\homework06\\spam_ham.txt', 'r', encoding='utf-8') as f:
#     data = list(csv.reader(f, delimiter="\t"))

# X, y = [], []
# for target, msg in data:
#     X.append(msg)
#     y.append(target)
# X = [clean(x).lower() for x in X]

# X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

# model = NaiveBayesClassifier()
# model.fit(X_train, y_train)
# print(model.score(X_test, y_test))
# # 0.8385167464114832
