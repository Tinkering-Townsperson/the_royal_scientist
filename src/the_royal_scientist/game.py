import richeradventurelib as adv

from .computer import Computer
from . import rooms, items  # noqa
from time import sleep
import sys

current_room = rooms.bedroom
inventory = adv.Bag()

computer_interface = Computer()
computer_interface.get_context = adv.get_context
computer_interface.set_context = adv.set_context
computer_interface.get_current_room = lambda: current_room

day = 0


# Item commands

@adv.when("inventory")
@adv.when("i")
@adv.when("inv")
def show_inventory():
	if len(inventory) == 0:
		print("You are not carrying anything.")
	else:
		print("You are carrying:")
		for item in inventory:
			print(f"- {item.name}")


@adv.when("look")
def look():
	print(current_room.short_desc)


@adv.when("look at ITEM")
def look_at(item: str):
	global inventory, current_room

	obj = current_room.items.find(item)
	if not obj:
		obj = inventory.find(item)
		if not obj:
			print(f"I can't find {item} anywhere.")
		else:
			print(f"You have {item}.")
	else:
		print(f"You see {item}.")


@adv.when("take ITEM")
@adv.when("get ITEM")
@adv.when("pickup ITEM")
@adv.when("pick up ITEM")
@adv.when("grab ITEM")
def take_item(item: str):
	global current_room

	obj = current_room.items.find(item)

	if not obj:
		print(f"I don't see {item} here.")
	elif not obj.moveable:
		print(f"You try to pick up {item}.")
		sleep(0.5)
		print("...")
		sleep(2)
		print(f"You can't pick up {item} --- it's not moveable.")
		sleep(0.5)
		print("Now your back hurts. Ouch.")
		sleep(0.5)
	else:
		print(f"You now have {obj.description}.")
		current_room.items.take(item)
		inventory.add(obj)


@adv.when("inspect ITEM")
def inspect_item(item: str):
	global inventory, current_room

	obj = inventory.find(item)
	if not obj:
		obj = current_room.items.find(item)
		if not obj:
			print(f"I can't find {item} anywhere.")
			return

	print(f"You inspect {item}.")
	print(obj.description)


@adv.when("read ITEM")
def read_item(item: str):
	global inventory

	obj = inventory.find(item)

	if not obj:
		print(f"You don't have {item}.")
		return

	if hasattr(obj, "text"):
		print(f"You read {item}.\n\n")

		for line in obj.text.splitlines():
			for char in line:
				print(char, end="")
				sys.stdout.flush()
				sleep(0.05)
			print()
			sleep(3 if line == "..." else 0.5)
	else:
		print(f"You try to read {item}.")
		sleep(0.5)
		print("...")
		sleep(2)
		print("But there was nothing to read.")
		sleep(0.5)


# Computer commands

@adv.when("logon")
def log_on():
	global current_room

	if adv.get_context() == "logged_in":
		print("You are already logged in.")
		return

	computer = current_room.items.find("computer")

	if not computer:
		print("There is no computer here.")
		return

	computer_interface.log_on()


@adv.when("logoff")
@computer_interface.check_logged_in
def log_off():
	computer_interface.log_off()


@adv.when("ls")
@computer_interface.check_logged_in
def ls():
	files = computer_interface.directory_tree.get(computer_interface.directory, {}).keys()

	if files:
		print(f"Showing directory tree of {computer_interface.directory}:")
		for file in files:
			print(file)
	else:
		print("There are no files here.")


@adv.when("cat FILE")
@computer_interface.check_logged_in
def cat(file: str):
	content = computer_interface.directory_tree.get(computer_interface.directory, {}).get(file)

	if content:
		print(content)
	else:
		print(f"File {file} not found.")


# Movement

@adv.when("go DIRECTION")
@adv.when("north", direction="north")
@adv.when("south", direction="south")
@adv.when("east", direction="east")
@adv.when("west", direction="west")
@adv.when("n", direction="north")
@adv.when("s", direction="south")
@adv.when("e", direction="east")
@adv.when("w", direction="west")
def go(direction: str):
	global current_room

	next_room = current_room.exit(direction)

	if next_room:
		if (
			direction in current_room.locked_exits
			and current_room.locked_exits[direction]
		):
			print(f"You can't go {direction} --- the door is locked.")
		else:
			current_room = next_room
			print(f"You go {direction}.")
			look()

	else:
		print("You walk into the wall. Ouch. Why would you do that?")


@adv.when("describe")
def describe_room():
	"""Print the full description of the room."""
	adv.say(current_room)

	# Are there any items here?
	for item in current_room.items:
		print(f"There is {item.description} here.")


def prompt():
	ctx = adv.get_context()

	if ctx == "logged_in":
		return f"gaster@LabPC: {computer_interface.directory}$ "
	else:
		return "> "


def start_game():
	print("Welcome to The Royal Scientist!")
	print("""You're Dr. WD Gaster, the royal scientist of the kingdom.

You have been working on a secret experiment in your laboratory,
but something has gone wrong. You wake up one day to find yourself
locked in your bedroom, with no memory of how you got there.""")
	# print("Type 'help' for a list of commands.")
	adv.set_context(None)
	adv.prompt = prompt
	look()
	adv.start(help=False)
