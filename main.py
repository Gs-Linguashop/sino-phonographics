import sys
import subprocess
from fontTools import ttLib
import copy

class Char:
    def __init__(self, name, type = None, parent_name = None, parent_type = None):
        self.name = name
        if len(name) == 1: self.ord = ord(name)
        else: self.ord = None # char is dummy, unicode unavailable 
        if type is None:
            if len(name) == 1: self.type = 'reg' 
            else: self.type = 'dummy'
        else: self.type = type # 'reg' 'dummy' 'reduced'
        self.parent_name = parent_name
        self.parent_type = parent_type # 'phonetic' 'dummy' 'reduced' 'alternative'

    def set_parent(self, parent_name, parent_type):
        self.parent_name = parent_name
        self.parent_type = parent_type

    def find_substitution_glyph(self, forest, displayed_chars, not_displayed_chars, display_subs, get_glyph_code, missing_glyphs, is_BMP):
        # print('processing ' + self.name)
        if self.parent_name == None or self.parent_name in not_displayed_chars or self.name in displayed_chars: 
            return self.get_glyph(display_subs.get(self.name,[]), get_glyph_code, missing_glyphs, is_BMP)
        else: 
            parent_result = forest.dict[self.parent_name].find_substitution_glyph(forest, displayed_chars, not_displayed_chars, display_subs, get_glyph_code, missing_glyphs, is_BMP)
            if parent_result is None: return self.get_glyph(display_subs.get(self.name,[]), get_glyph_code, missing_glyphs, is_BMP)
            else: return parent_result
    
    def get_glyph(self, sub_list, get_glyph_code, missing_glyphs, is_BMP):
        if self.type != 'reg' and len(sub_list) == 0: raise Exception("Missing Char Substitution Suggestions: " + self.name)
        if self.type == 'reg': add_to_sub_list = [self.name]
        else: add_to_sub_list = []
        for char_name in [*sub_list, *add_to_sub_list]:
            if len(char_name) > 1: raise Exception("Invalid Substitution Char: " + char_name)
            glyph_code = get_glyph_code(ord(char_name))
            if glyph_code is None: 
                if is_BMP is False or ord(char_name) < 16 ** 4: missing_glyphs.add(char_name)
            else: return char_name, glyph_code
        return None

class Forest:
    def __init__(self):
        self.dict = {None:None}
    
    def add(self, char, dup_chars): 
        if char.name in self.dict: 
            if dup_chars is not None: dup_chars.add(char.name)
        else: self.dict[char.name] = char

def parse(parent_name, children_string, forest, dup_chars, parent_type = 'phonetic', mode = None): # parent must be in forest, only children are added to the forest in this method 
    if parent_name not in forest.dict: raise Exception("Parent Missing: " + parent_name)
    if (children_string.count('(') != children_string.count(')') 
        or children_string.count('[') != children_string.count(']') 
        or children_string.count('{') != children_string.count('}')): 
        raise Exception("Format Error: " + children_string)
    if '\t' in children_string: parse(parent_name, children_string.replace('\t', '(', 1) + ')', forest, dup_chars, parent_type = parent_type, mode = mode); return
    nested_string = ''
    nesting = 0
    previous_char = parent_name
    for cursor in children_string:
        current_char = cursor
        if cursor in '([{': nesting += 1
        elif cursor in '}])': nesting -= 1
        if nesting == 0:
            if cursor == ']': current_char = nested_string + ']'
            if cursor == '}': parse(previous_char, nested_string[1:], forest, dup_chars, parent_type = 'alternative', mode = mode)
            elif cursor == ')': parse(previous_char, nested_string[1:], forest, dup_chars, parent_type = 'phonetic', mode = mode)
            elif current_char != parent_name: 
                if mode == 'init': forest.add(Char(current_char, parent_name = parent_name, parent_type = parent_type), dup_chars = dup_chars)
                if mode == 'mod' and parent_name is not None: forest.dict[current_char].set_parent(parent_name, parent_type)
                previous_char = current_char
            if cursor in '}])': nested_string = ''
        if nesting > 0: nested_string += cursor

def read_dict(file_name, forest, dup_chars, mode): # mode can be 'init' or 'mod'
    with open(file_name,'r',encoding='utf8') as file: lines = file.read().splitlines()
    for line in lines:
        if line[0] == '#': continue
        parse(None, line.split('\t#')[0], forest, dup_chars, mode = mode)

