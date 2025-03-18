import csv

def parse_key(key):
	vowels = "aeiouə"
	first_vowel_index = -1
	for i, char in enumerate(key):
		if char in vowels:
			if char == 'i' and any(v in key[i+1:] for v in vowels):
				continue
			first_vowel_index = i
			break
	if first_vowel_index != -1:
		return key[:first_vowel_index+1].replace('ʱ', ''), key[first_vowel_index+1:].replace('ʰ', '').replace('ˀ', '')
	return key.replace('ʱ', ''), ""

def read_pairs(file_path):
	pairs = []
	with open(file_path, 'r', encoding='utf-8') as file:
		for line in file:
			if line.startswith('#') or line.startswith('音') or line.startswith('-') or not line.strip():
				continue
			key, item = line.strip().split('\t')[:2]
			item = item.replace('!', '')
			pairs.append((key, item))
	return pairs

def create_table(pairs):
	rows = set()
	cols = set()
	table_dict = {}

	for key, item in pairs:
		row, col = parse_key(key)
		rows.add(row)
		cols.add(col)
		if row not in table_dict:
			table_dict[row] = {}
		if col not in table_dict[row]:
			table_dict[row][col] = item
		else:
			table_dict[row][col] += item

	vowel_order = "aeiouə"
	rows = sorted(rows, key=lambda x: [vowel_order.index(c) if c in vowel_order else len(vowel_order) + ord(c) for c in x])
	cols = ["", "ŋ", "k", "u", "uk", "i", "n", "t", "m", "p"]

	table = [[""] + cols]
	for row in rows:
		table_row = [row] + [table_dict[row].get(col, "") for col in cols]
		table.append(table_row)

	return table

def write_markdown(table, output_file):
	with open(output_file, 'w', encoding='utf-8') as file:
		# Write the header row
		file.write("| " + " | ".join(table[0]) + " |\n")
		file.write("|" + " --- |" * len(table[0]) + "\n")
		# Write the data rows
		for row in table[1:]:
			file.write("| " + " | ".join(row) + " |\n")

def main(input_file, output_file):
	pairs = read_pairs(input_file)
	table = create_table(pairs)
	write_markdown(table, output_file)

if __name__ == "__main__":
	input_file = 'phonographemes/phonographeme_usage_chart.txt'  # Replace with your input file path
	output_file = 'phonographemes/phonographeme_usage_chart.md'  # Replace with your desired output file path
	main(input_file, output_file)