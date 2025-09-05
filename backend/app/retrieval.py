from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .config import KNOWLEDGE_CSV_PATH


@dataclass
class RetrievalResult:
    passages: List[Tuple[str, float]]  # (text, score)


class KnowledgeBase:
    def __init__(self, csv_path: str | None = None) -> None:
        self.csv_path = csv_path or KNOWLEDGE_CSV_PATH
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix = None
        self.rows: List[str] = []

    def load(self) -> None:
        if not os.path.exists(self.csv_path):
            self.rows = []
            self.vectorizer = TfidfVectorizer(stop_words="english")
            self.matrix = self.vectorizer.fit_transform([""])
            return
        df = pd.read_csv(self.csv_path)
        df = df.fillna("")
        texts = [
            f"Sender: {r.get('sender','')} | Subject: {r.get('subject','')} | Body: {r.get('body','')}"
            for _, r in df.iterrows()
        ]
        self.rows = texts
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 5) -> RetrievalResult:
        if not self.vectorizer or self.matrix is None or len(self.rows) == 0:
            return RetrievalResult(passages=[])
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        results: List[Tuple[str, float]] = [(self.rows[i], float(s)) for i, s in ranked if s > 0]
        return RetrievalResult(passages=results)


# Singleton loader
kb_instance: KnowledgeBase | None = None


def get_kb() -> KnowledgeBase:
    global kb_instance
    if kb_instance is None:
        kb_instance = KnowledgeBase()
        kb_instance.load()
    return kb_instance


