import os
import sys
import re

from myreadline import myreadline
from pipe import pipe
from redirect import redirect


while True:
    if 'PS1' in os.environ:
        os.write(2, (os.environ['PS1']).encode())
    else:
        os.write(2, "$ ".encode())

    args = myreadline().strip().split(" ")

    if args[0] == "exit":
        os.write(2, "exiting shell...".encode())
        sys.exit(0)
            
    elif args[0] == "cd":
        try:
            os.chdir(args[1])
        except:
            os.write(2, "No such directory\n".encode())
        continue

    rc = os.fork()
    
    wait = True
    if '&' in args:
        wait = False
        args.remove('&')

    if rc < 0:
        os.write(2, "fork failed, exiting...".encode())
        sys.exit(0)

    elif rc == 0:  # child
        if '|' in args:
            pipe(args)
            continue

        if '<' in args:
            redirect(args, '<')

        if '>' in args:
            redirect(args, '>')

        try:
            os.execve(args[0], args, os.environ)
        except FileNotFoundError:
            pass

        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, args[0])

            try:
                os.execve(program, args, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

        os.write(2, ("Could not exec: %s\n" % args[0]).encode())
        sys.exit(1)
            
    elif wait:
        childPidCode = os.wait()
