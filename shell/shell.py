import os
import sys

from myreadline import myreadline
from pipe import pipe
from redirect import redirect


while True:
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else:
        os.write(1, "$ ".encode())

        args = myreadline().strip().split(" ")

        if args[0] == "exit":
            os.write(2, "exiting shell...".encode())
            sys.exit(1)
            
        elif args[0] == "cd":
            os.chdir(args[1])
            continue

        wait = True
        if '&' in args:
            wait = False
            args.remove('&')

        rc = os.fork()                                                                    

        if rc < 0:
            os.write(2, "fork failed, exiting...".encode())
            sys.exit(1)

        elif rc == 0:  # child
            left_arg = args[:args.index('|')]
            right_arg = args[args.index('|') + 1:]

            if '|' in args and '>' not in left_arg and '<' not in right_arg:
                pipe(args)

            if '<' in left_arg:
                redirect(left_arg, '<')

            if '>' in right_arg:
                redirect(right_arg, '>')
                
        elif wait:
            childPidCode = os.wait()
