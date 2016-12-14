import easygui as g
import sys

# g.msgbox('This is a testing!')
# g.msgbox("Hello, world!")
# g.msgbox("Danger, Will Robinson!", "Warning!")
# g.msgbox("Backup complete!", ok_button="Good job!")

# msg = "Do you want to continue?"
# title = "Please Confirm"
# if g.ccbox(msg, title):     # show a Continue/Cancel dialog
#     pass  # user chose Continue
# else:  # user chose Cancel
#     sys.exit(0)


choices = ["Yes","No","Only on Friday"]
reply = g.choicebox("Do you like to eat fish?", choices=choices)