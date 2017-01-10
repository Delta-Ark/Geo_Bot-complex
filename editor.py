#!/usr/bin/python
# editor.py
# Saito 2016


"""Creates a simple text editor
"""
import curses
from curses.textpad import Textbox
import locale


def emacs_textbox(stdscr, initial_text):
    instructions = """
    To Save and Exit hit Control-G

    This editing buffer uses Emacs commands (No Control-Y though)
    *** A command Control-G is == Control + g (don't capitalize) ***
    ---------------------------------------------------------------
    Movement:
    Use arrow keys

    OR:
    Start of line: Control-A
    End of line:   Control-E
    Back           Control-B
    Forward        Control-F
    Down line      Control-N Cursor down; move down one line.
    Previous line  Control-P Cursor up; move up one line.

    COPY + PASTE: Use mouse + keyboard shortcuts to copy and paste

    Deletion:
        Delete under cursor  Control-D
        Delete backwards     Control-H
        Kill line            Control-K
    """
    stdscr.addstr(instructions)

    ending = """------------------------------------------------------\n
                     EDIT BELOW ONLY
    ------------------------------------------------------\n"""
    stdscr.addstr(ending)
    stdscr.addstr(initial_text)
    box = Textbox(stdscr, insert_mode=False)  # Inf recursion bug when True
    box.edit()
    message = box.gather()
    # n_lines = len(instructions.splitlines()) - 4 + 1
    # lines = message.splitlines()
    # print lines[n_lines:]
    # message = "\n".join(lines[n_lines:])
    remove_index = len(ending) + len(instructions)
    return message[remove_index + 15:]


def create_editor(initial_text):
    locale.setlocale(locale.LC_ALL, '')
    code = locale.getpreferredencoding()
    initial_text = initial_text.encode(code, 'replace')  # or 'ignore'
    msg = curses.wrapper(emacs_textbox, initial_text)
    return msg


def main():
    initial_text = u"""
This is my po\xe9m
It is not very clever
But I'm fond of it
"""
    msg = create_editor(initial_text)
    print msg
    

if __name__ == '__main__':
    main()
