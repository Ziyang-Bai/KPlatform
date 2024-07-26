import curses

def display_text(stdscr, text, scroll_pos, filename):
    height, width = stdscr.getmaxyx()
    # 创建用于显示文本的子窗口
    text_win = stdscr.derwin(height - 2, width - 15, 1, 0)  # 保留15列空间给进度条和文件名
    
    # 清除文本窗口
    text_win.erase()
    
    # 计算最大滚动位置
    max_scroll_pos = max(0, len(text) - height + 2)
    
    # 显示文本，确保不超过窗口边界
    for i in range(max(0, scroll_pos), min(len(text), scroll_pos + height - 2)):
        try:
            text_win.addstr(i - scroll_pos, 0, text[i])
        except curses.error:
            break  # 如果超出边界，则停止尝试写入
    
    # 刷新文本窗口
    text_win.refresh()

def show_progress(stdscr, height, width, text, scroll_pos, filename):
    """显示一个简单的进度条，用于指示当前的阅读进度"""
    max_scroll_pos = max(0, len(text) - height + 2)
    
    # 创建用于显示进度条的子窗口
    progress_win = stdscr.derwin(height - 2, 10, 1, width - 15)
    
    # 清除进度条窗口
    progress_win.erase()
    
    # 计算进度百分比
    percent_complete = (scroll_pos / max_scroll_pos) * 100 if max_scroll_pos > 0 else 0
    
    # 显示进度条
    bar_length = int((height - 2) * (scroll_pos / max_scroll_pos)) if max_scroll_pos > 0 else 0
    for i in range(height - 2):
        if i < bar_length:
            progress_win.addstr(i, 0, "[#]")
        else:
            progress_win.addstr(i, 0, "[ ]")
    
    # 显示文件名
    stdscr.addstr(0, width - len(filename) - 15, filename)
    
    # 显示进度百分比
    stdscr.addstr(height - 1, width - len(filename) - 15, f"Progress: {percent_complete:.2f}%")
    
    # 刷新进度条窗口和百分比
    progress_win.refresh()
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)  # 隐藏光标

    # 文件名
    filename = "LICENSE"

    # 从文件读取文本
    with open(filename, 'r') as file:
        text = [line.rstrip('\n') for line in file]

    scroll_pos = 0

    while True:
        height, width = stdscr.getmaxyx()
        
        # 在滚动前显示进度条
        show_progress(stdscr, height, width, text, scroll_pos, filename)

        display_text(stdscr, text, scroll_pos, filename)
        
        key = stdscr.getch()

        # 更新滚动位置的条件需要考虑到换行后文本行数的变化
        if key == curses.KEY_UP and scroll_pos > 0:
            scroll_pos -= 1
        elif key == curses.KEY_DOWN:
            if scroll_pos < len(text) - height + 2:
                scroll_pos += 1
        elif key == curses.KEY_PPAGE and scroll_pos >= height - 2:  # PageUp
            scroll_pos -= (height - 2)
        elif key == curses.KEY_NPAGE and scroll_pos + height - 2 < len(text):  # PageDown
            scroll_pos += (height - 2)
        elif key == 27:  # ASCII code for ESC
            break

        # 在滚动后显示进度条
        show_progress(stdscr, height, width, text, scroll_pos, filename)

        # 确保滚动位置不会超出范围
        scroll_pos = max(0, min(scroll_pos, len(text) - height + 2))

if __name__ == '__main__':
    curses.wrapper(main)