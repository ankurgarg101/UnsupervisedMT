"""
Module that filters out the lines with incorrect unicode
"""

base_path = '../../conala-clean/'
with open(base_path + 'conala-mined.intent.old', 'r', encoding="utf-8") as ifp, open(base_path + 'conala-mined.snippet.old', 'r', encoding="utf-8") as sfp:

	intents = ifp.readlines()
	snippets = sfp.readlines()
	count = 0
	with open(base_path + 'conala-mined.intent', 'w', encoding="utf-8") as iwfp, open(base_path + 'conala-mined.snippet', 'w', encoding="utf-8") as swfp:
		sz = len(intents)
		for i in range(sz):
			add=True
			for ch in list(snippets[i].rstrip()):

				if ord(ch) >= 128 or ord(ch) < 32:
					add=False
					count += 1
					break
			if add:
				iwfp.write(intents[i])
				swfp.write(snippets[i].replace('\\', '#SLASH#'))

print(count)