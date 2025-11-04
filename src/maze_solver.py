"""
使用贪心算法实现迷宫求解
规则
1. 玩家仅拥有3x3的视野,探索过的区域将被照亮
2. 玩家从入口出发,击败boss后,才能出迷宫
3. 玩家发现boss可以选择探索后再来处理boss
4. 假设玩家发现boss后立刻知道最低消耗的金币
5. 假设陷阱不可见且陷阱触发后不会第二次扣去玩家金币,金币可见,迷宫可解
"maze": [
["#", "#", "#", "#", "#", "#", "#"],
["S", "T", " ", " ", " ", "T", "#"],
["#", "#", "#", "#", "#", "G", "#"],
["#", " ", " ", "G", "T", " ", "#"],
["#", "#", "#", "G", "#", " ", "#"],
["#", "B", " ", "G", "#", "G", "#"],
["#", "#", "E", "#", "#", "#", "#"]
]
返回数据示例:
"steps": 4,
"coins": 10,
"coinsPerStep": 2.5,
"path": [
[0, 0],
[0, 1],
[1, 1],
[2, 1]
]
"""

from fight_boss import main_fight_boss
import read_file as rf
from collections import deque
from pathlib import Path
from output_file import write_solve_path

def solve_maze(maze, c1, c2, gold_value, trap_penalty, B, PlayerSkills):
    height = len(maze)
    width = len(maze[0])
    
    start_pos, boss_pos, end_pos = None, None, None
    gold_positions = []
    
    for r in range(height):
        for c in range(width):
            if maze[r][c] == 'S':
                start_pos = (r, c)
            elif maze[r][c] == 'B':
                boss_pos = (r, c)
            elif maze[r][c] == 'E':
                end_pos = (r, c)
            elif maze[r][c] == 'G':
                gold_positions.append((r, c))

    if not start_pos or not boss_pos or not end_pos:
        return [], 0, 0, 0.0

    # 模拟战斗以获取成本
    _, boss_fight_rounds, boss_fight_coins = main_fight_boss(B, PlayerSkills, c1, c2)
    
    # BFS寻找从start到target的最短路径
    def bfs_path(start, target):
        queue = deque([(start, [start])])
        visited_bfs = {start}
        
        while queue:
            pos, path_to_pos = queue.popleft()
            
            if pos == target:
                return path_to_pos
            
            r, c = pos
            # 4个方向移动（上下左右）
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_pos = (r + dr, c + dc)
                nr, nc = next_pos
                
                # 检查边界、障碍物
                if (0 <= nr < height and 0 <= nc < width and 
                    maze[nr][nc] != '#' and 
                    next_pos not in visited_bfs):
                    
                    visited_bfs.add(next_pos)
                    queue.append((next_pos, path_to_pos + [next_pos]))
        
        return None  # 无法到达
    
    # 使用DFS遍历所有可达位置，收集所有金币
    def dfs_explore():
        stack = [start_pos]
        visited_explore = {start_pos}
        exploration_path = [start_pos]
        
        while stack:
            current = stack[-1]
            r, c = current
            
            # 查找未访问的邻居
            found_unvisited = False
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_pos = (r + dr, c + dc)
                nr, nc = next_pos
                
                if (0 <= nr < height and 0 <= nc < width and 
                    maze[nr][nc] != '#' and 
                    next_pos not in visited_explore):
                    
                    visited_explore.add(next_pos)
                    stack.append(next_pos)
                    exploration_path.append(next_pos)
                    found_unvisited = True
                    break
            
            if not found_unvisited:
                # 回溯
                stack.pop()
                if stack:
                    # 添加回溯路径
                    backtrack_path = bfs_path(current, stack[-1])
                    if backtrack_path and len(backtrack_path) > 1:
                        exploration_path.extend(backtrack_path[1:])
        
        return exploration_path
    
    # 第一阶段：遍历全图收集金币
    full_path = dfs_explore()
    
    # 计算遍历过程中的金币和陷阱
    visited = set()
    coins = 0
    boss_defeated = False
    
    for pos in full_path:
        if pos not in visited:
            cell_content = maze[pos[0]][pos[1]]
            
            if cell_content == 'G':
                coins += gold_value
            elif cell_content == 'T':
                coins -= trap_penalty
            elif cell_content == 'B' and not boss_defeated:
                # 路过Boss时检查金币是否足够
                if coins >= boss_fight_coins:
                    boss_defeated = True
                    coins -= boss_fight_coins
            
            visited.add(pos)
    
    # 第二阶段：如果Boss未击败，先去Boss再去出口
    current_pos = full_path[-1]
    
    if not boss_defeated:
        # 前往Boss
        path_to_boss = bfs_path(current_pos, boss_pos)
        if path_to_boss and len(path_to_boss) > 1:
            full_path.extend(path_to_boss[1:])
            
            # 处理路径上的新格子
            for pos in path_to_boss[1:]:
                if pos not in visited:
                    cell_content = maze[pos[0]][pos[1]]
                    if cell_content == 'G':
                        coins += gold_value
                    elif cell_content == 'T':
                        coins -= trap_penalty
                    visited.add(pos)
            
            # 击败Boss
            if coins >= boss_fight_coins:
                boss_defeated = True
                coins -= boss_fight_coins
            
            current_pos = boss_pos
    
    # 第三阶段：前往出口
    if current_pos != end_pos:
        path_to_exit = bfs_path(current_pos, end_pos)
        if path_to_exit and len(path_to_exit) > 1:
            full_path.extend(path_to_exit[1:])
            
            # 处理路径上的新格子
            for pos in path_to_exit[1:]:
                if pos not in visited:
                    cell_content = maze[pos[0]][pos[1]]
                    if cell_content == 'G':
                        coins += gold_value
                    elif cell_content == 'T':
                        coins -= trap_penalty
                    visited.add(pos)
    
    # 计算最终结果
    steps = len(full_path)
    coinsPerStep = round(coins / steps, 2) if steps > 0 else 0.0
    
    return full_path, steps, coins, coinsPerStep

