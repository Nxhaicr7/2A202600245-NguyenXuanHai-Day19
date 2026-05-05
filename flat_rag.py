import os
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from NodeRAG.config import NodeConfig

load_dotenv()

class FlatRAG:
    def __init__(self):
        self.config = NodeConfig.from_main_folder(".")
        self.api_key = self.config.embedding_config['api_keys']
        self.client = OpenAI(api_key=self.api_key)
        self.index = None
        self.documents = []
        self.embedding_model = "text-embedding-3-small"
        
        self._build_index()

    def _get_embedding(self, text):
        response = self.client.embeddings.create(
            input=[text],
            model=self.embedding_model
        )
        return response.data[0].embedding

    def _build_index(self):
        corpus_path = "input/corpus.txt"
        if not os.path.exists(corpus_path):
            print("Corpus not found.")
            return

        with open(corpus_path, "r", encoding="utf-8") as f:
            self.documents = [line.strip() for line in f if line.strip()]

        embeddings = []
        print(f"[*] Đang tạo vector cho {len(self.documents)} dòng văn bản...")
        # Xử lý theo batch để nhanh hơn
        batch_size = 50
        for i in range(0, len(self.documents), batch_size):
            batch = self.documents[i:i+batch_size]
            response = self.client.embeddings.create(
                input=batch,
                model=self.embedding_model
            )
            embeddings.extend([res.embedding for res in response.data])

        embeddings = np.array(embeddings).astype('float32')
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        print("[*] Đã xây dựng xong Flat Index.")

    async def search(self, question, k=5):
        query_vector = np.array([self._get_embedding(question)]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        retrieved_docs = [self.documents[i] for i in indices[0] if i != -1]
        context = "\n".join(retrieved_docs)
        
        prompt = f"""Dựa trên các đoạn văn bản sau, hãy trả lời câu hỏi. 
Nếu không có thông tin, hãy nói bạn không biết, đừng bịa đặt.

Ngữ cảnh:
{context}

Câu hỏi: {question}
Trả lời:"""

        # Sử dụng API_client từ NodeConfig để đồng nhất model
        response = await self.config.API_client({'query': prompt})
        return response

if __name__ == "__main__":
    import asyncio
    rag = FlatRAG()
    # print(asyncio.run(rag.search("Who founded Carlsberg?")))
