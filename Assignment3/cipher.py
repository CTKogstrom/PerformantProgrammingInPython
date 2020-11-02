import curses
from curses import wrapper
import timeit
from ctypes import *


def run_gui(stdscr):
    # First set up variables with the content to fill windows

    rust_lib = load_cipher_lib()
    text_key = {'TEXT': "This is a haiku; it is not too long I think; buy you may disagree".encode('cp437'),
                'KEY ': "But there's one sound that no one knows... What does the Fox say?".encode('cp437')}
    menu = {'f': 'Read text from a local File', 'i': 'Read text from user Input prompt',
            'r': 'Apply Rust cipher to this text', 'P': 'Apply Python cipher to this text',
            'v': 'Verify cipher results match', 'k': 'Change Key used for ciphers',
            'b': 'Run Benchmarks on text (100000x)', 'q': 'Quit the Application'}
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    # Wrapper window for application contains main window and status window
    wrapper_window = curses.newwin(25, 80, 0, 0)

    # Paint main window with border
    main_window = wrapper_window.derwin(24, 80, 0, 0)
    main_window.box()

    # create menu window and paint with text
    menu_window = main_window.derwin(10, 40, 2, 20)
    main_window.addstr(1, 25, "Welcome to the XOR-Cipher App!")
    menu_window.box()
    line = 1
    for option, value in menu.items():
        menu_window.addstr(line, 1, f' [{option.upper()}] {value}')
        line += 1

    # create text and key window to display current text and key
    text_key_window = main_window.derwin(4, 76, 12, 2)
    text_key_window.box()

    update_text_key_window(text_key_window, text_key)

    # Create status window below main window to display status
    status_window = wrapper_window.derwin(1, 80, 24, 0)
    update_status(status_window, 'Application Started Successfully.')

    # create input wrapper window
    input_wrapper_window = main_window.derwin(6, 78, 17, 1)
    input_window = input_wrapper_window.derwin(3, 68, 2, 5)

    main_window.refresh()
    menu_window.refresh()

    while True:
        c = stdscr.getch()
        input_wrapper_window.clear()
        input_wrapper_window.refresh()
        if c == ord('q') or c == ord('Q'):
            print("Thanks for using the XOR-Cipher App; See you next time!")
            break
        elif c == ord('f') or c == ord('F'):
            show_input_window(input_wrapper_window, input_window, 'Enter file to load below, then press [ENTER]', 0)
            curses.curs_set(2)
            curses.echo()
            file_name = input_window.getstr(1, 1, 65)
            if not(len(file_name)):
                update_status(status_window, 'File load cancelled.')
                continue
            else:
                try:
                    input_file = open(file_name.decode('cp437'), 'rt')
                    raw_text = input_file.read()
                    text_key['TEXT'] = raw_text.encode('cp437')
                    update_text_key_window(text_key_window, text_key)
                    update_status(status_window, f'File contents loaded successfully.')
                except:
                    raw_file_name = file_name.decode()
                    update_status(status_window, f'ERROR: COULD NOT LOAD FILE: {raw_file_name}.')

            input_wrapper_window.erase()
            input_wrapper_window.refresh()
        elif c == ord('i') or c == ord('I'):
            show_input_window(input_wrapper_window, input_window, 'Enter new text below, then press [ENTER]', 0)
            curses.curs_set(2)
            curses.echo()
            new_text = input_window.getstr(1, 1, 65)
            if not(len(new_text)):
                update_status(status_window, 'Cancelled user input of text (empty string).')
            else:
                text_key['TEXT'] = new_text
                update_text_key_window(text_key_window, text_key)
                update_status(status_window, 'New text loaded into memory from user input.')
            input_wrapper_window.erase()
            input_wrapper_window.refresh()
        elif c == ord('r') or c == ord('R'):
            rust_output = rust_cipher(text_key['TEXT'], text_key['KEY '], len(text_key['TEXT']), len(text_key['KEY ']), rust_lib)
            update_status(status_window, 'Applied Rust cipher.')
            text_key['TEXT'] = rust_output
            update_text_key_window(text_key_window, text_key)

        elif c == ord('p') or c == ord('P'):
            python_cipher_result = cipher(text_key['TEXT'], text_key['KEY '])
            update_status(status_window, "Applied Python cipher.")
            text_key['TEXT'] = python_cipher_result
            update_text_key_window(text_key_window, text_key)

        elif c == ord('v') or c == ord('V'):
            python_cipher_result = cipher(text_key['TEXT'], text_key['KEY '])
            rust_cipher_result = rust_cipher(text_key['TEXT'], text_key['KEY '], len(text_key['TEXT']), len(text_key['KEY ']), rust_lib)
            if python_cipher_result == rust_cipher_result:
                update_status(status_window, 'Cipher match verified!')
            else:
                update_status(status_window, 'WARNING: ciphers do not match!')
        elif c == ord('k') or c == ord('K'):
            show_input_window(input_wrapper_window, input_window, 'Enter new key and then press [ENTER]', 0)
            curses.curs_set(2)
            curses.echo()
            new_text = input_window.getstr(1, 1, 65)
            if not (len(new_text)):
                update_status(status_window, 'Cancelled user input of key (empty string).')
            else:
                text_key['KEY '] = new_text
                update_text_key_window(text_key_window, text_key)
                update_status(status_window, 'New key loaded into memory from user input.')
            input_wrapper_window.erase()
            input_wrapper_window.refresh()
        elif c == ord('b') or c == ord('B'):
            show_input_window(input_wrapper_window, input_window, 'Running benchmarks....', 1)
            rust_cipher_setup = 'from __main__ import rust_cipher\nfrom __main__ import load_cipher_lib\nlib = load_cipher_lib()'
            rust_cipher_stmt = f'rust_cipher({text_key["TEXT"]},{text_key["KEY "]}, {len(text_key["TEXT"])}, {len(text_key["KEY "])}, lib)'
            total_rust_time = timeit.timeit(setup=rust_cipher_setup, stmt=rust_cipher_stmt, number=100000)
            display_tot_rust_time = '{:06.3f}'.format(total_rust_time)
            update_status(status_window, 'Applied Rust cipher.')
            py_cipher_setup = f'from __main__ import cipher'
            py_cipher_stmt = f'cipher({text_key["TEXT"]},{text_key["KEY "]})'
            total_py_time = timeit.timeit(setup=py_cipher_setup, stmt=py_cipher_stmt, number=100000)
            display_tot_py_time = '{:06.3f}'.format(total_py_time)
            show_input_window(input_wrapper_window, input_window, 'Results from Benchmark', 2,
                              py_time=display_tot_py_time, rust_time=display_tot_rust_time)
            update_status(status_window, 'Benchmark results displayed.')
        else:
            update_status(status_window, 'ERROR: Invalid menu selection!')
        curses.noecho()
        curses.curs_set(0)


