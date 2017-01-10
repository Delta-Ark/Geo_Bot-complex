#!/usr/bin/python
# editor.py
# Saito 2016


"""Creates a simple text editor
"""
import curses
from curses.textpad import Textbox, rectangle
import traceback


def emacs_textbox(stdscr, initial_text):
    commands = """
    A command Control-G is == Control + g (don't capitalize)
    To Exit hit Control-G

    This editing buffer uses Emacs commands (No Control-Y though)

    Movement:
    Use arrow keys
    OR:
    Start of line: Control-A
    End of line:   Control-E
    Back           Control-B
    Forward        Control-F
    Down line      Control-N Cursor down; move down one line.
    Previous line  Control-P Cursor up; move up one line.
    ---------------------------------------------------------------
    Deletion:
        Delete under cursor  Control-D
        Delete backwards     Control-H
        Kill line            Control-K
    """
    stdscr.addstr(commands)
    n_lines = len(commands.splitlines()) - 4 + 1
    stdscr.addstr("-----------------------------------------\n")
    stdscr.addstr(initial_text)
    # lines = 10  #curses.LINES
    # cols = 80  #curses.COLS
    # uly = 5
    # ulx = 1
    # editwin = curses.newwin(lines, cols, uly, ulx)
    # rectangle(stdscr, uly, ulx, 1+lines+1, 1+cols+1)

    box = Textbox(stdscr)  # from curses.textpad
    box.edit()
    message = box.gather()
    lines = message.splitlines()
    message = "\n".join(lines[n_lines:])
    return message


def callable(stdscr):
    stdscr.clear()
    stdscr.addstr("Press ESC to exit editor\n")
    stdscr.addstr(str(stdscr.getmaxyx()))
    stdscr.addstr("\nsome text \n to edit \n is right here")
    while True:
        key = stdscr.getch()
        if key == 27:
            break
    return 0


def create_editor(initial_text):
    msg = curses.wrapper(emacs_textbox, initial_text)
    return msg


def main():
    initial_text = """
This is my poem
It is not very clever
But I'm fond of it
"""
    msg = create_editor(initial_text)
    print msg
    

if __name__ == '__main__':
    main()
