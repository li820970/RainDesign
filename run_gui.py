import raingui
import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

test_window = raingui.CollectionWindow()
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
