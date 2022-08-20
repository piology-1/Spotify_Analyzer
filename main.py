from authentication import authenticate
from utils import *   # get everythingcls
from prettyprinter import pprint
from GUI import MainApplication


def main():

    app = MainApplication()
    app.mainloop()


if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()
