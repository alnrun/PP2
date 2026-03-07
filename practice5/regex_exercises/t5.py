import re

s = input()
print("Yes" if re.fullmatch(r"a.*b", s) else "No")