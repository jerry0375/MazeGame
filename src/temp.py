import collections
import math

# --- 模拟函数 ---
# 假设这是用户提供的计算 Boss 战消耗的函数
# 我们在此模拟一个，假设它总是返回 (True, 0, 10)，即消耗10金币
def fight_boss(B, PlayerSkills, cc1, cc2):
    """
    模拟计算击败Boss的最小金币消耗。
    在实际应用中，这里会是一个复杂的计算。
    返回: (True, 0, 10) - 假设总是成功，消耗10金币
    """
    # 模拟计算消耗
    min_cost = 10  # 假设固定消耗10金币
    return (True, 0, min_cost)

# --- 迷宫求解器 ---

def solve_maze(maze, c1, c2, gold_value, trap_penalty, B, PlayerSkills):

    H = len(maze)
    W = len(maze[0])
    
    # -----------------------------------------------------------------
    # 辅助函数：BFS 寻路
    # -----------------------------------------------------------------
    def bfs_pathfind(start_pos, target_locs, target_chars, known_map, avoid_locs):
        """
        一个通用的BFS寻路器。
        - 寻找从 start_pos 到 target_locs 中任意一个位置的最短路径。
        - 或寻找从 start_pos 到 known_map 上任意一个 target_chars 单元格的最短路径。
        - 返回：到达目标的路径上的“第一步”坐标 (r, c)，如果找不到则返回 None。
        """
        queue = collections.deque([start_pos])
        # parent_map 用于回溯路径，找到“第一步”
        parent_map = {start_pos: None}
        
        target_locs_set = set(target_locs)
        target_chars_set = set(target_chars)

        while queue:
            curr = queue.popleft()
            r, c = curr

            # 检查是否到达目标
            if curr in target_locs_set or known_map[r][c] in target_chars_set:
                # 找到了，回溯以找到“第一步”
                path = []
                temp = curr
                while parent_map[temp] is not None:
                    path.append(temp)
                    temp = parent_map[temp]
                
                if not path: # 目标就在原地（虽然不太可能在决策时发生）
                    return curr
                return path[-1] # 返回路径的最后一步（即 start_pos 的下一步）

            # 探索邻居
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 上下左右
                nr, nc = r + dr, c + dc
                
                n_pos = (nr, nc)
                
                if 0 <= nr < H and 0 <= nc < W and n_pos not in parent_map:
                    n_char = known_map[nr][nc]
                    
                    # 检查是否可通行
                    if n_char != 'W' and n_pos not in avoid_locs:
                        parent_map[n_pos] = curr
                        queue.append(n_pos)
        
        return None # 找不到路径

    # -----------------------------------------------------------------
    # 辅助函数：扫描3x3视野
    # -----------------------------------------------------------------
    def scan_vision(pos, true_maze, known_map):
        """
        更新 known_map 中 pos 周围 3x3 的信息。
        """
        r, c = pos
        new_boss_loc = None
        new_exit_loc = None

        for nr in range(r - 1, r + 2):
            for nc in range(c - 1, c + 2):
                if 0 <= nr < H and 0 <= nc < W:
                    # 只有当该位置未知时才更新（'U'）
                    if known_map[nr][nc] == 'U':
                        true_cell = true_maze[nr][nc]
                        
                        if true_cell == '#':
                            known_map[nr][nc] = 'W' # 墙
                        elif true_cell == 'G':
                            known_map[nr][nc] = 'G' # 金币
                        elif true_cell == 'B':
                            known_map[nr][nc] = 'B' # Boss
                            new_boss_loc = (nr, nc)
                        elif true_cell == 'E':
                            known_map[nr][nc] = 'E' # Exit
                            new_exit_loc = (nr, nc)
                        elif true_cell in (' ', 'T', 'S'):
                            # 陷阱T在视野中不可见，表现为普通路径
                            known_map[nr][nc] = 'P' # 路径
        
        return new_boss_loc, new_exit_loc

    # -----------------------------------------------------------------
    # 辅助函数：在迷宫中找到起始点
    # -----------------------------------------------------------------
    def find_start(maze):
        for r in range(H):
            for c in range(W):
                if maze[r][c] == 'S':
                    return (r, c)
        return (0, 0) # 容错

    # --- 1. 初始化状态 ---
    start_pos = find_start(maze)
    current_pos = start_pos
    path = [current_pos]
    steps = 0
    my_coins = 0

    boss_defeated = False
    boss_location = None
    exit_location = None
    boss_cost = float('inf')

    # 内部知识地图: 'U' (Unknown), 'W' (Wall), 'P' (Path), 'G' (Gold),
    # 'B' (Boss), 'E' (Exit), 'T_T' (Trap Triggered)
    known_map = [['U' for _ in range(W)] for _ in range(H)]

    # 真实陷阱位置 (用于模拟)
    trap_locations = set()
    for r in range(H):
        for c in range(W):
            if maze[r][c] == 'T':
                trap_locations.add((r, c))
    
    # 复制迷宫，用于追踪已拾取的金币
    maze_copy = [row[:] for row in maze]
    
    # Failsafe for infinite loops
    max_steps = H * W * 10 

    # --- 2. 主循环 (每一步决策) ---
    while steps < max_steps:
        r, c = current_pos

        # --- 2a. 事件：到达单元格 ---
        
        # 1. 踩陷阱 (规则5)
        if current_pos in trap_locations:
            my_coins -= trap_penalty
            trap_locations.remove(current_pos) # 陷阱失效
            known_map[r][c] = 'T_T' # 标记为已触发
        
        # 2. 捡金币 (规则6)
        if maze_copy[r][c] == 'G':
            my_coins += gold_value
            maze_copy[r][c] = ' ' # 金币消失
            known_map[r][c] = 'P' # 变为路径
        
        # 3. 标记为已访问路径
        if known_map[r][c] not in ('T_T', 'B', 'E'):
             known_map[r][c] = 'P'

        # --- 2b. 事件：扫描视野 (规则1) ---
        new_boss, new_exit = scan_vision(current_pos, maze_copy, known_map)
        
        if new_boss and boss_location is None:
            boss_location = new_boss
            # 规则4: 知道最优策略，计算消耗
            _, _, boss_cost = fight_boss(B, PlayerSkills, c1, c2)
            # print(f"Step {steps}: Boss found at {boss_location}, cost: {boss_cost}") # 调试信息
            
        if new_exit and exit_location is None:
            exit_location = new_exit
            # print(f"Step {steps}: Exit found at {exit_location}") # 调试信息

        # --- 2c. 事件：检查结束条件 (规则2) ---
        if current_pos == exit_location:
            if boss_defeated:
                break # 成功！
            else:
                # 到了出口，但Boss没打，必须离开
                pass 

        # --- 2d. 事件：战斗 (规则3) ---
        if current_pos == boss_location and not boss_defeated:
            if my_coins >= boss_cost:
                # print(f"Step {steps}: Fighting boss...") # 调试信息
                my_coins -= boss_cost
                boss_defeated = True
                known_map[r][c] = 'P' # Boss 变为路径
                boss_location = None # Boss 不再是目标
            else:
                # 到了Boss点，但钱不够，必须离开
                # print(f"Step {steps}: At boss, but not enough coins.") # 调试信息
                pass 

        # --- 2e. 贪心决策：决定下一步 ---
        target_locs = []
        target_chars = set()
        avoid_locs = set()

        if boss_defeated:
            # 阶段 3: 寻找出口
            if exit_location:
                target_locs = [exit_location]
            else:
                # 出口未知，退回探索模式
                target_chars = {'U'} 
        
        elif boss_location and my_coins >= boss_cost:
            # 阶段 2: 讨伐 Boss
            target_locs = [boss_location]
        
        else:
            # 阶段 1: 探索与积累
            target_chars = {'G', 'U'} # 优先找金币，其次探索
            
            # 规则3/4：如果钱不够，避开Boss
            if boss_location:
                avoid_locs.add(boss_location)
            # 规则2：如果Boss没打，避开出口
            if exit_location:
                avoid_locs.add(exit_location)

        # --- 2f. 寻路并移动 ---
        next_move = bfs_pathfind(current_pos, target_locs, target_chars, known_map, avoid_locs)

        if next_move is None:
            # 找不到路（例如被墙/陷阱完全包围，或迷宫无解）
            # print("Error: Greedy algorithm is stuck. No path found.") # 调试信息
            break # 迷宫可解，理论上不应发生

        # 执行移动
        current_pos = next_move
        path.append(current_pos)
        steps += 1
        
        # print(f"Step {steps}: Moved to {current_pos}, Coins: {my_coins}") # 调试信息

    # --- 3. 格式化输出 ---
    coinsPerStep = my_coins / steps if steps > 0 else 0
    
    return {
        "steps": steps,
        "coins": my_coins,
        "coinsPerStep": round(coinsPerStep, 2),
        "path": path
    }

