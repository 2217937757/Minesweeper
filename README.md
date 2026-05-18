# Minesweeper - 经典扫雷游戏

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

经典的 Windows 7 风格扫雷游戏，使用 Python 和 Tkinter 开发。

## ✨ 功能特性

### 🎮 经典玩法
- **左键点击**：揭示格子
- **右键点击**：标记/取消标记地雷（⚑）
- **数字快速开格**：点击已揭示的数字，如果周围标记的地雷数等于该数字，自动揭开其他格子

### 😊 表情反馈系统
- **😊**：正常状态
- **😮**：按下鼠标时
- **😵**：踩到地雷，游戏失败
- **😎**：成功获胜

### 📊 多种难度级别
- **初级**：9×9 网格，10个地雷
- **中级**：16×16 网格，40个地雷
- **高级**：16×30 网格，99个地雷
- **自定义**：自由设置行数、列数和地雷数量

### ⏱️ 计时与计数系统
- 红色 LED 风格数字显示
- 第一次点击时开始计时
- 最大显示 999 秒
- 实时地雷计数器（总地雷数 - 已标记数）

### 💥 动画效果
- 炸弹爆炸扩散动画
- 平滑的界面过渡
- 优化的性能表现

### 🎨 经典界面设计
- Windows 7 风格的灰色 3D 边框
- 经典配色方案
- 不同数字使用不同颜色显示
- 自适应窗口大小

## 操作说明

### 键盘快捷键
- **F2**：重新开始游戏

### 菜单选项
- **游戏 → 开局**：重新开始当前难度
- **游戏 → 初级/中级/高级**：切换难度
- **游戏 → 退出**：关闭游戏

### 高级技巧
1. **快速开格（Chord Click）**：
   - 当一个数字周围的标记地雷数等于该数字时
   - 左键点击该数字可以一次性揭开所有未标记的相邻格子
   - 这是高手必备的技巧！

2. **标记策略**：
   - 确定的地雷用右键标记
   - 不确定的格子先留着
   - 利用数字推理找出安全区域

## 🚀 安装与运行

### 方法一：直接运行
```bash
python minesweeper/main.py
```

### 方法二：作为模块运行
```bash
python -m minesweeper
```

### 方法三：安装后运行
```bash
# 安装项目
pip install .

# 运行游戏
minesweeper
```

### 环境要求
- Python 3.8+
- Tkinter（通常随 Python 一起安装）
- 无需任何外部依赖

## 游戏规则

1. 游戏目标：找出所有地雷而不触发它们
2. 数字表示周围8个格子中的地雷数量
3. 标记所有地雷并揭开所有安全格子即可获胜
4. 第一次点击永远不会是地雷

## 📦 项目结构

```
Minesweeper/
├── minesweeper/          # 主程序包
│   ├── __init__.py      # 包初始化
│   ├── __main__.py      # 模块入口点
│   └── main.py          # 游戏主逻辑
├── pyproject.toml       # 项目配置
├── requirements.txt     # 依赖说明
├── LICENSE             # MIT 许可证
├── .gitignore          # Git 忽略文件
└── README.md           # 项目文档
```

## 🛠️ 技术实现

### 核心技术
- **GUI 框架**：Tkinter
- **数据结构**：二维数组存储游戏板状态
- **搜索算法**：BFS（广度优先搜索）展开空白区域
- **事件处理**：鼠标点击、释放、悬停事件

### 性能优化
- 批量模式更新界面，避免频繁刷新
- 动态调整动画速度，适配不同地图大小
- 使用字典解包减少重复代码
- 两阶段更新策略（先收集再应用）

### 代码架构
```python
MinesweeperGame         # 主游戏类
├── create_menu()       # 创建菜单栏
├── create_widgets()    # 创建游戏界面
├── init_game()         # 初始化游戏
├── place_mines()       # 放置地雷（确保第一次点击安全）
├── reveal_cell()       # 揭示格子（BFS 展开）
├── chord_click()       # 快速开格功能
├── animate_explosion() # 炸弹爆炸动画
├── check_win()         # 检查胜利条件
└── run()               # 启动游戏主循环
```

---

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

享受经典扫雷的乐趣吧！💣🎮


## 打包命令
pyinstaller --noconfirm --clean --windowed --onefile --name Minesweeper minesweeper\main.py