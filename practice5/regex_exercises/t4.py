import re

s = input()
matches = re.findall(r"[A-Z][a-z]+", s)
print(" ".join(matches))