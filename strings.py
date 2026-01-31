#strings in python are surrounded by either single quotation marks, or double quotation marks
print("Hello")
print('Hello')

#Quotes Inside Quotes
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

#multiline strings
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)
#or you can use single quotes

a = "Hello, World!"
print(a[1])

for x in "banana":
  print(x)

#string length
a = "Hello, World!"
print(len(a))

#slicing strings
b = "Hello, World!"
print(b[2:5]) # will be llo

b = "Hello, World!"
print(b[:5]) #will be Hello

b = "Hello, World!"
print(b[2:]) #will be ello, World!

#modify strings
a = "Hello, World!"
print(a.upper()) # will be HELLO, WORLD!

a = "Hello, World!"
print(a.lower()) # will be hello, world!

a = " Hello, World! "
print(a.strip()) # will be "Hello, World!"

a = "Hello, World!"
print(a.replace("H", "J")) # will be "Jello, World!"

a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']

#string concatenation
a = "Hello"
b = "World"
c = a + b
print(c) #HelloWorld

a = "Hello"
b = "World"
c = a + " " + b
print(c) # Hello World

#format strings
age = 36
txt = f"My name is John, I am {age}"
print(txt)

price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)

#escape characters
"""
\'	Single Quote	
\\	Backslash	
\n	New Line	
\r	Carriage Return	
\t	Tab	
\b	Backspace	
\f	Form Feed	
\ooo	Octal value	
\xhh	Hex value
"""