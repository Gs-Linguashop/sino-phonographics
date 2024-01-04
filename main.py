import subprocess
import sys
from fontTools import ttLib
import copy
import chinese_converter as cvt # used only for morphs

def read_dict(file_name,delim=None):
    d = dict()
    with open(file_name,'r',encoding='utf8') as f: lines = f.read().splitlines()
    for line in lines:
        if line[0] == '#': continue
        if delim is None: d[line[0]] = line.split('\t')[0][1:] # [key][val][val]...\t[comment]
        else: # [key][key]...[delim][val][val]...\t[comment]
            for key in line.split(delim)[0].split('#')[0]:
                d[key] = line.split(delim)[1].split('\t')[0]
    return d # {'key':'val'+'val'+..., 'another key':'...', ...}

def mod_dict_keys(d,key_dict):
    for key_from,key_to in key_dict.items():
        chars_in_key_from = d.pop(key_from)
        d.setdefault(key_to,[]).extend(chars_in_key_from)
    return True

def read_morphs(file_name,pre_assigned_dict): # traditional morphs
    morph_dict = dict()
    with open(file_name,'r',encoding='utf8') as f: lines = f.read().splitlines()
    for line in lines:
        if line[0] == '#': continue
        morph, chars = line.split('\t')[0], [*line.split('\t')[1]]
        morph_dict[morph] = chars
        for char in chars.copy():
            if char in pre_assigned_dict: chars.remove(char)
        if len(morph_dict[morph]) == 0: morph_dict.pop(morph)
    for char, morph in pre_assigned_dict.items():
        morph_dict.setdefault(morph,[]).append(char)
    return morph_dict

# Main
# 1. read chars with assigned morphs
# 2. read morphs and then modify with pre-assigned chars
# 3. replace unwanted morphs then merge secondary morphs
# 4. modify the font file and sub with desired displayed form
# 5. save font and delete excessive glyphs
font_dir = 'SourceHan/'; src_dir = 'src/'; log_dir = 'log/'

pre_assigned_dict = read_dict(src_dir + 'exception_chars.txt')
morph_dict = read_morphs('phonographeme_dict.txt',pre_assigned_dict)

font_path = font_dir + 'SourceHanSansTC-Regular.otf' #
font_output = font_dir + 'SourceHanSans-Phonetic-Minimal.ttf' # SourceHanSans-Phonetic.ttf SourceHanSans-Phonetic-Minimal.ttf

font = ttLib.TTFont(font_path)

mod_dict_keys(morph_dict,read_dict(src_dir + 'rare_PhGs.txt'))

morph_sub_dict = read_dict(src_dir + 'display_mod(minimal).txt',delim='\t')

# convert morph to simplified
# for morph in morph_dict.copy():
#     if cvt.to_simplified(morph) not in morph_dict:
#         morph_dict[cvt.to_simplified(morph)] = morph_dict.pop(morph)
#         if morph in morph_sub_dict: morph_sub_dict[cvt.to_simplified(morph)] = morph_sub_dict.pop(morph)

# fonttools cannot handle ord(char) >= 16**4
for morph, chars in morph_dict.items():
    for char in chars:
        if ord(char) >= 16**4: chars.remove(char); print('char ' + char + ' overflow and deleted')

glyphs_to_include = set(font.getGlyphOrder()); glyphs_morphs = set(); missing_morph = set()
all_chars = set(); all_morph_glyphs = set()
for cmap,ori_cmap in zip(font['cmap'].tables,copy.deepcopy(font['cmap'].tables)):
    if ord('一') not in ori_cmap.cmap: continue # not a chinese ideograph cmap
    for morph, chars in morph_dict.items():
        if ord(morph) not in ori_cmap.cmap: missing_morph.add(morph); continue
        ord_morph = ord(morph)
        for sub_morph in morph_sub_dict.get(morph,[]): # sub can have multiple choices
            if ord(sub_morph) in ori_cmap.cmap: ord_morph = ord(sub_morph); break
        glyphs_morphs.add(ori_cmap.cmap[ord_morph])
        for char in chars:
            glyphs_to_include.discard(ori_cmap.cmap.get(ord(char)))
            cmap.cmap[ord(char)] = ori_cmap.cmap[ord_morph]
            all_chars.add(char); all_morph_glyphs.add(chr(ord_morph))
glyphs_to_include.update(glyphs_morphs)

glyphs_to_include_file_name = log_dir + 'glyphs_to_include.txt'
with open(glyphs_to_include_file_name,"w",encoding="utf8") as f:
    f.write(','.join(sorted(glyphs_to_include)))

with open(log_dir + 'font_missing_phonographemes.txt',"w",encoding="utf8") as f:
    f.write(''.join(sorted(missing_morph)))
with open(log_dir + 'chars_covered.txt',"w",encoding="utf8") as f:
    f.write(''.join(sorted(all_chars)))
with open(log_dir + 'phonographemes.txt',"w",encoding="utf8") as f:
    f.write(''.join(sorted(all_morph_glyphs)))

font.save(font_output); print('font saved, deleting excessive glyphs')

subprocess.run('pyftsubset ' + font_output + ' --output-file=' + font_output + ' --glyphs-file=' + glyphs_to_include_file_name, shell=True) # may not work, try changing the format of the input file 
print('done')
