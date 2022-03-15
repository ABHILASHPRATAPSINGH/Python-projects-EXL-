# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import traceback

from PyQt5.QtWidgets import QApplication

from userform.duplicatePaymentEx import duplicatePaymentEx


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        app=QApplication(sys.argv)
        window=duplicatePaymentEx()
        window.show()
        app.exec()
    except BaseException as e:
        traceback.print_exc()
        print (e)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
