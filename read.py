import curses

def wrap_text(text, width):
    """将文本按宽度分割为多个行"""
    wrapped_lines = []
    for line in text:
        words = line.split()
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                current_line += word + " "
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "
        wrapped_lines.append(current_line.strip())
    return wrapped_lines

def display_text(stdscr, text, scroll_pos, filename):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    wrapped_text = wrap_text(text, width - 1)

    # 限制滚动位置在有效范围内
    max_scroll_pos = max(0, len(wrapped_text) - height + 2)
    scroll_pos = min(scroll_pos, max_scroll_pos)

    # 显示文本
    for i, line in enumerate(wrapped_text[scroll_pos:scroll_pos+height-2]):
        try:
            stdscr.addstr(i, 0, line)
        except curses.error:
            pass  # 屏幕太小，忽略错误

    # 显示底部的退出提示和文件名
    try:
        stdscr.addstr(height-1, 0, "Press ESC to exit")
        stdscr.addstr(height-1, width - len(filename), filename)
    except curses.error:
        pass  # 屏幕太小，忽略错误

    stdscr.refresh()
def main(stdscr):
    curses.curs_set(0)  # 隐藏光标

    # 示例文本
    text = [
        "Line 1 of your text.Line 1 of your text.Line 1 of your text.Line 1 of your text.",
        "Line 2 of your text.Line 2 of your text.Line 2 of your text.Line 2 of your text.",
        "Line 3 of your text.Line 3 of your text.Line 3 of your text.Line 3 of your text.",
        "Line 4 of your text.Line 4 of your text.Line 4 of your text.Line 4 of your text.",
        # ... 更多行 ...
    ]
    filename = "example.txt"
    scroll_pos = 0

    while True:
        display_text(stdscr, text, scroll_pos,filename)
        
        key = stdscr.getch()
        
        # 更新滚动位置的条件需要考虑到换行后文本行数的变化
        if key == curses.KEY_UP and scroll_pos > 0:
            scroll_pos -= 1
        elif key == curses.KEY_DOWN:
            height, width = stdscr.getmaxyx()
            wrapped_text = wrap_text(text, width - 1)
            if scroll_pos < len(wrapped_text) - height + 2:
                scroll_pos += 1
        elif key == 27:  # ASCII code for ESC
            break

if __name__ == '__main__':
    curses.wrapper(main)