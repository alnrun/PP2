import re

s = input().strip()
print("Yes" if re.fullmatch(r"ab*", s) else "No")