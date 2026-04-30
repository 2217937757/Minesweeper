"""
Entry point for the Minesweeper game application.

This module provides the main function to launch the game.
"""

import sys
import tkinter as tk
from minesweeper.main import MinesweeperGame


def main():
    """Launch the Minesweeper game."""
    try:
        root = tk.Tk()
        root.resizable(True, True)
        game = MinesweeperGame(root)
        
        # 居中显示窗口
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'+{x}+{y}')
        
        game.root = root
        game.run()
    except KeyboardInterrupt:
        print("\n游戏已退出")
        sys.exit(0)
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
