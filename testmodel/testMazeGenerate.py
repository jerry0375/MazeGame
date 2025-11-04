import random

# --- 常量定义 ---
wall = 1  # 墙
path = 0  # 路径

# --- 打印函数 ---
def print_maze(grid, wall_char='*', path_char=' '):
    """
    以美观的方式打印迷宫网格。
    """
    for row in grid:
        # 将 1 替换为墙壁字符， 0 替换为路径字符
        line = " ".join([wall_char if cell == wall else path_char for cell in row])
        print(line)

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

# --- 主生成函数 ---
def generate_maze(width, height):
    """
    生成一个指定大小的迷宫。
    """
    # 确保维度是奇数，以适应算法
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    # 1. 初始化一个开放的网格（所有都是路径）
    grid = [[path for _ in range(height)] for _ in range(width)]

    # 2. 建造“边界墙”
    for i in range(width):
        grid[i][0] = wall      # 左边界
        grid[i][height - 1] = wall # 右边界
    for j in range(height):
        grid[0][j] = wall      # 上边界
        grid[width - 1][j] = wall # 下边界

    # 3. 开始递归分割
    # 我们从内部的开放区域 (1, 1) 开始
    # 内部高度/宽度 = 总-2
    recursive_divide(grid, 1, 1, width - 2, height - 2)

    return grid

# --- 执行 ---
if __name__ == "__main__":
    ROWS = 15
    COLS = 15
    
    print(f"正在生成一个 {ROWS}x{COLS} 的迷宫...")
    maze = generate_maze(ROWS, COLS)
    
    # 打印迷宫
    print_maze(maze)