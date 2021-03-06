import os
import sys
import re

from redirect import redirect


def pipe(args):
    pr, pw = os.pipe()
    rc = os.fork()

    if rc < 0:
        os.write(2, "fork failed, exiting...".encode())
        sys.exit(1)

    elif rc == 0:  # child - will write to pipe
        os.close(1)  # redirect child's stdout
        os.dup(pw)
        os.set_inheritable(1, True)

        for fd in (pr, pw):
            os.close(fd)

        left_args = args[:args.index('|')]

        if '<' in left_args:
            redirect(left_args, '<')

        try:
            os.execve(left_args[0], left_args, os.environ)
        except FileNotFoundError:
            pass
        
        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, left_args[0])

            try:
                os.execve(program, left_args, os.environ)  # try to exec program

            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

        os.write(2, ("Could not exec: %s\n" % left_args[0]).encode())
        sys.exit(1)

    else:  # parent (forked ok)
        os.close(0)
        os.dup(pr)
        os.set_inheritable(0, True)

        for fd in (pw, pr):
            os.close(fd)

        right_args = args[args.index('|') + 1:]

        if '>' in right_args:
            redirect(right_args, '>')

        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, right_args[0])

            try:
                os.execve(program, right_args, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly
            
        os.write(2, ("Could not exec: %s\n" % right_args[0]).encode())
        sys.exit(1)
