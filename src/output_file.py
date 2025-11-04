# 创建json文件,写入迷宫信息
import json

def write_maze_file(file_path, maze, B, PlayerSkills):
    # 手动构建紧凑格式的 JSON 字符串
    lines = ['{']
    
    # 写入 maze,每行一个数组
    lines.append('  "maze": [')
    for i, row in enumerate(maze):
        row_json = json.dumps(row, ensure_ascii=False)
        if i < len(maze) - 1:
            lines.append(f'    {row_json},')
        else:
            lines.append(f'    {row_json}')
    lines.append('  ],')
    
    # 写入 B,单行
    b_json = json.dumps(B, ensure_ascii=False)
    lines.append(f'  "B": {b_json},')
    
    # 写入 PlayerSkills,单行
    skills_json = json.dumps(PlayerSkills, ensure_ascii=False)
    lines.append(f'  "PlayerSkills": {skills_json}')
    
    lines.append('}')
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
        f.write('\n')

def write_fight_boss_result(file_path, skillSequence, rounds, coinsConsumed):
    # 手动构建紧凑格式的 JSON 字符串
    lines = ['{']
    
    # 写入 skillSequence，单行
    sequence_json = json.dumps(skillSequence, ensure_ascii=False)
    lines.append(f'  "skillSequence": {sequence_json},')
    
    # 写入 rounds，单行
    lines.append(f'  "rounds": {rounds},')
    
    # 写入 coinsConsumed，单行
    lines.append(f'  "coinsConsumed": {coinsConsumed}')
    
    lines.append('}')
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
        f.write('\n')

def write_solve_path(file_path, path, coins, steps, coinsPerStep):
    # 手动构建紧凑格式的 JSON 字符串
    lines = ['{']

    # 写入 steps，单行
    lines.append(f'  "steps": {steps},')
    
    # 写入 coins，单行
    lines.append(f'  "coins": {coins},')
    
    # 写入 coinsPerStep，保留两位小数

    lines.append(f'  "coinsPerStep": {coinsPerStep},')
    
    # 写入 path，每行一个数组
    lines.append('  "path": [')
    for i, position in enumerate(path):
        pos_json = json.dumps(position, ensure_ascii=False)
        if i < len(path) - 1:
            lines.append(f'    {pos_json},')
        else:
            lines.append(f'    {pos_json}')
    lines.append('  ]')
    
    lines.append('}')
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
        f.write('\n')





