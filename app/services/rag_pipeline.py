from app.services.vector_store import VectorStoreService
from app.services.llm_service import LLMService
from app.services.keyword_search import KeywordSearchService
from app.prompts.rag_prompt import RAG_PROMPT_TEMPLATE
from app.prompts.rewrite_prompt import REWRITE_PROMPT_TEMPLATE


class RAGPipeline:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.llm_service = LLMService()
        self.llm = self.llm_service.get_model()

    def _format_history(self, history):
        if not history:
            return "No conversation history."

        lines = []
        for msg in history:
            role = msg.get("role", "user").capitalize()
            content = msg.get("content", "")
            lines.append(f"{role}: {content}")

        return "\n".join(lines)

    def rewrite_question(self, question: str, history=None) -> str:
        if not history:
            return question

        history_text = self._format_history(history)

        rewrite_prompt = REWRITE_PROMPT_TEMPLATE.format(
            history=history_text,
            question=question
        )

        response = self.llm_service.invoke(rewrite_prompt)
        rewritten_question = response.content.strip() if hasattr(response, "content") else str(response).strip()

        return rewritten_question if rewritten_question else question

    def ask(
        self,
        question: str,
        top_k: int = 3,
        source: str = None,
        history=None,
        user_email: str = None
    ):
        rewritten_question = self.rewrite_question(question, history)

        vector_results = self.vector_store.search(
            query=rewritten_question,
            top_k=top_k,
            source=source,
            user_email=user_email
        )

        vector_chunks = [doc.page_content for doc in vector_results]

        keyword_results = []
        if vector_chunks:
            keyword_search = KeywordSearchService(vector_chunks)
            keyword_results = keyword_search.search(rewritten_question, top_k=top_k)

        combined_chunks = vector_chunks + keyword_results
        unique_chunks = list(dict.fromkeys(combined_chunks))
        final_chunks = unique_chunks[:top_k]

        if not final_chunks:
            return {
                "rewritten_question": rewritten_question,
                "answer": "I could not find that information in your uploaded documents.",
                "cited_answer": "I could not find that information in your uploaded documents.",
                "sources": [],
                "retrieved_chunks": []
            }

        sources = []
        seen_sources = set()
        labeled_context_parts = []
        label_counter = 1

        for doc in vector_results:
            source_name = doc.metadata.get("source", "unknown")
            chunk_index = doc.metadata.get("chunk_index", -1)
            chunk_text = doc.page_content

            source_key = (source_name, chunk_index)

            if source_key not in seen_sources:
                seen_sources.add(source_key)

                label = f"S{label_counter}"
                label_counter += 1

                sources.append({
                    "label": label,
                    "source": source_name,
                    "chunk_index": chunk_index
                })

                labeled_context_parts.append(
                    f"[{label}] Source: {source_name}, Chunk: {chunk_index}\n{chunk_text}"
                )

        labeled_context = "\n\n".join(labeled_context_parts)

        final_prompt = RAG_PROMPT_TEMPLATE.format(
            context=labeled_context,
            question=rewritten_question
        )

        response = self.llm.invoke(final_prompt)

        cited_answer = response.content.strip() if hasattr(response, "content") else str(response).strip()

        if not cited_answer:
            cited_answer = "I could not generate an answer from the retrieved context."

        return {
            "rewritten_question": rewritten_question,
            "answer": cited_answer,
            "cited_answer": cited_answer,
            "sources": sources,
            "retrieved_chunks": final_chunks
        }