def update_status(window, status):
    window.clear()
    window.addstr(0, 0, f' Status: {status}')
    window.refresh()


def update_text_key_window(window, text_key):
    window.clear()
    window.box()

    line = 1
    for name, value in text_key.items():
        display_value = value.decode('cp437')
        if len(display_value) > 71:
            display_value = display_value[:65]
        ctrl_translation = str.maketrans(bytes(range(0, 32)).decode("cp437"), "�☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲▼")
        display_text = display_value.translate(ctrl_translation)
        window.addnstr(line, 1, f' {name} [{display_text}]', 73)
        line += 1
    window.refresh()


def show_input_window(wrapper_window, input_window, msg, benchmark, py_time='', rust_time=''):
    wrapper_window.box()
    if benchmark == 0:
        input_window.box()
        wrapper_window.addstr(1, 17, msg)
        input_window.refresh()
    elif benchmark == 1:
        wrapper_window.addstr(1, 28, msg)
    elif benchmark == 2:
        wrapper_window.addstr(1, 28, msg)
        wrapper_window.addstr(2, 28, '----------------------')
        wrapper_window.addstr(3, 28, f'Rust Cipher:   {rust_time}s')
        wrapper_window.addstr(4, 28, f'Python Cipher: {py_time}s')
    wrapper_window.refresh()


def cipher(message, key):
    return bytes([message[i] ^ key[i % len(key)] for i in range(0, len(message))])


def load_cipher_lib(library_path='./libxorcipher.so'):
    rust_cipher_lib = cdll.LoadLibrary(library_path)
    rust_cipher_lib.restype = None
    return rust_cipher_lib


def rust_cipher(text, key, text_len, key_len, lib):
    buf = create_string_buffer(text_len)
    lib.cipher(text, key, byref(buf), text_len, key_len)
    return bytes(buf)


if __name__ == '__main__':
    wrapper(run_gui)


