import os
import sys


def redirect(arg, symbol):
    if symbol == '<' and arg.count("<") == 1:
        os.close(0)
        os.open(arg[arg.index(symbol) + 1], os.O_RDONLY)
        os.set_inheritable(0, True)

    elif symbol == '>' and arg.count(">") == 1:
        os.close(1)
        os.open(arg[arg.index(symbol) + 1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)

    else:
        os.write(2, "redirect error, exiting...".encode())
        sys.exit(1)