def main_maze_solver(maze, c1, c2, gold_value, trap_penalty, B, PlayerSkills):
    import sys
    path, steps, coins, coinsPerStep = solve_maze(maze, c1, c2, gold_value, trap_penalty, B, PlayerSkills)
    
    # 确定输出路径 - 兼容打包后的环境
    if getattr(sys, 'frozen', False):
        # 打包后的 exe 环境
        output_dir = Path(sys.executable).parent / "res"
    else:
        # 开发环境
        output_dir = Path(__file__).parent.parent / "res"
    
    # 确保 res 目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    fp = output_dir / "solve_data.json"
    write_solve_path(fp, path, coins, steps, coinsPerStep)
    return path, steps, coins, coinsPerStep    
    

if __name__ == "__main__":
    from pathlib import Path
    fp = Path(__file__).parent.parent / "config.yaml"
    print(fp)
    config = rf.read_config_file(fp)
    # B = config('boss_health')
    c1 = config['c1']
    c2 = config['c2']
    gold_value = config['gold_value']
    trap_penalty = config['trap_penalty']
    # PlayerSkills = config('player_skills')

    # fp = Path(__file__).parent.parent / config['maze_file']
    fp = "C:\\Users\\Administrator\\Desktop\\MazeGame\\testData\\maze_7_7.json"
    print(fp)
    maze, B, PlayerSkills = rf.read_maze_file(fp)

    path, steps, coins, coinsPerStep = main_maze_solver(maze, c1, c2, gold_value, trap_penalty, B, PlayerSkills)

    print("Steps:", steps)
    print("Coins:", coins)
    print("Coins per Step:", coinsPerStep)
    print("Path:", path)




