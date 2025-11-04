import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
import maze_generate as mg
import maze_solver as ms
import fight_boss as fb
import read_file as rf
from pathlib import Path
import argparse

# 获取应用程序根目录（兼容 PyInstaller 打包后的环境）
def get_app_root():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe 文件
        return Path(sys.executable).parent
    else:
        # 如果是 Python 脚本
        return Path(__file__).parent

def main():
    # 获取应用根目录
    app_root = get_app_root()
    
    # 读取迷宫配置文件中的参数
    config_path = app_root / "config.yaml"
    if not config_path.exists():
        print(f"Error: Configuration file not found at {config_path}")
        print("Please ensure config.yaml is in the same directory as the executable.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    config = rf.read_config_file(config_path)
    c1 = config['c1']
    c2 = config['c2']
    gold_value = config.get('gold_value')
    trap_penalty = config.get('trap_penalty')
    maze_file_path = Path(config['maze_file'])
    use_default = config.get('use_default')

    if args.use_default or use_default:
        print("Using default configuration to generate maze.")
        # 生成迷宫并获取 Boss 信息和玩家技能
        maze, B, PlayerSkills = mg.main_maze_generate()
    else:
        if not maze_file_path.is_absolute():
            fp = app_root / maze_file_path
        else:
            fp = maze_file_path
        print(f"Using maze file: {fp}")
        
        if not fp.exists():
            print(f"Error: Maze file not found at {fp}")
            input("Press Enter to exit...")
            sys.exit(1)
        
        maze, B, PlayerSkills = rf.read_maze_file(fp)

    # 与 Boss 战斗
    skillSequence, rounds, coinsConsumed = fb.main_fight_boss(B, PlayerSkills, c1, c2)
    
    # 求解迷宫路径
    path, steps, coins, coinsPerStep = ms.main_maze_solver(maze, c1, c2, gold_value, trap_penalty, B, PlayerSkills)

    # 打印结果
    print("\nMaze:")
    for row in maze:
        print(' '.join(row))
    print("\nMaze Solving Results:")
    print(f"Path: {path}")
    print(f"Steps: {steps}")
    print(f"Coins: {coins}")
    print(f"Coins per Step: {coinsPerStep}")
    print("\nBoss Fight Results:")
    print(f"Skill Sequence: {skillSequence}")
    print(f"Total Rounds: {rounds}")
    print(f"Total Coins Consumed: {coinsConsumed}")

    # 打印结果文件位置
    res_dir = app_root / "res"
    print(f"\nResult files have been saved to: {res_dir}")
    print(f"  - Maze data: {res_dir / 'maze_data.json'}")
    print(f"  - Boss fight result: {res_dir / 'fight_data.json'}")
    print(f"  - Maze solution: {res_dir / 'solve_data.json'}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Maze Game Main Execution", 
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parse.add_argument('--use_default', type = int, default = 0, choices=[0,1],
                       help = "是否使用默认迷宫配置文件")
    args = parse.parse_args()
    main()


