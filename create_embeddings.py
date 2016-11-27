import numpy as np
from gensim.models import Word2Vec
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

import dataset as ds

EMB_SIZE = 20

h_sentences = ds.dataset()

model = Word2Vec(size=EMB_SIZE, window=4, min_count=5, max_vocab_size=10000)
model.build_vocab(h_sentences)  # can be a non-repeatable, 1-pass generator
print('Training word2vec model.....')
model.train(h_sentences)  # can be a non-repeatable, 1-pass generator

vocab = list(model.vocab.keys())
vocab_size = len(vocab)

print(vocab)
print(vocab_size)

indices = np.arange(vocab_size * 0.5, dtype=int)
np.random.shuffle(indices)

words = [vocab[i] for i in indices]
vecs = [model[w].reshape((1, EMB_SIZE)) for w in words]
vecs = np.array(np.concatenate(vecs), dtype='float')

# T-SNE
print('Running t-sne....')
ts = TSNE(2)
reduced_vecs = ts.fit_transform(vecs)

print('Running DBSCAN....')
db_pred = DBSCAN(eps=2, ).fit_predict(reduced_vecs)

print('Plotting results.')
# Plot results
plt.figure()
plt.scatter(reduced_vecs[:, 0], reduced_vecs[:, 1], c=db_pred)
for i in range(len(reduced_vecs)):
    plt.annotate(words[i], xy=(reduced_vecs[i, 0], reduced_vecs[i, 1]), size='x-small')
plt.show()


