import platform
import curses

def get_system_info():
    system_info = {}
    system_info['architecture'] = platform.machine()
    system_info['bits'] = platform.architecture()[0]
    return system_info



def draw_menu(stdscr, title, options, current_row):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # 计算标题位置
    title_x = int((width // 2) - (len(title) // 2) - len(title) % 2)
    # 计算选项位置
    options_y = int(height / 2 - len(options) / 2)
    # 标题位于选项上方，保持一定的距离
    title_y = options_y - 2  # 调整这里的数字以改变标题和选项之间的距离

    # 绘制标题
    stdscr.addstr(title_y, title_x, title, curses.A_BOLD)

    # 绘制选项
    for i, option in enumerate(options):
        x = int(width / 2 - len(option) / 2)
        y = options_y + i
        if i == current_row:
            stdscr.addstr(y, x, f"> {option}", curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, f"  {option}")

    stdscr.refresh()

def mainMenu(stdscr):
    curses.curs_set(0)  # 隐藏光标

    title = "Main Menu"
    menu_options = ["Read computer CPU architecture information", "Option 2", "Credits","Exit"]
    current_row = 0  # 初始化当前行

    while True:
        draw_menu(stdscr, title, menu_options, current_row)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            break

    return menu_options[current_row]

if __name__ == "__main__":
    while 1:
        selected_option = curses.wrapper(mainMenu)
        if selected_option == "Read computer CPU architecture information":
            system_info = get_system_info()
            print("Processor architecture:", system_info['architecture'])
            print("Processor Bits:", system_info['bits'])
        if selected_option == "Exit":
            break
