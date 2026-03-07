import re

s = input()
matches = re.findall(r"[a-z]+_[a-z]+", s)
print(" ".join(matches))