def read_subs(file_name):
    subs = dict()
    with open(file_name,'r',encoding='utf8') as file: lines = file.read().splitlines()
    for line in lines:
        if line[0] == '#': continue
        l = line.split('\t#')[0].split('\t')
        subs[l[0]] = l[1:]
    return subs

# Main
font_dir = 'SourceHan/'; src_dir = 'src/'; log_dir = 'log/'

font_path = font_dir + 'SourceHanSans-Regular.ttf' 
font_output = font_dir + 'SourceHanSansPhonetic-Regular.ttf' 

forest =  Forest()
dup_chars = set()
read_dict(src_dir + 'phonograph_dict.txt', forest, dup_chars, mode = 'init')
read_dict(src_dir + 'phonograph_hierarchy.txt', forest, dup_chars, mode = 'mod')
read_dict(src_dir + 'phonograph_relation_mod.txt', forest, dup_chars, mode = 'mod')
displayed_chars = Forest()
read_dict(src_dir + 'phonograph_displayed.txt', displayed_chars, None, mode = 'init')
not_displayed_chars = Forest()
read_dict(src_dir + 'phonograph_not_displayed.txt', not_displayed_chars, None, mode = 'init')
subs = read_subs(src_dir + 'phonograph_display_subs.txt')

font = ttLib.TTFont(font_path)

all_accounted_chars = set(); all_displayed_chars = set(); missing_glyphs = set()
# glyph_labels_to_include = set(font.getGlyphOrder()); glyph_labels_sub_to = set()
for cmap,ori_cmap in zip(font['cmap'].tables,copy.deepcopy(font['cmap'].tables)):
    if (cmap.platformID,cmap.platEncID) in [(0,3), (3,1)]: is_BMP = True
    elif (cmap.platformID,cmap.platEncID) in [(0,4), (0,6), (3,10)]: is_BMP = False
    else: continue
    for char_ord in ori_cmap.cmap:
        char = chr(char_ord)
        if char not in forest.dict: continue
        if char is None or forest.dict[char].type != 'reg': continue
        map_to_char_and_glyph = forest.dict[char].find_substitution_glyph(forest, displayed_chars.dict, not_displayed_chars.dict, subs, ori_cmap.cmap.get, missing_glyphs, is_BMP)
        if map_to_char_and_glyph is None: continue
        map_to_char, cmap.cmap[char_ord] = map_to_char_and_glyph
        all_accounted_chars.add(char); all_displayed_chars.add(map_to_char)
#            glyph_labels_to_include.discard(ori_cmap.cmap[char_ord]); glyph_labels_sub_to.add(cmap.cmap[char_ord])
# glyph_labels_to_include.update(glyph_labels_sub_to)

"""
glyph_labels_to_include2 = set()
for cmap in font['cmap'].tables:
    for char_ord in cmap.cmap:
        glyph_labels_to_include2.add(cmap.cmap[char_ord])

glyph_labels_to_include.update(glyph_labels_to_include2)
"""

with open(log_dir + 'missing_glyphs.txt',"w",encoding="utf8") as f:
    f.write('\n'.join(sorted(missing_glyphs)))
with open(log_dir + 'chars_covered.txt',"w",encoding="utf8") as f:
    f.write('\n'.join(sorted(all_accounted_chars)))
with open(log_dir + 'chars_displayed.txt',"w",encoding="utf8") as f:
    f.write('\n'.join(sorted(all_displayed_chars)))

font.save(font_output); print('font saved, deleting excessive glyphs')

font = ttLib.TTFont(font_output)
glyph_labels_to_include = set()
for cmap in font['cmap'].tables:
    for char_ord in cmap.cmap:
        glyph_labels_to_include.add(cmap.cmap[char_ord])

glyphs_to_include_file_name = log_dir + 'glyph_labels_to_include.txt'
with open(glyphs_to_include_file_name,"w",encoding="utf8") as f:
    f.write(','.join(sorted(glyph_labels_to_include)))

subprocess.run('pyftsubset ' + font_output + ' --output-file=' + font_output + ' --glyphs-file=' + glyphs_to_include_file_name, shell=True) # may not work, try changing the format of the input file 
print('done')