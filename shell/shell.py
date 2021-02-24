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
            if '|' in args:
                pipe(args)
                continue

            if '<' in args:
                redirect(args, '<')

            if '>' in args:
                redirect(args, '>')
                
        elif wait:
            childPidCode = os.wait()
