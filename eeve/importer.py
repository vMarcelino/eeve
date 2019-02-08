import os
import sys
import importlib


def import_from_folder(folder):
    imported_files = []
    folder = os.path.abspath(folder)
    if folder not in sys.path:
        sys.path.insert(0, folder)

    for file_obj in os.listdir(folder):
        print('inspecting', file_obj)
        file_obj = os.path.join(folder, file_obj)
        if os.path.isfile(file_obj):
            if file_obj.endswith('.py'):
                module_name = os.path.splitext(os.path.basename(file_obj))[0]
                print('==> importing', module_name)
                imported_files.append(importlib.import_module(module_name))

        elif os.path.isdir(file_obj):
            if os.path.basename(file_obj) not in ['.', '..', '__pycache__']:
                module_name = os.path.basename(file_obj)
                print('--> importing', module_name)
                imported_files.append(importlib.import_module(module_name))

    return imported_files
