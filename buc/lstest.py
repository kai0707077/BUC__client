import os, sys

output = os.popen('ls')
print(type(output.read()))
print(output.read())