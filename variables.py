#creating variables
x = 5
y = 4
print(x)
print(y)

#casting
a = str(3) #a will be '3'
b = int(4) #b will be 4
c = float(5) #c will be 5.0

#get the type of a variable
w = 4
print(type(w)) # will be int

#variable names that we can use
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#cannot use
2myvar = "John"
my-var = "John"
my var = "John"

myVariableName = "John" #camel case
MyVariableName = "John" #pascal case
my_variable_name = "John" #snake case

#multiple variables
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

#one value to multiple variables
x = y = z = 'Orange'
print(x)
print(y)
print(z)

#global variables
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()
#we can create a variable inside a function, with the same name as the global variable
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)
#we can use a keyword global, to create a global variable inside a function
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)