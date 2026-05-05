import asyncio
import json
from flat_rag import FlatRAG
from custom_retrieval import custom_graph_search

questions = [
    "Ai là người sáng lập ra công ty thuộc ngành khách sạn và được thành lập vào năm 1876?",
    "Mối quan hệ giữa J. C. Jacobsen và ngành công nghiệp đồ uống là gì?",
    "Công ty Carlsberg Group và Heineken, công ty nào được thành lập sớm hơn và ai là người sáng lập của chúng?",
    "Liệt kê các công ty ở Đan Mạch và ngành công nghiệp chính của họ.",
    "Người sáng lập của Beck's có liên quan gì đến ngành công nghiệp sản xuất bia không?"
]

async def run_comparison():
    print("[*] Đang khởi tạo Flat RAG...")
    flat_rag = FlatRAG()
    
    results = []

    for i, q in enumerate(questions):
        print(f"\n--- Câu hỏi {i+1}: {q} ---")
        
        print("[Flat RAG] Đang xử lý...")
        flat_ans = await flat_rag.search(q)
        
        print("[GraphRAG] Đang xử lý...")
        graph_ans = await custom_graph_search(q)
        
        results.append({
            "id": i + 1,
            "question": q,
            "flat_rag": flat_ans,
            "graph_rag": graph_ans
        })

    # Lưu kết quả ra file json để phân tích
    with open("comparison_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print("\n[*] Đã hoàn thành so sánh. Kết quả được lưu tại comparison_results.json")

if __name__ == "__main__":
    asyncio.run(run_comparison())
