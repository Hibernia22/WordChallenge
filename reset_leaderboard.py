import pickle

with open('scores_pickle', 'rb') as scores:
    data = pickle.load(scores)
data.clear()
with open('scores.pickle', 'wb') as s:
    pickle.dump(data. s)