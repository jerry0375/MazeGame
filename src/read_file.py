import json
import yaml

# 读取json文件中的迷宫信息
def read_maze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        maze = data.get('maze', [])
        B = data.get('B', [])
        PlayerSkills = data.get('PlayerSkills', [])
        return maze, B, PlayerSkills
    
def read_config_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config







