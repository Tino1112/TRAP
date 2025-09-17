import os

def fix_tcL_error():
    python_base = r"C:\Users\User\AppData\Local\Programs\Python\Python313"
    os.environ['TCL_LIBRARY'] = os.path.join(python_base, "tcl", "tcl8.6")
    os.environ['TK_LIBRARY'] = os.path.join(python_base, "tcl", "tk8.6")