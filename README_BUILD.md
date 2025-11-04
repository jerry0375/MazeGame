# MazeGame 打包说明

## 功能说明

本项目将 MazeGame 打包成独立的 Windows 可执行文件（exe），用户可以在没有 Python 环境的情况下运行程序。

## 打包步骤

### 1. 安装依赖

确保已安装 PyInstaller：

```bash
pip install pyinstaller
```

### 2. 运行打包脚本

在项目根目录下，双击运行 `build.bat` 或在命令行中执行：

```bash
build.bat
```

打包脚本会自动：
- 安装 PyInstaller（如果未安装）
- 清理旧的构建文件
- 打包生成 exe 文件
- 复制配置文件到输出目录
- 创建 res 输出目录

### 3. 打包完成

打包完成后，在 `dist` 文件夹中会生成：
```
dist/
├── MazeGame.exe          # 可执行文件
├── config.yaml           # 配置文件
└── res/                  # 结果输出目录（运行后生成）
    ├── maze_data.json           # 迷宫数据
    ├── fight_boss_result.json   # Boss战斗结果
    └── solve_data.json          # 迷宫求解结果
```

## 使用方法

### 基本使用

1. 进入 `dist` 文件夹
2. 双击运行 `MazeGame.exe`
3. 程序会使用默认配置生成迷宫、求解并输出结果

### 自定义配置

1. 编辑 `config.yaml` 文件修改参数：
   ```yaml
   # 迷宫尺寸
   width: 15
   height: 15
   
   # 金币和陷阱数量
   gold_count: 5
   trap_count: 3
   
   # Boss 属性
   boss_health: [10,5,3,6]
   player_skills: [[10,3,9],[5,2,5],[3,1,4]]
   
   # 使用默认配置（生成新迷宫）
   use_default: true
   
   # 或使用自定义迷宫文件
   # use_default: false
   # maze_file: testData\maze_15_15_3.json
   ```

2. 运行 `MazeGame.exe`

### 命令行参数

也可以通过命令行传递参数：

```bash
# 使用默认配置生成新迷宫
MazeGame.exe --use_default 1

# 使用配置文件中指定的迷宫文件
MazeGame.exe --use_default 0
```

## 输出文件说明

程序运行后会在 `res` 文件夹中生成三个 JSON 文件：

### 1. maze_data.json - 迷宫数据
包含生成的迷宫地图、Boss 属性和玩家技能信息。

### 2. fight_boss_result.json - Boss 战斗结果
包含：
- `skillSequence`: 技能使用顺序
- `rounds`: 战斗回合数
- `coinsConsumed`: 消耗的金币数

### 3. solve_data.json - 迷宫求解结果
包含：
- `path`: 移动路径（坐标数组）
- `steps`: 总步数
- `coins`: 剩余金币
- `coinsPerStep`: 每步平均金币收益

## 注意事项

1. **配置文件位置**：`config.yaml` 必须与 `MazeGame.exe` 在同一目录下
2. **结果文件位置**：程序会自动在 exe 所在目录创建 `res` 文件夹
3. **自定义迷宫文件**：如果使用自定义迷宫文件，确保文件路径正确
   - 使用相对路径：`testData\maze_15_15_3.json`
   - 或绝对路径：`C:\Users\...\maze.json`

## 故障排除

### 问题1：程序闪退
- 在命令行中运行 exe 查看错误信息：
  ```bash
  cd dist
  MazeGame.exe
  ```

### 问题2：找不到配置文件
- 确保 `config.yaml` 与 `MazeGame.exe` 在同一目录
- 检查配置文件编码为 UTF-8

### 问题3：无法生成结果文件
- 检查 exe 所在目录是否有写入权限
- 手动创建 `res` 文件夹

### 问题4：自定义迷宫文件找不到
- 检查 `config.yaml` 中 `maze_file` 路径是否正确
- 使用绝对路径或确保相对路径从 exe 所在目录开始

## 分发说明

将整个 `dist` 文件夹分发给用户，用户需要：
1. 解压到任意目录
2. 根据需要修改 `config.yaml`
3. 运行 `MazeGame.exe`

无需安装 Python 或任何依赖库。
