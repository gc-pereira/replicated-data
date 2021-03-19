import os
import shutil

def export_file():
    os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
    shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
    os.replace("path/to/current/file.foo", "path/to/new/destination/for/file.foo")