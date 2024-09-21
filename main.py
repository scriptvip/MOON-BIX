from src.__init__ import *
from src.core import *

if __name__ == '__main__':
    try:
        awak()
        menu()
    except KeyboardInterrupt:
        exit_code()

