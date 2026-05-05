import pickle
import networkx as nx
import matplotlib.pyplot as plt
import os
from NodeRAG.config import NodeConfig

def visualize_kg():
    config = NodeConfig.from_main_folder(".")
    graph_path = os.path.join(config.cache, "graph.pkl")
    
    if not os.path.exists(graph_path):
        print("Graph not found.")
        return

    with open(graph_path, 'rb') as f:
        G = pickle.load(f)

    # Lấy một tập con các node để vẽ cho đẹp (ví dụ 30 node đầu tiên)
    nodes_to_show = list(G.nodes())[:30]
    sub_G = G.subgraph(nodes_to_show)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(sub_G, k=1, seed=42)
    
    # Vẽ các node
    nx.draw_networkx_nodes(sub_G, pos, node_size=1500, node_color='skyblue', alpha=0.8)
    
    # Vẽ các cạnh
    nx.draw_networkx_edges(sub_G, pos, width=1, alpha=0.5, edge_color='gray')
    
    # Vẽ nhãn
    labels = {node: str(node)[:15] for node in sub_G.nodes()}
    nx.draw_networkx_labels(sub_G, pos, labels, font_size=8, font_family='sans-serif')

    plt.title("Trực quan hóa một phần Đồ thị Tri thức (NodeRAG)")
    plt.axis('off')
    
    # Lưu hình ảnh
    output_path = "kg_visualization.png"
    plt.savefig(output_path)
    print(f"[*] Đã lưu hình ảnh trực quan hóa đồ thị tại {output_path}")

if __name__ == "__main__":
    visualize_kg()
