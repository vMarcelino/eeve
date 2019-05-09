import os
print(f'Started in {os.getcwd()}')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f'Migrated to {os.getcwd()}')

try:
    import travel_backpack
    travel_backpack.log_stdout('output.log')
    print('\n\n\n\nlogging from travel-backpack')
except:
    import sys
    sys.stdout = open('output2.log', 'w')
    sys.stderr = open('output-error-2.log', 'w')
    print('logging from 2')
import eeve.__main__