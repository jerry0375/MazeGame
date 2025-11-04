import yaml
from pathlib import Path
import random
from output_file import write_maze_file
# 迷宫符号
wall = '#'
path = ' '
start = 'S'
end = 'E'
gold = 'G'
trap = 'T'
boss = 'B'
# 输出路径
output_path = "./res/maze_data.json"

# --- 主生成函数 ---
def generate_maze():
    import random
    
    # 读取配置文件中的迷宫参数
    config = read_config()

    width = config['width']
    height = config['height']
    gold_count = config['gold_count']
    trap_count = config['trap_count']
    boss_count = config['boss_count']
    B = config['boss_health']
    PlayerSkills = config['player_skills']
    
    # 确保维度是奇数，以适应算法
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    # 1. 初始化一个开放的网格（所有都是路径）
    maze = [[path for _ in range(height)] for _ in range(width)]

    # 2. 建造“边界墙”
    for i in range(width):
        maze[i][0] = wall      # 左边界
        maze[i][height - 1] = wall # 右边界
    for j in range(height):
        maze[0][j] = wall      # 上边界
        maze[width - 1][j] = wall # 下边界

    # 3. 开始递归分割
    # 我们从内部的开放区域 (1, 1) 开始
    # 内部高度/宽度 = 总-2
    recursive_divide(maze, 1, 1, width - 2, height - 2)

    # 4. 放置起点，终点，金币，陷阱，boss
    place_elements(maze, gold_count, trap_count, boss_count)
    
    return maze, B, PlayerSkills

# 放置起点，终点，金币，陷阱，boss
def place_elements(maze, gold_count, trap_count, boss_count):
    width = len(maze)
    height = len(maze[0])
    
    def random_empty_cell():
        while True:
            r = random.randint(1, width - 2)
            c = random.randint(1, height - 2)
            if maze[r][c] == path:
                return (r, c)
    
    def random_boundary_cell():
        edges = []
        for i in range(1, width - 1):
            if maze[i][1] == path:
                edges.append((i, 0)) # 左边界
            if maze[i][height - 2] == path:
                edges.append((i, height - 1)) # 右边界
        for j in range(1, height - 1):
            if maze[1][j] == path:
                edges.append((0, j)) # 上边界
            if maze[width - 2][j] == path:
                edges.append((width - 1, j)) # 下边界
        return random.choice(edges)
    
    # 在边界放置起点和终点
    sr, sc = random_boundary_cell()
    maze[sr][sc] = start
    er, ec = random_boundary_cell()
    while (er, ec) == (sr, sc):
        er, ec = random_boundary_cell()
    maze[er][ec] = end
    
    # 放置金币
    for _ in range(gold_count):
        gr, gc = random_empty_cell()
        maze[gr][gc] = gold
    
    # 放置陷阱
    for _ in range(trap_count):
        tr, tc = random_empty_cell()
        maze[tr][tc] = trap
    
    # 放置boss
    for _ in range(boss_count):
        br, bc = random_empty_cell()
        maze[br][bc] = boss

