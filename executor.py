import hashlib
from typing import Tuple

import numpy as np
from jina import Executor, DocumentArray, requests


class FeatureHasher(Executor):
    """Convert a collection of features to a fixed-dimensional matrix using the hashing trick

    More info: https://en.wikipedia.org/wiki/Feature_hashing
    """

    def __init__(self, n_dim: int = 256, sparse: bool = False, text_attrs: Tuple[str, ...] = ('text',), **kwargs):
        """
        :param n_dim: the dimensionality of each document in the output embedding.
            Small numbers of features are likely to cause hash collisions,
            but large numbers will cause larger overall parameter dimensions.
        :param sparse: whether the resulting feature matrix should be a sparse csr_matrix or dense ndarray.
            Note that this feature requires ``scipy``
        :param text_attrs: which attributes to be considered as text attributes.
        :param kwargs:
        """

        super().__init__(**kwargs)
        self.n_dim = n_dim
        self.hash = hashlib.md5
        self.text_fields = text_attrs
        self.sparse = sparse

    @requests
    def encode(self, docs: DocumentArray, **kwargs):
        if self.sparse:
            from scipy.sparse import csr_matrix

        for idx, doc in enumerate(docs):
            all_tokens = doc.get_vocabulary(self.text_fields)
            if all_tokens:
                idxs, data = [], []  # sparse
                table = np.zeros(self.n_dim)  # dense
                for f_id, val in all_tokens.items():
                    h = int(self.hash(f_id.encode('utf-8')).hexdigest(), base=16)
                    col = h % self.n_dim
                    idxs.append((0, col))
                    data.append(np.sign(h) * val)
                    table[col] += np.sign(h) * val

                if self.sparse:
                    doc.embedding = csr_matrix((data, zip(*idxs)), shape=(1, self.n_dim))
                else:
                    doc.embedding = table
