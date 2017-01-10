import sys
from termcolor import colored, cprint

text = colored('1.Hello, World!', 'red', attrs=['reverse', 'blink'])
print(text)
cprint('2.Hello, World!', 'red', 'on_grey',attrs=['bold'])

print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
print_red_on_cyan('3.Hello, World!')
print_red_on_cyan('4.Hello, Universe!')

for i in range(10):
    cprint(i, 'magenta', end=' ')

cprint("5.Attention!", 'red', attrs=['bold'], file=sys.stderr)

"""
Text Properties

Text colors:

grey
red
green
yellow
blue
magenta
cyan
white
Text highlights:

on_grey
on_red
on_green
on_yellow
on_blue
on_magenta
on_cyan
on_white
Attributes:

bold
dark
underline
blink
reverse
concealed
Terminal properties

Terminal	bold	dark	underline	blink	reverse	concealed
xterm	yes	no	yes	bold	yes	yes
linux	yes	yes	bold	yes	yes	no
rxvt	yes	no	yes	bold/black	yes	no
dtterm	yes	yes	yes	reverse	yes	yes
teraterm	reverse	no	yes	rev/red	yes	no
aixterm	normal	no	yes	no	yes	yes
PuTTY	color	no	yes	no	yes	no
Windows	no	no	no	no	yes	no
Cygwin SSH	yes	no	color	color	color	yes
Mac Terminal	yes	no	yes	yes	yes	yes
"""