from rank_bm25 import BM25Okapi


class KeywordSearchService:
    def __init__(self, documents):
        self.documents = documents
        self.tokenized_corpus = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def search(self, query, top_k=3):
        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)

        ranked_docs = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, score in ranked_docs[:top_k]]
    