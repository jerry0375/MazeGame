# MazeGame 使用指南

## 快速开始

### 1. 打包程序（无需执行）

在项目根目录双击运行 `build.bat`，程序会自动打包成 exe 文件。

### 2. 使用打包好的程序

打包完成后，在 `dist` 文件夹中：

```
dist/
├── MazeGame.exe          # 主程序
├── config.yaml           # 配置文件
└── res/                  # 结果输出文件夹（运行后自动创建）
    ├── maze_data.json
    ├── fight_boss_result.json
    └── solve_data.json
```

### 3. 运行程序

**方式一：双击运行**
- 直接双击 `MazeGame.exe`，使用默认配置生成迷宫

**方式二：命令行运行**
```bash
# 使用默认配置生成新迷宫
MazeGame.exe --use_default 1

# 使用配置文件中指定的迷宫文件
MazeGame.exe --use_default 0
```

### 4. 修改配置

编辑 `config.yaml` 文件来自定义设置：

```yaml
# 迷宫尺寸（建议使用奇数）
width: 15
height: 15

# 迷宫元素数量
gold_count: 5        # 金币数量
trap_count: 3        # 陷阱数量
boss_count: 1        # Boss 数量

# 元素属性
gold_value: 50       # 每个金币的价值
trap_penalty: 30     # 陷阱扣除的金币

# Boss 和玩家设置
boss_health: [10,5,3,6]                    # Boss 血量数组
player_skills: [[10,3,9],[5,2,5],[3,1,4]] # [攻击力, 冷却回合, 金币消耗]

# 优化权重
c1: 0    # 回合数权重
c2: 1    # 金币消耗权重

# 运行模式
use_default: true    # true=生成新迷宫, false=使用自定义迷宫文件

# 自定义迷宫文件路径（当 use_default 为 false 时使用）
maze_file: testData\maze_15_15_3.json
```

### 5. 查看结果

运行完成后，在 `res` 文件夹查看三个结果文件：

**maze_data.json** - 迷宫数据
```json
{
  "maze": [["#","S"," ","#"], ...],
  "B": [10,5,3,6],
  "PlayerSkills": [[10,3,9],[5,2,5],[3,1,4]]
}
```

**fight_boss_result.json** - Boss 战斗结果
```json
{
  "skillSequence": [0, 1, 2, 2, 2],  // 技能使用顺序
  "rounds": 6,                        // 战斗回合数
  "coinsConsumed": 26                 // 消耗的金币
}
```

**solve_data.json** - 迷宫求解结果
```json
{
  "path": [[0,0],[0,1],[1,1], ...],  // 移动路径
  "steps": 50,                        // 总步数
  "coins": 334,                       // 最终金币
  "coinsPerStep": 6.68                // 每步平均金币
}
```

## 分发给他人

将整个 `dist` 文件夹打包分发，包含：
- `MazeGame.exe`
- `config.yaml`

接收者只需：
1. 解压到任意目录
2. 根据需要修改 `config.yaml`
3. 双击运行 `MazeGame.exe`
4. 在 `res` 文件夹查看结果

**无需安装 Python 或任何依赖！**

## 常见问题

**Q: 程序闪退怎么办？**
A: 在命令行运行查看错误信息：
```bash
cd dist
MazeGame.exe
```

**Q: 找不到配置文件？**
A: 确保 `config.yaml` 与 `MazeGame.exe` 在同一目录

**Q: 结果文件在哪里？**
A: 自动生成在 `MazeGame.exe` 所在目录的 `res` 文件夹中

**Q: 如何使用自己的迷宫文件？**
A: 修改 `config.yaml`:
```yaml
use_default: false
maze_file: 你的迷宫文件路径.json
```

## 技术细节

- **打包工具**: PyInstaller
- **打包模式**: 单文件 exe
- **配置文件**: YAML 格式
- **输出格式**: JSON 格式
- **编码**: UTF-8

详细的技术文档请查看 `README_BUILD.md`
