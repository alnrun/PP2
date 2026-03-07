import re

s = input().strip()
parts = re.split(r"(?<!^)(?=[A-Z])", s)
print(",".join([p for p in parts if p]))