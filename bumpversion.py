files = ['setup.py', 'pyproject.toml', 'eeve/__init__.py']
bump = [False, True, False]
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
                    lines[i] = line.replace(current_ver, new_ver)
            except:
                print('failed:', line)
    with open(fn, 'w') as f:
        f.writelines(lines)