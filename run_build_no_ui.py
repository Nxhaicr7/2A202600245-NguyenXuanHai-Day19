import asyncio
from NodeRAG.config import NodeConfig
from NodeRAG.build.Node import NodeRag, State

async def run_build_manual():
    # Load config
    config = NodeConfig.from_main_folder(".")
    
    # Khởi tạo NodeRag
    node = NodeRag(config)
    
    # Bắt đầu pipeline mà không hiển thị cây trạng thái (bỏ qua bước hỏi y/n)
    print("[*] Bắt đầu quá trình xây dựng đồ thị (Bỏ qua UI)...")
    
    # Tương đương với node._run_async() nhưng không có display_state_tree()
    from NodeRAG.build.pipeline import INIT_pipeline
    node.Is_incremental = await INIT_pipeline(node.config).main()
    
    # Chạy transition
    await node.state_transition()

if __name__ == "__main__":
    asyncio.run(run_build_manual())
