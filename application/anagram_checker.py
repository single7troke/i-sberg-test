from collections import defaultdict


def is_anagram(first_str, second_str):
	char_count = defaultdict(int)

	for char in first_str:
		char_count[char] += 1

	for char in second_str:
		char_count[char] -= 1

	for v in char_count.values():
		if v != 0:
			return False

	return True
