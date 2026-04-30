# 开发指南

## 项目结构

```
Minesweeper/
├── minesweeper/          # 主程序包
│   ├── __init__.py      # 包初始化和导出
│   ├── __main__.py      # 模块入口点 (python -m minesweeper)
│   └── main.py          # 游戏主逻辑和 MinesweeperGame 类
├── pyproject.toml       # 项目配置和元数据
├── requirements.txt     # 依赖说明
├── LICENSE             # MIT 许可证
├── .gitignore          # Git 忽略文件
├── README.md           # 项目文档
└── CHANGELOG.md        # 变更日志
```

## 快速开始

### 运行游戏

```bash
# 方法一：直接运行
python minesweeper/main.py

# 方法二：作为模块运行
python -m minesweeper

# 方法三：安装后运行
pip install .
minesweeper
```

### 开发环境设置

```bash
# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安装项目（开发模式）
pip install -e .
```

## 代码架构

### 核心类：MinesweeperGame

```python
class MinesweeperGame:
    def __init__(self, root):
        """初始化游戏，创建界面"""
        
    def create_menu(self):
        """创建菜单栏"""
        
    def create_widgets(self):
        """创建游戏界面组件"""
        
    def init_game(self):
        """初始化游戏状态"""
        
    def place_mines(self, safe_row, safe_col):
        """放置地雷，确保第一次点击安全"""
        
    def reveal_cell(self, row, col, batch_mode=False):
        """揭示格子（使用 BFS 展开空白区域）"""
        
    def chord_click(self, row, col):
        """快速开格功能"""
        
    def animate_explosion(self, click_row, click_col):
        """炸弹爆炸动画"""
        
    def check_win(self):
        """检查胜利条件"""
        
    def run(self):
        """启动游戏主循环"""
```

### 主要方法说明

#### reveal_cell - 格子揭示

使用 BFS（广度优先搜索）算法展开空白区域：

```python
def reveal_cell(self, row, col, batch_mode=False):
    """
    Args:
        row: 行号
        col: 列号
        batch_mode: 批量模式，跳过中间刷新以提高性能
    """
    # 使用队列进行广度优先搜索
    queue = [(row, col)]
    visited = set()
    
    while queue:
        r, c = queue.pop(0)
        # ... 处理逻辑
```

#### animate_explosion - 爆炸动画

从点击位置向外扩散的动画效果：

```python
def animate_explosion(self, click_row, click_col):
    """
    1. 计算每个地雷到点击位置的曼哈顿距离
    2. 按距离排序
    3. 分批显示，近的先爆炸
    4. 根据地雷数量动态调整延迟时间
    """
```

## 性能优化技巧

### 1. 批量模式更新

```python
# 批量模式下，跳过中间的界面刷新
if not batch_mode:
    self.root.update_idletasks()
```

### 2. 字典解包配置

```python
# 使用字典批量设置属性
common_config = {
    'text': '',
    'bg': '#c0c0c0',
    'relief': tk.RAISED,
    'state': tk.NORMAL,
}
button.config(**common_config)
```

### 3. 两阶段更新

```python
# 第一阶段：收集所有更新
updates = []
for i, j in positions:
    updates.append((i, j, config))

# 第二阶段：批量应用
for i, j, config in updates:
    button.config(**config)
```

## 扩展开发

### 添加新难度

在 `__init__` 方法的 `difficulties` 字典中添加：

```python
self.difficulties = {
    "初级": {"rows": 9, "cols": 9, "mines": 10},
    "中级": {"rows": 16, "cols": 16, "mines": 40},
    "高级": {"rows": 16, "cols": 30, "mines": 99},
    "专家": {"rows": 20, "cols": 40, "mines": 150},  # 新增
}
```

### 自定义主题

修改颜色配置：

```python
# 未揭示格子背景色
'bg': '#c0c0c0'

# 已揭示格子背景色
'bg': '#e8e8e8'

# 数字颜色
colors = {
    1: '#0000ff',  # 蓝色
    2: '#008000',  # 绿色
    3: '#ff0000',  # 红色
    # ...
}
```

### 添加新功能

1. **排行榜**：记录最佳时间
2. **提示系统**：自动标记确定的地雷
3. **撤销功能**：允许撤销上一步操作
4. **统计信息**：记录游戏统计数据

## 测试

目前项目使用手动测试。建议添加单元测试：

```python
# tests/test_game.py
import unittest
from minesweeper.main import MinesweeperGame

class TestMinesweeper(unittest.TestCase):
    def test_init(self):
        """测试游戏初始化"""
        pass
    
    def test_place_mines(self):
        """测试地雷放置"""
        pass
    
    def test_reveal_cell(self):
        """测试格子揭示"""
        pass

if __name__ == '__main__':
    unittest.main()
```

## 常见问题

### Q: 如何修改窗口大小？
A: 在 `create_widgets` 方法中调整按钮大小和间距。

### Q: 如何改变动画速度？
A: 修改 `animate_explosion` 中的 `delay_per_step` 值。

### Q: 如何添加音效？
A: 使用 `winsound` 模块（Windows）或 `pygame.mixer`。

### Q: 如何支持多语言？
A: 使用 gettext 国际化框架。

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目主页：https://github.com/yourusername/minesweeper
- 问题反馈：https://github.com/yourusername/minesweeper/issues
