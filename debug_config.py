import yaml
import os
from NodeRAG.config import NodeConfig

with open('Node_config.yaml', 'r') as f:
    config_dict = yaml.safe_load(f)

print("Model Config api_keys:", config_dict['model_config'].get('api_keys'))
print("Embedding Config api_keys:", config_dict['embedding_config'].get('api_keys'))

try:
    node_config = NodeConfig(config_dict)
    print("NodeConfig initialized successfully")
    node_config.config_integrity()
    print("Config integrity check passed")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
