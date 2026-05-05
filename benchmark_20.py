import asyncio
import json
from flat_rag import FlatRAG
from custom_retrieval import custom_graph_search

questions = [
    "Who founded Carlsberg Group?",
    "When was Heineken founded?",
    "What is the main industry of Goldman Sachs?",
    "Where is Hotel Sacher located?",
    "Who is the founder of Beck's?",
    "What are the industries associated with Kasikornbank?",
    "In which country is A. Le Coq located?",
    "When was Sberbank founded?",
    "What type of company is HSBC?",
    "Who founded Hotel Sacher?",
    "What is the website of Deutsche Bank?",
    "Is Carlsberg Group in the beverage industry?",
    "What is the description of Goldman Sachs?",
    "Which city is Hotel Sacher in?",
    "What are the industries of Sberbank?",
    "Who founded Kasikornbank?",
    "What is the website of Carlsberg Group?",
    "When was Deutsche Bank founded?",
    "Is Heineken a Dutch company?",
    "What is the primary sector of Goldman Sachs?"
]

async def run_benchmark():
    flat_rag = FlatRAG()
    results = []

    for i, q in enumerate(questions):
        print(f"[*] Processing Q{i+1}: {q}")
        flat_ans = await flat_rag.search(q)
        graph_ans = await custom_graph_search(q)
        
        results.append({
            "id": i + 1,
            "question": q,
            "flat_rag": flat_ans,
            "graph_rag": graph_ans
        })

    with open("benchmark_20_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
