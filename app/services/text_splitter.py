from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitterService:
    @staticmethod
    def split_text(text: str):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        return splitter.split_text(text)