# --- 核心的分治算法 ---
def recursive_divide(grid, r, c, h, w):
    """
    在给定的网格区域内递归地生成墙壁。

    参数:
    grid (list[list]): 迷宫网格
    r (int): 当前区域的起始行 (奇数)
    c (int): 当前区域的起始列 (奇数)
    h (int): 当前区域的高度 (路径高度)
    w (int): 当前区域的宽度 (路径宽度)
    """

    # 1. 查找可能的墙壁位置
    # 墙壁必须放在偶数索引上
    # 它们必须在当前区域的“内部”
    
    # r=1, h=5 (行 1,2,3,4,5)。可能的墙行：2, 4
    possible_h_walls = [i for i in range(r + 1, r + h - 1) if i % 2 == 0]
    # c=1, w=5 (列 1,2,3,4,5)。可能的墙列：2, 4
    possible_v_walls = [i for i in range(c + 1, c + w - 1) if i % 2 == 0]

    # 2. 基本情况 (Base Case)
    # 如果没有地方可以画墙（区域太小），则停止递归
    if not possible_h_walls and not possible_v_walls:
        return

    # 3. 决定分割方向
    orientation = None
    if not possible_h_walls:
        orientation = 'VERTICAL'
    elif not possible_v_walls:
        orientation = 'HORIZONTAL'
    else:
        # 优先分割较长的维度，以产生更有趣的迷宫
        if w > h:
            orientation = 'VERTICAL'
        elif h > w:
            orientation = 'HORIZONTAL'
        else:
            # 如果是正方形，随机选择
            orientation = random.choice(['HORIZONTAL', 'VERTICAL'])

    # 4. 执行分割 (Divide & Conquer)
    if orientation == 'HORIZONTAL':
        # (a) 选择一个偶数行来画水平墙
        wr = random.choice(possible_h_walls)
        
        # (b) 选择一个奇数列来开“门”
        possible_passages = [i for i in range(c, c + w) if i % 2 != 0]
        pc = random.choice(possible_passages)
        
        # (c) 画墙，并打开门
        for j in range(c, c + w):
            grid[wr][j] = wall
        grid[wr][pc] = path  # 打开门

        # (d) 递归处理上下两个子区域
        # 顶部区域
        recursive_divide(grid, r, c, wr - r, w)
        # 底部区域
        recursive_divide(grid, wr + 1, c, (r + h) - (wr + 1), w)

    else: # 'VERTICAL'
        # (a) 选择一个偶数列来画垂直墙
        wc = random.choice(possible_v_walls)
        
        # (b) 选择一个奇数行来开“门”
        possible_passages = [i for i in range(r, r + h) if i % 2 != 0]
        pr = random.choice(possible_passages)
        
        # (c) 画墙，并打开门
        for i in range(r, r + h):
            grid[i][wc] = wall
        grid[pr][wc] = path  # 打开门
        
        # (d) 递归处理左右两个子区域
        # 左侧区域
        recursive_divide(grid, r, c, h, wc - c)
        # 右侧区域
        recursive_divide(grid, r, wc + 1, h, (c + w) - (wc + 1))

# 读取配置文件中的迷宫参数
def read_config():
    import sys
    # 配置文件地址 - 兼容打包后的环境
    if getattr(sys, 'frozen', False):
        # 打包后的 exe 环境
        config_path = Path(sys.executable).parent / "config.yaml"
    else:
        # 开发环境
        config_path = Path(__file__).parent.parent / "config.yaml"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    # 读取迷宫环境参数
    width = config_data.get('width')   # 迷宫宽度
    height = config_data.get('height') # 迷宫高度
    gold_count = config_data.get('gold_count') # 迷宫中金币数量
    trap_count = config_data.get('trap_count') # 迷宫中陷阱数量
    boss_count = config_data.get('boss_count') # 迷宫中boss数量
    
    # 读取第 13-14 行的数据（boss 属性和玩家技能）
    boss_health = config_data.get('boss_health')
    player_skills = config_data.get('player_skills')
    
    config = {
        'width': width,
        'height': height,
        'gold_count': gold_count,
        'trap_count': trap_count,
        'boss_count': boss_count,
        'boss_health': boss_health,
        'player_skills': player_skills
    }
    return config    

# 迷宫生成主函数
def main_maze_generate():
    import sys
    maze, B, PlayerSkills = generate_maze()
    
    # 确定输出路径 - 兼容打包后的环境
    if getattr(sys, 'frozen', False):
        # 打包后的 exe 环境
        output_dir = Path(sys.executable).parent / "res"
    else:
        # 开发环境
        output_dir = Path(__file__).parent.parent / "res"
    
    # 确保 res 目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = output_dir / "maze_data.json"
    print(f"Writing maze data to: {filepath}")
    write_maze_file(filepath, maze, B, PlayerSkills)
    return maze, B, PlayerSkills

# 测试生成迷宫
if __name__ == "__main__":
    # maze, B, PlayerSkills = generate_maze()
    # for row in maze:
    #     print(' '.join(row))
    main_maze_generate()









