import os
import pickle
import asyncio
import pandas as pd
import networkx as nx
from dotenv import load_dotenv
from NodeRAG.config import NodeConfig

load_dotenv() # Load API keys from .env

async def custom_graph_search(question: str):
    # 1. Khởi tạo Config và API Client
    config = NodeConfig.from_main_folder(".")
    api_client = config.API_client
    
    graph_path = config.graph_path
    if not os.path.exists(graph_path):
        graph_path = os.path.join(config.cache, "graph.pkl")
    
    if not os.path.exists(graph_path):
        return "Lỗi: Đồ thị chưa được xây dựng. Vui lòng chạy build trước."

    # 2. Trích xuất thực thể chính từ câu hỏi bằng LLM
    extract_prompt = f"""Extract the main entity from the following question. 
Return ONLY the name of the entity, nothing else.
Question: {question}
Entity:"""
    
    entity_name = await api_client({'query': extract_prompt})
    entity_name = entity_name.strip().strip('"').strip("'")
    print(f"[*] Thực thể trích xuất được: {entity_name}")

    # 3. Tìm hash_id của thực thể từ entities.parquet
    entities_df = pd.read_parquet(config.entities_path)
    # Tìm thực thể khớp nhất trong cột 'context'
    matches = entities_df[entities_df['context'].str.contains(entity_name, case=False, na=False)]
    
    if matches.empty:
        return f"Không tìm thấy thông tin về '{entity_name}' trong dữ liệu thực thể."
    
    target_node_id = matches.iloc[0]['hash_id']
    actual_name = matches.iloc[0]['context']
    print(f"[*] Khớp với thực thể trong đồ thị: {actual_name} (ID: {target_node_id[:8]}...)")

    # 4. Tải đồ thị và duyệt 2-hop
    with open(graph_path, 'rb') as f:
        G = pickle.load(f)

    if target_node_id not in G:
        return f"Node ID {target_node_id} không tồn tại trong file đồ thị."

    # Duyệt 2-hop
    hop1 = list(G.neighbors(target_node_id))
    all_related_nodes = {target_node_id}.union(set(hop1))
    for n in hop1:
        all_related_nodes.update(G.neighbors(n))
    
    # 5. Thu thập thông tin bộ ba (Triples)
    # Trong NodeRAG: Entity1 (hash) --edge-- RelationshipNode (hash) --edge-- Entity2 (hash)
    # Chúng ta cần lấy context của các node này để tạo câu văn
    
    # Tạo bản đồ hash_id -> context
    id_to_context = dict(zip(entities_df['hash_id'], entities_df['context']))
    
    # Lấy thêm context của các quan hệ từ relationship.parquet
    rel_df = pd.read_parquet(config.relationship_path)
    rel_id_to_context = dict(zip(rel_df['hash_id'], rel_df['context']))
    
    knowledge_triples = []
    processed_rels = set()

    for node in all_related_nodes:
        # Nếu node là một relationship node
        if node in rel_id_to_context:
            # Tìm source và target kết nối với nó
            neighbors = list(G.neighbors(node))
            # Lọc ra các entity node (bỏ qua chính nó hoặc các node ko phải thực thể)
            linked_entities = [n for n in neighbors if n in id_to_context]
            
            if len(linked_entities) >= 2:
                s_name = id_to_context[linked_entities[0]]
                t_name = id_to_context[linked_entities[1]]
                rel_desc = rel_id_to_context[node]
                knowledge_triples.append(f"- {rel_desc}") # rel_desc thường đã chứa "Source relation Target"
            elif len(linked_entities) == 1:
                # Nếu chỉ tìm thấy 1 đầu kết nối
                s_name = id_to_context[linked_entities[0]]
                rel_desc = rel_id_to_context[node]
                knowledge_triples.append(f"- Liên quan đến {s_name}: {rel_desc}")

    # 6. Gộp thông tin và gửi LLM
    context_str = "\n".join(list(set(knowledge_triples))) # Bỏ trùng lặp
    if not context_str:
        context_str = f"Thực thể {actual_name} tồn tại nhưng chưa có các mối quan hệ chi tiết được lập chỉ mục."

    final_prompt = f"""Bạn là một trợ lý thông minh. Dưới đây là dữ liệu thu thập được từ Đồ thị tri thức (Knowledge Graph) về thực thể '{actual_name}':

{context_str}

Hãy dựa trên dữ liệu trên để trả lời câu hỏi của người dùng. Nếu dữ liệu không đủ, hãy trả lời dựa trên kiến thức của bạn nhưng ưu tiên thông tin từ đồ thị.
Câu hỏi: {question}
Trả lời:"""

    print("[*] Đang tổng hợp câu trả lời từ LLM...")
    answer = await api_client({'query': final_prompt})
    return answer
