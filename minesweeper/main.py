import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
from collections import deque


NUMBER_COLORS = {
    1: "#0000ff",
    2: "#008000",
    3: "#ff0000",
    4: "#000080",
    5: "#800000",
    6: "#008080",
    7: "#000000",
    8: "#808080",
}


class MinesweeperGame:
    def __init__(self, root):
        self.root = root
        self.root.title("扫雷")
        # 允许窗口调整大小
        self.root.resizable(True, True)
        
        # 难度配置
        self.difficulties = {
            "初级": {"rows": 9, "cols": 9, "mines": 10},
            "中级": {"rows": 16, "cols": 16, "mines": 40},
            "高级": {"rows": 16, "cols": 30, "mines": 99}
        }
        self.current_difficulty = "初级"
        
        # 游戏配置
        config = self.difficulties[self.current_difficulty]
        self.rows = config["rows"]
        self.cols = config["cols"]
        self.mines = config["mines"]
        
        # 游戏状态
        self.board = []
        self.revealed = []
        self.flagged = []
        self.game_over = False
        self.first_click = True
        self.start_time = None
        self.timer_running = False
        self.elapsed_time = 0
        self.timer_id = None
        self.timer_paused = False
        self.flags_placed = 0
        self.animation_playing = False  # 动画播放标志
        self.current_font_size = 12  # 当前字体大小
        self._hover_fix_id = None
        
        # 创建界面
        self.create_menu()
        self.create_widgets()
        self.init_game()

        self.root.bind("<Deactivate>", self.on_window_deactivate, add="+")
        self.root.bind("<Activate>", self.on_window_activate, add="+")
        self.root.bind("<Unmap>", self.on_window_unmap, add="+")
        self.root.bind("<Map>", self.on_window_map, add="+")
        self.root.bind_all("<FocusOut>", self.on_any_focus_out, add="+")
        self.root.bind_all("<FocusIn>", self.on_any_focus_in, add="+")
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 游戏菜单
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="游戏(G)", menu=game_menu)
        game_menu.add_command(label="开局(N)\tF2", command=self.restart_game, accelerator="F2")
        game_menu.add_separator()
        game_menu.add_command(label="初级(B)", command=lambda: self.change_difficulty("初级"))
        game_menu.add_command(label="中级(I)", command=lambda: self.change_difficulty("中级"))
        game_menu.add_command(label="高级(E)", command=lambda: self.change_difficulty("高级"))
        game_menu.add_command(label="自定义(C)...", command=self.custom_difficulty)
        game_menu.add_separator()
        game_menu.add_command(label="退出(X)", command=self.root.quit)
        
        # 绑定F2快捷键
        self.root.bind('<F2>', lambda e: self.restart_game())
    
    def change_difficulty(self, difficulty):
        """改变难度"""
        self.current_difficulty = difficulty
        config = self.difficulties[difficulty]
        self.rows = config["rows"]
        self.cols = config["cols"]
        self.mines = config["mines"]
        # 销毁旧的游戏界面并重新创建
        self.info_frame.destroy()
        self.outer_frame.destroy()
        self.create_widgets()
        self.init_game()
    
    def custom_difficulty(self):
        """自定义难度"""
        # 创建自定义对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("自定义难度")
        dialog.resizable(False, False)
        
        # 居中显示
        dialog.update_idletasks()
        width = 300
        height = 230
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # 创建输入框，使用当前游戏参数作为默认值
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="行数 (9-30):", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        rows_var = tk.StringVar(value=str(self.rows))
        rows_entry = tk.Entry(frame, textvariable=rows_var, font=("Arial", 10), width=10)
        rows_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="列数 (9-50):", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        cols_var = tk.StringVar(value=str(self.cols))
        cols_entry = tk.Entry(frame, textvariable=cols_var, font=("Arial", 10), width=10)
        cols_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="雷数 (10-999):", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        mines_var = tk.StringVar(value=str(self.mines))
        mines_entry = tk.Entry(frame, textvariable=mines_var, font=("Arial", 10), width=10)
        mines_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="雷密度:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=5)
        density_var = tk.StringVar(value="—")
        tk.Label(frame, textvariable=density_var, font=("Arial", 10)).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        def clamp_value(var, min_val, max_val):
            """自动调整数值到有效范围内并更新显示"""
            try:
                value = int(var.get())
                if value < min_val:
                    var.set(str(min_val))
                elif value > max_val:
                    var.set(str(max_val))
            except ValueError:
                # 如果输入的不是数字，恢复为最小值
                var.set(str(min_val))

        def update_density(*args):
            try:
                rows = int(rows_var.get())
                cols = int(cols_var.get())
                mines = int(mines_var.get())
                total = rows * cols
                if total <= 0:
                    density_var.set("—")
                    return
                max_mines = total - 1
                if mines > max_mines:
                    mines = max_mines
                if mines < 0:
                    mines = 0
                density = (mines / total) * 100
                density_var.set(f"{density:.2f}%（{mines}/{total}）")
            except ValueError:
                density_var.set("—")
        
        def update_mines_limit(*args):
            """当行数或列数改变时，自动调整雷数上限"""
            nonlocal mines_trace_id
            try:
                rows = int(rows_var.get())
                cols = int(cols_var.get())
                
                # 验证行数和列数的有效性
                if rows < 9 or rows > 30 or cols < 9 or cols > 50:
                    return
                
                max_mines = rows * cols - 1
                
                # 确保雷数不超过新上限
                try:
                    current_mines = int(mines_var.get())
                    if current_mines > max_mines:
                        # 暂时取消追踪，避免递归
                        if mines_trace_id is not None:
                            mines_var.trace_remove('write', mines_trace_id)
                        mines_var.set(str(max_mines))
                        # 重新添加追踪
                        mines_trace_id = mines_var.trace_add('write', update_mines_limit)
                except ValueError:
                    pass
            except ValueError:
                pass
            update_density()
        
        # 绑定失焦事件，自动调整数值
        rows_entry.bind('<FocusOut>', lambda e: clamp_value(rows_var, 9, 30))
        cols_entry.bind('<FocusOut>', lambda e: clamp_value(cols_var, 9, 50))
        mines_entry.bind('<FocusOut>', lambda e: clamp_value(mines_var, 10, 999))
        
        # 监听行数和列数的变化，动态调整雷数上限
        rows_trace_id = rows_var.trace_add('write', update_mines_limit)
        cols_trace_id = cols_var.trace_add('write', update_mines_limit)
        density_rows_trace_id = rows_var.trace_add('write', update_density)
        density_cols_trace_id = cols_var.trace_add('write', update_density)
        density_mines_trace_id = mines_var.trace_add('write', update_density)
        mines_trace_id = None

        update_density()
        
        def apply_custom():
            try:
                rows = int(rows_var.get())
                cols = int(cols_var.get())
                mines = int(mines_var.get())
                
                # 最终验证（确保数据有效）
                max_mines = rows * cols - 1
                if mines > max_mines:
                    mines = max_mines
                
                # 应用自定义难度
                self.current_difficulty = "自定义"
                self.rows = rows
                self.cols = cols
                self.mines = mines
                
                # 销毁旧的游戏界面并重新创建
                self.info_frame.destroy()
                self.outer_frame.destroy()
                self.create_widgets()
                self.init_game()
                
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字！", parent=dialog)
        
        # 按钮
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="确定", command=apply_custom, font=("Arial", 10), width=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="取消", command=dialog.destroy, font=("Arial", 10), width=8).pack(side=tk.LEFT, padx=5)
    
    def create_widgets(self):
        # 顶部信息面板（经典样式）
        self.info_frame = tk.Frame(self.root, bg="#c0c0c0", bd=3, relief=tk.SUNKEN)
        self.info_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # 地雷计数器（红色LED风格）
        self.mine_counter = tk.Label(
            self.info_frame,
            text=str(self.mines).zfill(3),
            font=("Digital-7", 24, "bold"),
            bg="black",
            fg="red",
            width=3,
            anchor="e",
            relief=tk.SUNKEN,
            bd=2
        )
        self.mine_counter.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 中间笑脸按钮
        self.face_button = tk.Button(
            self.info_frame,
            text="😊",
            font=("Arial", 18),
            width=2,
            height=1,
            bg="#c0c0c0",
            relief=tk.RAISED,
            bd=3,
            command=self.restart_game,
            cursor="hand2"
        )
        self.face_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)
        
        # 计时器（红色LED风格）
        self.timer_display = tk.Label(
            self.info_frame,
            text="000",
            font=("Digital-7", 24, "bold"),
            bg="black",
            fg="red",
            width=3,
            anchor="e",
            relief=tk.SUNKEN,
            bd=2
        )
        self.timer_display.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # 游戏区域外框
        self.outer_frame = tk.Frame(self.root, bg="#808080", bd=3, relief=tk.RAISED)
        self.outer_frame.pack(padx=5, pady=5)
        
        self.game_frame = tk.Frame(self.outer_frame, bg="#c0c0c0", bd=2, relief=tk.SUNKEN)
        
        # 创建按钮网格 - 使用自适应大小的正方形格子
        self.buttons = []
        self.button_positions = {}
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                btn = tk.Button(
                    self.game_frame,
                    width=2,  # 宽度（字符数）
                    height=1,  # 高度（字符行数）
                    font=("Arial", self.current_font_size, "bold"),  # 使用动态字体大小
                    relief=tk.RAISED,  # 立体凸起效果
                    bd=3,  # 边框宽度3，增强立体感
                    bg="#c0c0c0",
                    fg="#000000",
                    activebackground="#c0c0c0",
                    disabledforeground="#000000",  # 关键：设置禁用时的文字颜色为黑色
                    overrelief=tk.RAISED,
                    padx=5,  # 水平内边距
                    pady=5,  # 垂直内边距
                    highlightthickness=0  # 禁用系统主题的高亮边框
                )
                btn.grid(row=i, column=j, sticky="nsew")  # 填满格子
                # 绑定鼠标事件
                btn.bind("<ButtonPress-1>", lambda e, r=i, c=j: self.on_button_press(r, c))
                btn.bind("<ButtonRelease-1>", lambda e, r=i, c=j: self.left_release(r, c))
                btn.bind("<ButtonPress-3>", lambda e, r=i, c=j: self.right_click(r, c))
                btn.bind("<ButtonRelease-3>", lambda e, r=i, c=j: self.right_release(r, c))
                btn.bind("<Enter>", lambda e, r=i, c=j: self.on_enter_button(r, c))
                btn.bind("<Leave>", lambda e: self.on_leave_button())
                # 禁用右键菜单
                btn.bind("<Button-3>", lambda e: "break", add="+")
                self.button_positions[btn] = (i, j)
                row.append(btn)
            self.buttons.append(row)
        
        # 配置grid使所有行列均匀分布，形成正方形
        for i in range(self.rows):
            self.game_frame.grid_rowconfigure(i, weight=1, uniform="square")
        for j in range(self.cols):
            self.game_frame.grid_columnconfigure(j, weight=1, uniform="square")
        
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        # 绑定窗口大小变化事件
        self.root.bind('<Configure>', self.on_window_resize)
    
    def calculate_font_size(self):
        """根据窗口大小计算合适的字体大小"""
        try:
            # 获取游戏区域的实际大小
            game_width = self.game_frame.winfo_width()
            game_height = self.game_frame.winfo_height()
            
            if game_width <= 1 or game_height <= 1:
                return self.current_font_size  # 如果还没初始化，返回当前值
            
            # 计算每个格子的像素大小
            cell_width = game_width / self.cols
            cell_height = game_height / self.rows
            cell_size = min(cell_width, cell_height)  # 取较小值确保正方形
            
            # 根据格子大小计算字体大小（格子大小的约40%作为字体大小）
            new_font_size = max(8, min(24, int(cell_size * 0.4)))
            
            return new_font_size
        except:
            return self.current_font_size
    
    def update_all_fonts(self, font_size):
        """更新所有按钮的字体大小"""
        if font_size == self.current_font_size:
            return  # 如果字体大小没变，不需要更新
        
        self.current_font_size = font_size
        font = ("Arial", font_size, "bold")
        
        for i in range(self.rows):
            for j in range(self.cols):
                btn = self.buttons[i][j]
                current_config = btn.config()
                
                # 只更新字体，保持其他属性不变
                btn.config(font=font)
    
    def on_window_resize(self, event):
        """窗口大小变化时调整字体大小"""
        # 只处理根窗口的resize事件
        if event.widget != self.root:
            return
        
        # 延迟更新，避免频繁刷新（增加到200ms）
        if hasattr(self, '_resize_timer'):
            self.root.after_cancel(self._resize_timer)
        
        self._resize_timer = self.root.after(200, self._do_resize_update)
    
    def _do_resize_update(self):
        """执行字体大小更新"""
        new_font_size = self.calculate_font_size()
        # 只有当字体大小真正改变时才更新
        if new_font_size != self.current_font_size:
            self.update_all_fonts(new_font_size)
    
    def on_button_press(self, row, col):
        """按钮按下事件 - 改变笑脸表情"""
        if not self.game_over and not self.revealed[row][col] and not self.flagged[row][col]:
            self.face_button.config(text="😮")
    
    def on_enter_button(self, row, col):
        """鼠标进入按钮 - 如果已揭示，强制保持SUNKEN效果"""
        if self.revealed[row][col]:
            # 已揭示的格子，强制设置为SUNKEN
            self.buttons[row][col].config(relief=tk.SUNKEN, overrelief=tk.SUNKEN)
    
    def on_leave_button(self):
        """鼠标离开按钮 - 恢复笑脸"""
        if not self.game_over:
            self.face_button.config(text="😊")

    def schedule_hover_relief_fix(self):
        if getattr(self, "_hover_fix_id", None):
            try:
                self.root.after_cancel(self._hover_fix_id)
            except tk.TclError:
                pass
            self._hover_fix_id = None

        self._hover_fix_id = self.root.after(1, self.apply_hover_relief_fix)

    def apply_hover_relief_fix(self):
        self._hover_fix_id = None
        widget = None
        try:
            widget = self.root.winfo_containing(
                self.root.winfo_pointerx(),
                self.root.winfo_pointery(),
            )
        except tk.TclError:
            return

        positions = getattr(self, "button_positions", {})
        pos = None

        if widget is not None:
            current = widget
            while current is not None:
                pos = positions.get(current)
                if pos is not None:
                    widget = current
                    break
                current = getattr(current, "master", None)

        if pos is None:
            origin = getattr(self, "_last_reveal_origin", None)
            if origin is None:
                return
            r, c = origin
            if not (0 <= r < self.rows and 0 <= c < self.cols and self.revealed[r][c]):
                return
            widget = self.buttons[r][c]
        else:
            r, c = pos
            if not (0 <= r < self.rows and 0 <= c < self.cols and self.revealed[r][c]):
                return

        widget.config(relief=tk.SUNKEN, overrelief=tk.SUNKEN)
        try:
            widget.config(overrelief=tk.RAISED)
            widget.config(overrelief=tk.SUNKEN)
        except tk.TclError:
            pass

        widget.event_generate("<Leave>")
        widget.event_generate("<Enter>")
    
    def update_mine_counter(self):
        """更新地雷计数器"""
        remaining = self.mines - self.flags_placed
        # 处理负数情况
        if remaining < 0:
            self.mine_counter.config(text=f"-{abs(remaining):02d}")
        else:
            self.mine_counter.config(text=str(remaining).zfill(3))
    
    def init_game(self):
        # 如果动画正在播放，禁止重置
        if self.animation_playing:
            return
        
        # 初始化游戏板
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.game_over = False
        self.first_click = True
        self.start_time = None
        self.timer_running = False
        self.elapsed_time = 0
        self.timer_paused = False
        self.flags_placed = 0
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        # 重置显示（不立即刷新）
        self.update_mine_counter()
        self.timer_display.config(text="000")
        self.face_button.config(text="😊")
        
        # 批量重置所有按钮 - 先设置共同属性
        common_config = {
            'text': '',
            'bg': '#c0c0c0',
            'relief': tk.RAISED,
            'state': tk.NORMAL,
            'fg': '#000000',
            'bd': 2,
            'disabledforeground': '#000000'
        }
        
        # 批量应用配置（不触发中间刷新）
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].config(**common_config)
    
    def place_mines(self, first_row, first_col):
        """放置地雷，确保第一次点击的位置及其周围没有雷"""
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # 避免在第一次点击位置及其周围放置地雷
            if abs(row - first_row) <= 1 and abs(col - first_col) <= 1:
                continue
            
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_placed += 1
        
        # 计算每个格子周围的雷数
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == -1:
                    continue
                count = self.count_adjacent_mines(i, j)
                self.board[i][j] = count
    
    def count_adjacent_mines(self, row, col):
        """计算周围8个格子的地雷数量"""
        count = 0
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.board[i][j] == -1:
                    count += 1
        return count
    
    def left_click(self, row, col):
        """左键按下事件"""
        if self.game_over:
            return
        
        # 改变笑脸为惊讶表情
        if not self.revealed[row][col] and not self.flagged[row][col]:
            self.face_button.config(text="😮")
    
    def left_release(self, row, col):
        """左键释放事件"""
        if self.game_over:
            self.face_button.config(text="😊")
            return
        
        # 如果点击的是已揭示的数字，尝试快速开格
        if self.revealed[row][col] and self.board[row][col] > 0:
            self.chord_click(row, col)
            self.face_button.config(text="😊")
            return
        
        if self.flagged[row][col]:
            self.face_button.config(text="😊")
            return
        
        # 第一次点击时放置地雷并开始计时
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
            self.start_timer()
        
        self.reveal_cell(row, col)
        self.face_button.config(text="😊")
        
        # 检查是否踩到雷
        if self.board[row][col] == -1:
            self.game_over = True
            self.stop_timer()
            self.face_button.config(text="😵")
            # 使用动画效果显示爆炸
            self.animate_explosion(row, col)
            return
        
        # 检查是否胜利
        if self.check_win():
            self.game_over = True
            self.stop_timer()
            self.face_button.config(text="😎")
            # 清除动画播放标志（如果有）
            self.animation_playing = False
            messagebox.showinfo("恭喜", f"你赢了！用时: {self.elapsed_time}秒", parent=self.root)
    
    def chord_click(self, row, col):
        """双击数字快速开格（当周围标记数等于数字时）"""
        if not self.revealed[row][col] or self.board[row][col] <= 0:
            return
        
        # 计算周围标记的地雷数
        flagged_count = 0
        unrevealed_cells = []
        
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if i == row and j == col:
                    continue
                if self.flagged[i][j]:
                    flagged_count += 1
                elif not self.revealed[i][j]:
                    unrevealed_cells.append((i, j))
        
        # 如果标记数等于数字，揭开所有未标记的格子
        if flagged_count == self.board[row][col]:
            for i, j in unrevealed_cells:
                self.reveal_cell(i, j, batch_mode=True)
                # 检查是否踩到雷
                if self.board[i][j] == -1:
                    self.game_over = True
                    self.stop_timer()
                    self.face_button.config(text="😵")
                    # 使用动画效果显示爆炸，以踩到的雷为中心
                    self.animate_explosion(i, j)
                    return
            
            # 批量揭示完成后，统一刷新界面
            self.root.update_idletasks()
            self.schedule_hover_relief_fix()
            
            # 检查是否胜利
            if self.check_win():
                self.game_over = True
                self.stop_timer()
                self.face_button.config(text="😎")
                # 清除动画播放标志（如果有）
                self.animation_playing = False
                messagebox.showinfo("恭喜", f"你赢了！用时: {self.elapsed_time}秒", parent=self.root)
    
    def right_click(self, row, col):
        """右键按下事件"""
        if self.game_over:
            return "break"
        
        # 改变笑脸为惊讶表情
        if not self.revealed[row][col]:
            self.face_button.config(text="😮")
        
        return "break"
    
    def right_release(self, row, col):
        """右键释放事件 - 标记/取消标记地雷"""
        if self.game_over or self.revealed[row][col]:
            self.face_button.config(text="😊")
            return "break"
        
        if self.flagged[row][col]:
            self.flagged[row][col] = False
            self.flags_placed -= 1
            # 取消标记 - 恢复原始样式
            self.buttons[row][col].config(
                text="",
                bg="#c0c0c0",
                relief=tk.RAISED,
                state=tk.NORMAL,
                bd=2,  # 恢复边框宽度2，增强立体感
                disabledforeground="#000000"
            )
        else:
            self.flagged[row][col] = True
            self.flags_placed += 1
            # 标记旗帜 - 使用鲜艳的红色背景和白色旗帜图标
            self.buttons[row][col].config(
                text="⚑",
                bg="#e74c3c",  # 鲜艳的红色背景
                fg="#ffffff",  # 纯白色旗帜
                font=("Arial", 12, "bold"),  # 增大字体匹配格子大小
                relief=tk.RAISED,  # 保持凸起效果，表示未揭示
                bd=3,  # 边框宽度3，与未揭示格子一致
                disabledforeground="#ffffff"  # 禁用时保持白色
            )
        
        # 更新剩余雷数显示
        self.update_mine_counter()
        self.face_button.config(text="😊")
        
        return "break"
    
    def on_mouse_move(self, row, col):
        """鼠标移动事件 - 检测是否移出按钮区域"""
        if not self.game_over:
            self.face_button.config(text="😊")
    
    def reveal_cell(self, row, col, batch_mode=False):
        """揭示一个格子
        Args:
            row: 行号
            col: 列号
            batch_mode: 批量模式，跳过刷新以提高性能
        """
        if (
            row < 0
            or row >= self.rows
            or col < 0
            or col >= self.cols
            or self.revealed[row][col]
            or self.flagged[row][col]
        ):
            return
        
        # 使用队列进行广度优先搜索，避免递归过深
        self._last_reveal_origin = (row, col)
        rows = self.rows
        cols = self.cols
        board = self.board
        buttons = self.buttons
        revealed = self.revealed
        flagged = self.flagged

        queue = deque([row * cols + col])
        visited = [bytearray(cols) for _ in range(rows)]
        enqueued = [bytearray(cols) for _ in range(rows)]
        enqueued[row][col] = 1
        changed = False
        
        while queue:
            idx = queue.popleft()
            r = idx // cols
            c = idx - r * cols
            
            # 边界检查和状态检查
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= cols
                or revealed[r][c]
                or flagged[r][c]
                or visited[r][c]
            ):
                continue
            
            visited[r][c] = 1
            revealed[r][c] = True
            cell_value = board[r][c]
            
            if cell_value == 0:
                # 空白格 - 批量模式下跳过刷新
                buttons[r][c].config(
                    text="",
                    bg="#e8e8e8",
                    relief=tk.SUNKEN,
                    bd=2,
                    state=tk.NORMAL,
                    overrelief=tk.SUNKEN,
                    highlightthickness=0,
                )
                changed = True
                # 如果是空白格，将周围的格子加入队列
                r0 = r - 1 if r > 0 else 0
                r1 = r + 1 if r + 1 < rows else rows - 1
                c0 = c - 1 if c > 0 else 0
                c1 = c + 1 if c + 1 < cols else cols - 1
                for i in range(r0, r1 + 1):
                    row_enqueued = enqueued[i]
                    row_visited = visited[i]
                    for j in range(c0, c1 + 1):
                        if row_visited[j] or row_enqueued[j] or revealed[i][j] or flagged[i][j]:
                            continue
                        row_enqueued[j] = 1
                        queue.append(i * cols + j)
            else:
                # 数字格 - 批量模式下跳过刷新
                color = NUMBER_COLORS.get(cell_value, "#000000")
                buttons[r][c].config(
                    text=str(cell_value),
                    fg=color,
                    bg="#e8e8e8",
                    relief=tk.SUNKEN,
                    font=("Arial", 12, "bold"),
                    bd=2,
                    state=tk.NORMAL,
                    overrelief=tk.SUNKEN,
                    highlightthickness=0,
                )
                changed = True

        if not batch_mode and changed:
            self.root.update_idletasks()
            self.schedule_hover_relief_fix()
    
    def animate_explosion(self, click_row, click_col):
        """炸弹爆炸动画 - 从点击位置向外扩散"""
        # 设置动画播放标志
        self.animation_playing = True
        
        # 收集所有需要显示的地雷
        mines_by_distance = {}
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == -1:
                    distance = abs(i - click_row) + abs(j - click_col)
                    mines_by_distance.setdefault(distance, []).append((i, j))
        # 分批显示爆炸效果
        max_distance = max(mines_by_distance.keys(), default=0)
        
        # 根据地雷数量动态调整延迟时间
        total_mines = sum(len(v) for v in mines_by_distance.values())
        if total_mines > 200:
            delay_per_step = 10  # 大量地雷时快速播放
        elif total_mines > 100:
            delay_per_step = 15
        elif total_mines > 50:
            delay_per_step = 20
        else:
            delay_per_step = 30  # 少量地雷时正常速度
        
        def explode_step(current_distance):
            # 显示当前距离的所有地雷
            for i, j in mines_by_distance.get(current_distance, []):
                if self.flagged[i][j]:
                    # 正确标记的地雷 - 绿色对勾
                    self.buttons[i][j].config(
                        text="✓",
                        bg="#27ae60",
                        fg="#ffffff",
                        font=("Arial", 12, "bold"),
                        relief=tk.FLAT,
                        bd=1,
                    )
                else:
                    # 未标记的地雷 - 红色炸弹背景
                    self.buttons[i][j].config(
                        text="💥",
                        bg="#c0392b",
                        fg="#ffffff",
                        font=("Arial", 12, "bold"),
                        relief=tk.FLAT,
                        bd=1,
                    )
            
            # 强制刷新界面，让动画立即可见
            self.root.update_idletasks()
            
            # 继续下一批
            if current_distance < max_distance:
                self.root.after(delay_per_step, lambda: explode_step(current_distance + 1))
            else:
                # 显示错误标记的位置
                for i in range(self.rows):
                    for j in range(self.cols):
                        if self.flagged[i][j] and self.board[i][j] != -1:
                            self.buttons[i][j].config(
                                text='✗',
                                bg='#e67e22',
                                fg='#ffffff',
                                font=("Arial", 12, "bold"),  # 增大字体匹配格子大小
                                relief=tk.FLAT,
                                bd=1
                            )
                # 清除动画播放标志
                self.animation_playing = False
                # 动画结束后显示消息框
                messagebox.showerror("游戏结束", "你踩到雷了！", parent=self.root)
        
        # 开始动画
        explode_step(0)
    
    def reveal_all_mines(self):
        """游戏结束时显示所有地雷 - 批量优化版"""
        # 收集需要更新的按钮
        updates = []
        
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == -1:
                    if self.flagged[i][j]:
                        # 正确标记的地雷 - 绿色对勾
                        updates.append((i, j, {
                            'text': '✓',
                            'bg': '#27ae60',
                            'fg': '#ffffff',
                            'font': ("Arial", 9, "bold"),
                            'relief': tk.FLAT,
                            'bd': 1
                        }))
                    else:
                        # 未标记的地雷 - 红色炸弹背景
                        updates.append((i, j, {
                            'text': '💥',
                            'bg': '#c0392b',
                            'fg': '#ffffff',
                            'font': ("Arial", 9, "bold"),
                            'relief': tk.FLAT,
                            'bd': 1
                        }))
                elif self.flagged[i][j]:
                    # 错误标记的位置 - 橙色叉号
                    updates.append((i, j, {
                        'text': '✗',
                        'bg': '#e67e22',
                        'fg': '#ffffff',
                        'font': ("Arial", 9, "bold"),
                        'relief': tk.FLAT,
                        'bd': 1
                    }))
        
        # 批量应用更新（不触发中间刷新）
        for i, j, config in updates:
            self.buttons[i][j].config(**config)
    
    def check_win(self):
        """检查是否获胜"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != -1 and not self.revealed[i][j]:
                    return False
        return True
    
    def restart_game(self):
        """重新开始游戏"""
        # 如果动画正在播放，禁止重置
        if self.animation_playing:
            return
        
        # 停止计时器
        self.stop_timer()
        
        # 重新初始化游戏
        self.init_game()
    
    def start_timer(self):
        """启动计时器"""
        if self.timer_paused:
            return
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
    
    def stop_timer(self):
        """停止计时器"""
        self.timer_running = False
        self.timer_paused = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def pause_timer(self):
        if not self.timer_running:
            return
        self.timer_running = False
        self.timer_paused = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def resume_timer(self):
        if not self.timer_paused:
            return
        if self.game_over:
            self.timer_paused = False
            return
        if self.start_time is None:
            self.timer_paused = False
            return
        self.start_time = time.time() - self.elapsed_time
        self.timer_running = True
        self.timer_paused = False
        self.update_timer()
    
    def update_timer(self):
        """更新计时器显示"""
        if self.timer_running:
            if self.root.state() == "iconic" or self.root.focus_get() is None:
                self.pause_timer()
                return
            self.elapsed_time = int(time.time() - self.start_time)
            # 限制最大显示999
            if self.elapsed_time > 999:
                self.elapsed_time = 999
            self.timer_display.config(text=str(self.elapsed_time).zfill(3))
            self.timer_id = self.root.after(1000, self.update_timer)

    def schedule_focus_check(self):
        if self.start_time is None:
            return
        if hasattr(self, "_focus_check_id") and self._focus_check_id:
            self.root.after_cancel(self._focus_check_id)
        self._focus_check_id = self.root.after(80, self.apply_focus_state)

    def apply_focus_state(self):
        self._focus_check_id = None
        if self.start_time is None:
            return
        if self.game_over:
            return
        if self.root.state() == "iconic" or self.root.focus_get() is None:
            self.pause_timer()
            return
        self.resume_timer()

    def on_any_focus_out(self, event=None):
        self.schedule_focus_check()

    def on_any_focus_in(self, event=None):
        self.schedule_focus_check()

    def on_window_unmap(self, event=None):
        if event is not None and event.widget != self.root:
            return
        if self.start_time is None:
            return
        if self.game_over:
            return
        self.pause_timer()

    def on_window_map(self, event=None):
        if event is not None and event.widget != self.root:
            return
        self.schedule_focus_check()

    def on_window_deactivate(self, event=None):
        if self.start_time is None:
            return
        if self.game_over:
            return
        self.pause_timer()
    
    def on_window_activate(self, event=None):
        self.schedule_focus_check()
    
    def run(self):
        """启动游戏主循环"""
        self.root.mainloop()


def main():
    """程序入口点"""
    root = tk.Tk()
    root.resizable(True, True)  # 允许窗口调整大小和最大化
    
    game = MinesweeperGame(root)
    
    # 居中显示窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    
    # 设置消息框的父窗口为游戏窗口，使其在窗口中间显示
    game.root = root
    
    root.mainloop()


if __name__ == "__main__":
    main()
