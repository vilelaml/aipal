import dataclasses
import orjson
from typing import Any, List, Optional
import numpy as np
import os
from src.server.memory.base import BaseMemorySingleton, get_ada_embedding

EMBED_DIM = 1536
SAVE_OPTIONS = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_DATACLASS


def create_default_embeddings():
    return np.zeros((0, EMBED_DIM)).astype(np.float32)


@dataclasses.dataclass
class CacheContent:
    texts: List[str] = dataclasses.field(default_factory=list)
    embeddings: np.ndarray = dataclasses.field(
        default_factory=create_default_embeddings
    )


class LocalCache(BaseMemorySingleton):
    def __init__(self, file="memory.json", autosave=True) -> None:
        self.memory_file = file
        self.autosave = autosave
        self.data = []

    @property
    def memories(self):
        return self.data.texts

    def add(self, data: str):
        """
        Add text to our list of texts, add embedding as row to our
            embeddings-matrix

        Args:
            data: str

        Returns: None
        """
        self.data.texts.append(data)

        embedding = get_ada_embedding(data)

        vector = np.array(embedding).astype(np.float32)
        vector = vector[np.newaxis, :]
        self.data.embeddings = np.concatenate([vector, self.data.embeddings, ], axis=0)

        if self.autosave:
            self.save()
        return data

    def clear(self) -> None:
        """
        Clears memory.
        """
        self.data = CacheContent()

    def get(self, data: str) -> Optional[List[Any]]:
        """
        Gets the data from the memory that is most relevant to the given data.

        Args:
            data: The data to compare to.

        Returns: The most relevant data.
        """
        return self.get_relevant(data, 1)

    def get_relevant(self, data: str, num_relevant: int = 5) -> List[Any]:
        """
        matrix-vector mult to find score-for-each-row-of-matrix
         get indices for top-k winning scores
         return texts for those indices
        Args:
            data: str
            num_relevant: int

        Returns: List[str]
        """
        embedding = get_ada_embedding(data)

        scores = np.dot(self.data.embeddings, embedding)

        top_k_indices = np.argsort(scores)[-num_relevant:][::-1]

        return [self.data.texts[i] for i in top_k_indices]

    def get_stats(self):
        """
        Returns: The stats of the local cache.
        """
        return len(self.data.texts), self.data.embeddings.shape

    def save(self):
        with open(self.memory_file, 'wb') as f:
            out = orjson.dumps(self.data, option=SAVE_OPTIONS)
            f.write(out)

    def load(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'rb') as f:
                file_content = f.read()
                if file_content == b'':
                    file_content = b'{}'
                loaded = orjson.loads(file_content)
                self.data = CacheContent(**loaded)
        else:
            self.data = CacheContent()
