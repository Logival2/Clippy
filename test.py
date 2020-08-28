import termios
import tty
import sys

# old_settings = termios.tcgetattr(fd)

print("plop")
tty.setraw(sys.stdin.fileno())

# termios.tcsetattr(1, termios.TCSADRAIN, old_settings)
print("plop")
