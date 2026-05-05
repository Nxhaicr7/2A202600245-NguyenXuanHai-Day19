import asyncio
from custom_retrieval import custom_graph_search

async def main():
    print("--- Chế độ truy vấn Đồ thị tri thức (Custom 2-hop) ---")
    while True:
        question = input("\nNhập câu hỏi của bạn (hoặc 'exit' để thoát): ")
        if question.lower() == 'exit':
            break
        
        try:
            answer = await custom_graph_search(question)
            print(f"\n[🤖 Trả lời]:\n{answer}")
        except Exception as e:
            print(f"Lỗi: {e}")

if __name__ == "__main__":
    asyncio.run(main())
