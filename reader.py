import os
import curses
import sys
def draw_menu(stdscr, title, options, current_row):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    title_x = int((width // 2) - (len(title) // 2) - len(title) % 2)
    options_y = int(height / 2 - len(options) / 2)
    title_y = options_y - 2

    stdscr.addstr(title_y, title_x, title, curses.A_BOLD)

    for i, option in enumerate(options):
        x = int(width / 2 - len(option) / 2)
        y = options_y + i
        if i == current_row:
            stdscr.addstr(y, x, f"> {option}", curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, f"  {option}")

    stdscr.refresh()

def mainMenu(stdscr):
    curses.curs_set(0)
    title = "Main Menu"
    menu_options = ["Open", "Credits", "Exit"]
    current_row = 0
    exit_program = False

    while not exit_program:
        draw_menu(stdscr, title, menu_options, current_row)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu_options[current_row] == "Open":
                openFile(stdscr, os.getcwd())
            elif menu_options[current_row] == "Exit":
                exit_program = True
            else:
                # 处理"Credits"等其他菜单项
                pass
        elif key == 27:  # Esc 键
            exit_program = sys.exit()
        elif exit == True:
            sys.exit()

def openFile(stdscr, path):
    curses.curs_set(0)
    title = "Open File"
    files = os.listdir(path)
    menu_options = files + ["[Back]"]
    current_row = 0

    while True:
        draw_menu(stdscr, title, menu_options, current_row)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_options) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected = menu_options[current_row]
            if selected == "[Back]":
                new_path = os.path.dirname(path)
                if new_path != path:
                    openFile(stdscr, new_path)
            elif os.path.isdir(os.path.join(path, selected)):
                openFile(stdscr, os.path.join(path, selected))
            else:
                return selected
                pass
        elif key == 27:  # Esc 键
            break
# 在这里调用 curses wrapper 函数
curses.wrapper(mainMenu)
if __name__ == "__main__":
    while 1:
        selected_option = curses.wrapper(mainMenu)
        if selected_option == "Credits":
            print("Credits")
            print("Thanks to them, Kreader wouldn't have made it this far without these contributors. \n jing_jian main writer \n TinkerLee provided a lot of help with troubleshooting.")
        if selected_option == "Open":
            filepath = curses.wrapper(openFile)
            print(filepath)
            os.system('msg * /time:10 "This is the title" ' + filepath)
        if selected_option == "Exit":
            exit = True
