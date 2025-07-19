import os
from membase.knowledge.chroma import ChromaKnowledgeBase
from membase.knowledge.document import Document

class TextRAG:
    def __init__(
        self,
        rag_input,
        persist_directory="./chroma_db_text",
        collection_name="text_store",
        membase_account=None,
        auto_upload_to_hub=False,
    ):
        if membase_account:
            os.environ["MEMBASE_ACCOUNT"] = membase_account
        self.rag_input = rag_input
        self.rag = ChromaKnowledgeBase(
            persist_directory=persist_directory,
            collection_name=collection_name,
            membase_account=os.getenv("MEMBASE_ACCOUNT"),
            auto_upload_to_hub=auto_upload_to_hub,
        )

    def add_text(self,doc_id: str = "text_doc"):
        doc = Document(doc_id=doc_id, content=self.rag_input, metadata={"source": "raw_text"})
        self.rag.add_documents(doc)
        print(f"Document '{doc_id}' added to vectorstore.")

    def query(self, query: str, top_k: int = 5):
        results = self.rag.retrieve(query, top_k=top_k)
        return [
            {
                "name": doc.doc_id,
                "content": doc.content[:300],
                "metadata": doc.metadata
            }
            for doc in results
        ]


# Example usage
if __name__ == "__main__":
    sample_text = """
    Floks is an agentic workflow automation tool that integrates AI and blockchain for secure task management.
    It enables users to design decentralized workflows, track data lineage, and automate decisions.
    """
    query = "What is Floks?"
    rag = TextRAG(membase_account="sarathc")
    rag.add_text(sample_text, doc_id="floks_doc")
    results = rag.query(query)

    for idx, res in enumerate(results):
        print(f"\nResult {idx+1}:\n{res['content']}\n---")
