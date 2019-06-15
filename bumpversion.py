files = ['setup.py', 'pyproject.toml', 'eeve/__init__.py']

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--major', action='store_true', default=False, help='to bump major version number')
parser.add_argument('--minor', action='store_true', default=False, help='to bump minor version number')
parser.add_argument('--micro', action='store_true', default=False, help='to bump micro version number')

args = parser.parse_args()

bump = [args.major, args.minor, args.micro]
for fn in files:
    lines = ['ERROR']
    with open(fn, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            try:
                if 'version' in line:
                    current_ver = line.split('=')[-1].strip()
                    if current_ver.endswith(','):
                        current_ver = current_ver[:-1].strip()

                    encapsulators = ['"', "'"]
                    for encap in encapsulators:
                        if current_ver.startswith(encap) and current_ver.endswith(encap):
                            current_ver = current_ver[1:-1].strip()

                    ver_parts = [int(x) for x in current_ver.split('.')]
                    for j, ver in enumerate(ver_parts):
                        if bump[j]:
                            ver_parts[j] += 1
                    new_ver = '.'.join(map(str, ver_parts))
                    print('bumping version from', current_ver, 'to', new_ver, 'in', fn)
                    lines[i] = line.replace(current_ver, new_ver)
            except:
                print('failed:', line)
    with open(fn, 'w') as f:
        f.writelines(lines)
    print(fn, 'done')

print('all bumps finished')