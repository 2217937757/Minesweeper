# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-30

### Added
- 经典 Windows 7 风格扫雷游戏
- 三种难度级别（初级、中级、高级）
- 自定义难度功能，可自由设置行数、列数和地雷数
- 表情反馈系统（😊😮😵😎）
- 计时器和地雷计数器
- 左键点击揭示格子
- 右键点击标记/取消标记地雷
- 数字快速开格功能（Chord Click）
- 炸弹爆炸扩散动画效果
- 自适应窗口大小
- 菜单栏支持（游戏、难度选择）
- F2 快捷键重新开始

### Changed
- 使用 BFS（广度优先搜索）替代递归展开空白区域，避免栈溢出
- 优化大地图性能，使用批量模式更新界面
- 动态调整动画速度，适配不同地雷数量
- 改进输入验证，自动调整超出范围的数值
- 实时显示自定义难度的输入值

### Fixed
- 修复标旗子时格子凹陷的问题
- 修复 trace_add 导致的无限循环卡死问题
- 修复 chord_click 踩雷时缺少动画的问题
- 修复自定义难度对话框变量作用域问题

### Technical
- 重构为标准 Python 包结构
- 添加 pyproject.toml 配置文件
- 添加完整的文档和注释
- 实现两阶段更新策略优化性能
- 使用字典解包减少重复代码
