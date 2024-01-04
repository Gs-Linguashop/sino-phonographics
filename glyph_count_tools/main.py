import sys

char_set = set()
with open('glyph_count_tools/common_chars.txt','r',encoding='utf8') as f: # 通用规范汉字表
    for line in f.read().splitlines():
        if len(line) != 6: sys.exit(line)
        char_set.add(line[-1])

char_set = set()
with open('glyph_count_tools/common_chars(TW).txt','r',encoding='utf8') as f: # 常用國字標準字體表
    for line in f.read().splitlines():
        if len(line) != 19: sys.exit(line)
        char_set.add(line[-1])

with open('log/chars_covered.txt','r',encoding='utf8') as f:
    for char in f.read(): char_set.discard(char)

with open('glyph_count_tools/log/glyphs_missing.txt','w',encoding='utf8') as f:
    f.write(''.join(sorted(char_set)))

print('done')
