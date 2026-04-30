# 贡献者指南

感谢你考虑为 Minesweeper 项目做出贡献！

## 行为准则

本项目采用开放和包容的态度。请尊重所有贡献者。

## 如何贡献

### 报告 Bug

如果你发现了 Bug，请在 GitHub Issues 中创建一个新的 issue，包含：

1. **清晰的标题**：简要描述问题
2. **复现步骤**：详细说明如何触发 Bug
3. **预期行为**：应该发生什么
4. **实际行为**：实际发生了什么
5. **环境信息**：Python 版本、操作系统等
6. **截图或日志**：如果有的话

### 提出新功能

在开始开发新功能之前，请先创建一个 issue 讨论你的想法。这样可以避免重复工作。

### 提交代码

1. **Fork 仓库**
   ```bash
   # 点击 GitHub 页面上的 Fork 按钮
   ```

2. **克隆你的 Fork**
   ```bash
   git clone https://github.com/yourusername/Minesweeper.git
   cd Minesweeper
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **进行修改**
   - 遵循现有的代码风格
   - 添加必要的注释
   - 更新文档（如果需要）

5. **测试你的更改**
   ```bash
   python -m minesweeper
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

7. **推送到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 在 GitHub 上打开 Pull Request
   - 详细描述你的更改
   - 关联相关的 issue（如果有的话）

## 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用 4 个空格缩进
- 行长度不超过 100 字符
- 使用有意义的变量名

### 注释规范

- 所有公共方法必须有 docstring
- 复杂逻辑需要添加注释说明
- 使用中文注释（因为主要用户是中文用户）

示例：
```python
def reveal_cell(self, row, col, batch_mode=False):
    """揭示一个格子
    
    Args:
        row: 行号
        col: 列号
        batch_mode: 批量模式，跳过中间刷新以提高性能
    """
    # 边界检查
    if (row < 0 or row >= self.rows or 
        col < 0 or col >= self.cols):
        return
```

### Commit 消息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构
- `perf:` 性能优化
- `test:` 测试相关
- `chore:` 构建过程或辅助工具变动

示例：
```bash
git commit -m "feat: add explosion animation"
git commit -m "fix: resolve infinite loop in custom difficulty"
git commit -m "docs: update README with installation guide"
```

## 开发流程

### 设置开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安装项目（开发模式）
pip install -e .
```

### 运行测试

目前项目使用手动测试。建议添加单元测试：

```bash
python -m minesweeper
```

### 文档更新

如果你添加了新功能或修改了现有功能，请更新相关文档：

- `README.md` - 用户文档
- `DEVELOPMENT.md` - 开发文档
- `CHANGELOG.md` - 变更日志

## 审查流程

1. 所有 Pull Request 至少需要一个审查者批准
2. CI 测试必须通过（如果配置了的话）
3. 代码必须符合项目规范
4. 文档必须更新（如果需要）

## 常见问题

### Q: 我可以添加音效吗？
A: 可以！但请确保它是可选的，并且不会增加外部依赖。

### Q: 如何支持多语言？
A: 欢迎实现国际化功能，建议使用 gettext 框架。

### Q: 可以添加在线排行榜吗？
A: 这会增加复杂性，建议先讨论实现方案。

### Q: 我能修改 UI 主题吗？
A: 当然！欢迎添加主题切换功能。

## 联系方式

- GitHub Issues: https://github.com/2217937757/Minesweeper/issues
- Email: your.email@example.com

## 许可证

通过贡献代码，你同意你的贡献将在 MIT 许可证下发布。

---

再次感谢你的贡献！🎉