# -----------------------------------------------------------------
# 示例运行
# -----------------------------------------------------------------
if __name__ == "__main__":
    
    # 示例输入
    maze = [
        ["#","#","#","#","E","#","#","#","#","#","#","#","#","#","#"],
        ["#"," "," "," "," "," "," "," "," "," ","#"," ","T"," ","#"],
        ["#"," ","#","#","#"," ","#","#","#"," ","#"," ","#","#","#"],
        ["#"," "," "," ","#"," ","#"," "," "," ","#"," "," "," ","S"],
        ["#"," ","#"," ","#"," ","#"," ","#","#","#"," ","#"," ","#"],
        ["#"," ","#","G","#"," ","#"," "," "," ","#"," ","#"," ","#"],
        ["#","#","#","#","#"," ","#","#","#"," ","#","#","#","B","#"],
        ["#"," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
        ["#","#","#","#","#","#","#","#","#"," ","#","#","#","#","#"],
        ["#"," "," "," "," "," "," "," ","G"," ","#"," "," "," ","#"],
        ["#"," ","#","#","#","#","#","#","#"," ","#","#","#"," ","#"],
        ["#"," ","#"," ","#","T"," "," "," "," ","#"," "," "," ","#"],
        ["#"," ","#"," ","#"," ","#","#","#"," ","#"," ","#","#","#"],
        ["#"," "," "," ","#","T","#"," "," "," "," "," ","G"," ","#"],
        ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"]
    ]
    
    # 模拟参数
    c1, c2 = 0.5, 0.5
    gold_value = 5
    trap_penalty = 3
    B = [100, 50] # 模拟Boss属性
    PlayerSkills = [[10, 0, 5], [5, 1, 4]] # 模拟玩家技能
    
    # 运行求解器
    result = solve_maze(maze, c1, c2, gold_value, trap_penalty, B, PlayerSkills)
    
    # 打印结果
    import json
    print(json.dumps(result, indent=2))