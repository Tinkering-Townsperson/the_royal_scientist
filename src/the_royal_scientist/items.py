import richeradventurelib as adv  # noqa

adv.Item.colour = "undistinguished"
adv.Item.description = "a generic thing"
adv.Item.edible = False
adv.Item.wearable = False
adv.Item.moveable = True

red_book = adv.Item("worn red book", "book")
red_book.colour = "red"
red_book.description = "a worn red book with a mysterious substance splattered on it. The title is \"Notes\""
red_book.text = """ENTRY NUMBER 17:

DARK,
DARKER, YET DARKER,
THE DARKNESS KEEPS GROWING,
THE SHADOWS CUTTING DEEPER,
PHOTON READINGS... NEGATIVE
THIS NEXT EXPERIMENT, SEEMS
VERY,
VERY,
INTERESTING

...

WHAT DO YOU TWO THINK?
"""

computer = adv.Item("computer", "desk computer")
computer.description = "A computer on the desk. There is a sticky note on the screen that says \"\""
computer.moveable = False
