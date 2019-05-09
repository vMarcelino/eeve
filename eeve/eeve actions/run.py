import os


def run_system_command(cmd):
    os.system(cmd)


actions = {'run': {'run': run_system_command}}
