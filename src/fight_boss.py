from pathlib import Path
from output_file import write_fight_boss_result
"""
boss属性和玩家属性
boss_health: [10,5,3,6]
player_skills: [[10,3,9],[5,2,5],[3,1,4]] # [攻击力, 冷却值(接下来n回合无法施法), 金币消耗]
实现一个简单的战斗模拟，返回技能使用顺序，回合数，金币消耗总量
要求尽可能少的回合数和金币消耗（建模为线性多目标规划）
规则：
- 每回合可以使用一个技能，技能有冷却时间和金币消耗
- 每个boss需要被击败后才能进入下一个boss战斗
- 技能在使用后进入冷却状态，冷却时间结束后才能再次使用
- 玩家可以选择跳过回合以减少技能冷却时间
目标：
- 击败所有boss
返回：
- skillSequence: 技能使用顺序列表，元素为技能索引
- rounds: 总回合数
- coinsConsumed: 总金币消耗
策略：
- 分枝定界法
"""
def fight_boss(B, PlayerSkills, cc1, cc2):
    global rounds, coinsConsumed, current_boss_index, skillSequence
    global res_rounds, res_coinsConsumed, res_skillSequence
    global skill_cooldowns, boss_health, skills, c1, c2
    # 初始化全局变量
    boss_health = B.copy() # boss血量列表
    skills = PlayerSkills.copy() # 玩家技能列表
    skill_cooldowns = [0] * len(skills) # 技能冷却状态初始化
    skillSequence = [] # 技能使用顺序
    rounds = 0 # 总回合数
    coinsConsumed = 0 # 总金币消耗
    current_boss_index = 0 # 当前战斗的boss索引
    res_rounds = float('inf') # 最优回合数
    res_coinsConsumed = float('inf')  # 最优金币消耗
    res_skillSequence = [] # 最优技能使用顺序
    c1, c2 = cc1, cc2 # 多目标优化参数, c1控制回合数权重, c2控制金币消耗权重

    # 递归查询最优解
    dfs()
            
    return res_skillSequence, res_rounds, res_coinsConsumed

# 递归寻找最优解
def dfs():
    global rounds, coinsConsumed, current_boss_index, skillSequence
    global res_rounds, res_coinsConsumed, res_skillSequence
    global skill_cooldowns, boss_health, skills, c1, c2

    # 如果所有 Boss 已被击败，直接返回
    if current_boss_index >= len(boss_health):
        # 更新最优解
        cr = c1 * res_rounds if c1 != 0 else 0
        cc = c2 * res_coinsConsumed if c2 != 0 else 0
        if c1 * rounds + c2 * coinsConsumed < cr + cc:
            res_rounds = rounds
            res_coinsConsumed = coinsConsumed
            res_skillSequence = skillSequence.copy()
        return

    # 遍历所有技能选择，如果存在可用技能则选择，否则跳过回合
    is_skill_available = any(cooldown == 0 for cooldown in skill_cooldowns)
    if not is_skill_available:
        # 选择跳过回合
        rounds += 1
        # 更新技能冷却状态
        for j in range(len(skills)):
            if skill_cooldowns[j] > 0:
                skill_cooldowns[j] -= 1

        # 递归调用
        dfs()

        # 回溯
        rounds -= 1
        for j in range(len(skills)):
            if skill_cooldowns[j] < skills[j][1]:
                skill_cooldowns[j] += 1
        return
    
    for i in range(len(skills)):
        if skill_cooldowns[i] == 0:  # 只有冷却时间为 0 的技能可以使用
            # 选择技能 i 进行战斗
            skillSequence.append(i)
            rounds += 1
            coinsConsumed += skills[i][2]
            boss_health[current_boss_index] -= skills[i][0]

            # 更新技能冷却状态
            for j in range(len(skills)):
                if skill_cooldowns[j] > 0:
                    skill_cooldowns[j] -= 1
            skill_cooldowns[i] = skills[i][1]

            # 检查当前 Boss 是否被击败
            is_boss_defeated = False
            if boss_health[current_boss_index] <= 0:
                current_boss_index += 1
                is_boss_defeated = True

            # 递归调用
            dfs()

            # 回溯
            skillSequence.pop()
            rounds -= 1
            coinsConsumed -= skills[i][2]
            if is_boss_defeated:
                current_boss_index -= 1
            boss_health[current_boss_index] += skills[i][0]
            for j in range(len(skills)):
                if skill_cooldowns[j] > 0:
                    skill_cooldowns[j] += 1
            skill_cooldowns[i] = 0

def main_fight_boss(B, PlayerSkills, c1, c2):
    import sys
    skillSequence, rounds, coinsConsumed = fight_boss(B, PlayerSkills, c1, c2)
    
    # 确定输出路径 - 兼容打包后的环境
    if getattr(sys, 'frozen', False):
        # 打包后的 exe 环境
        output_dir = Path(sys.executable).parent / "res"
    else:
        # 开发环境
        output_dir = Path(__file__).parent.parent / "res"
    
    # 确保 res 目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = output_dir / "fight_data.json"
    write_fight_boss_result(filepath, skillSequence, rounds, coinsConsumed)
    return skillSequence, rounds, coinsConsumed

if __name__ == "__main__":
    B = [55, 35, 55]
    PlayerSkills = [    
        [24, 1, 3],
        [10, 0, 2],
        [35, 2, 5]
    ]
    c1, c2 = 0, 1  # 优先考虑金币消耗
    res_skillSequence, res_rounds, res_coinsConsumed = main_fight_boss(B, PlayerSkills, c1, c2)
    print("技能顺序:", res_skillSequence)
    print("总回合数:", res_rounds)
    print("总金币消耗:", res_coinsConsumed)






