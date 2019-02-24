import uuid
import re
u = lambda: str(uuid.uuid4()).replace('-', '')

special_chars = [':', '->', '=', ',', ';', '|']
char_map = {c: u() for c in special_chars}
char_map = {k: f'<[{k}]>' for k in char_map}
slash = u()


def remap(e):
    for char in char_map:
        print('searching  ', char)

        def sub(pat):
            print('found:', '[', pat[0], ']')

            return pat[0][0] + char_map[char]

        c = char.replace('|', r'\|').replace('$', r'\$')
        e = re.sub(fr"[^({slash})]{c}", sub, e)
        print(e)
        print()
    return e


# test
if __name__ == '__main__':
    char_map = {k: f'<[{k}]>' for k in char_map}
    slash = '#'
    s = r'timer: 2 -> test action: oi\, tudo  bem? \=\,\\ Eu \= vc  , init_par3= teste teste | trigger_result=$return_result'

    replaces = []
    mx = len(s)
    i = 0
    while i < mx:
        if s[i] == '\\':
            replaces.append(i)
            i += 1

        i += 1

    for r in reversed(replaces):
        s = s[:r] + slash + s[r + 1:]

    print(s)
    s = remap(s).replace(slash, '')
    print(s)
    print('end')