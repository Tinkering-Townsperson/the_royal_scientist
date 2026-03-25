import richeradventurelib as adv

from .computer import Computer
from . import rooms, items  # noqa
from time import sleep
import sys

current_room = rooms.bedroom
inventory = adv.Bag()

computer_interface = Computer(console=adv.console)
computer_interface.get_context = adv.get_context
computer_interface.set_context = adv.set_context
computer_interface.get_current_room = lambda: current_room

day = 0


def typewrite(text, delay=0.05, emphasis_delay=3.0, style="italic"):
	for line in text.splitlines():
		for char in line:
			adv.console.print(char, end="", style=style)
			sys.stdout.flush()
			sleep(delay)
		print()
		sleep(emphasis_delay if line == "..." else delay * 6)


# Item commands

@adv.when("inventory")
@adv.when("i")
@adv.when("inv")
def show_inventory():
	if len(inventory) == 0:
		adv.say("You are not carrying anything.")
	else:
		adv.say("You are carrying:")
		for item in inventory:
			adv.say(f"- {item.name}")


@adv.when("look")
def look():
	adv.say(current_room.short_desc)


@adv.when("look at ITEM")
def look_at(item: str):
	global inventory, current_room

	obj = current_room.items.find(item)
	if not obj:
		obj = inventory.find(item)
		if not obj:
			adv.say(f"I can't find {item} anywhere.")
		else:
			adv.say(f"You have {item}.")
	else:
		adv.say(f"You see {item}.")


@adv.when("take ITEM")
@adv.when("get ITEM")
@adv.when("pickup ITEM")
@adv.when("pick up ITEM")
@adv.when("grab ITEM")
def take_item(item: str):
	global current_room

	obj = current_room.items.find(item)

	if not obj:
		adv.say(f"I don't see {item} here.")
	elif not obj.moveable:
		adv.say(f"You try to pick up {item}.")
		sleep(0.5)
		adv.say("...")
		sleep(2)
		adv.say(f"You can't pick up {item} --- it's not moveable.")
		sleep(0.5)
		adv.say("Now your back hurts. Ouch.")
		sleep(0.5)
	else:
		adv.say(f"You now have {obj.description}.")
		current_room.items.take(item)
		inventory.add(obj)


@adv.when("inspect ITEM")
def inspect_item(item: str):
	global inventory, current_room

	obj = inventory.find(item)
	if not obj:
		obj = current_room.items.find(item)
		if not obj:
			adv.say(f"I can't find {item} anywhere.")
			return

	adv.say(f"You inspect {item}.")
	adv.say(obj.description)


@adv.when("read ITEM")
def read_item(item: str):
	global inventory

	obj = inventory.find(item)

	if not obj:
		adv.say(f"You don't have {item}.")
		return

	if hasattr(obj, "text"):
		adv.say(f"You read {item}.\n\n")

		typewrite(obj.text)
	else:
		adv.say(f"You try to read {item}.")
		sleep(0.5)
		adv.say("...")
		sleep(2)
		adv.say("But there was nothing to read.")
		sleep(0.5)


# Computer commands

@adv.when("logon")
def log_on():
	global current_room

	if adv.get_context() == "logged_in":
		adv.say("You are already logged in.")
		return

	computer = current_room.items.find("computer")

	if not computer:
		adv.say("There is no computer here, doofus :clown:! Aren't you a doctor or something?")
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
		adv.console.print(f"Showing directory tree of {computer_interface.directory}:")
		for file in files:
			adv.console.print(file)
	else:
		adv.console.print("There are no files here.")


@adv.when("echo", text="")
@adv.when("echo TEXT")
@computer_interface.check_logged_in
def echo(text: str):
	adv.console.print(text, end="")


@adv.when("pwd")
@computer_interface.check_logged_in
def pwd():
	adv.console.print(computer_interface.directory, end="")


@adv.when("clear")
@computer_interface.check_logged_in
def clear():
	adv.console.clear()


@adv.when("cat FILE")
@computer_interface.check_logged_in
def cat(file: str):
	content = computer_interface.directory_tree.get(computer_interface.directory, {}).get(file)

	if content:
		typewrite(content, delay=0.03, emphasis_delay=0.03)
	else:
		adv.console.print(f"File {file} not found.", end="")


@adv.when("wingfetch")
@computer_interface.check_logged_in
def wingfetch():
	computer_interface.wingfetch()


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
			adv.say(f"You can't go {direction} --- the door is locked.")
		else:
			current_room = next_room
			adv.say(f"You go {direction}.")
			look()

	else:
		adv.say("You walk into the wall. Ouch. Why would you do that?")


@adv.when("describe")
def describe_room():
	"""Print the full description of the room."""
	adv.say(current_room)

	# Are there any items here?
	for item in current_room.items:
		adv.say(f"There is {item.description} here.")


@adv.when("talk to CHARACTER")
def talk_to(character: str):
	global current_room

	char = current_room.characters.find(character)

	if not char:
		adv.say(f"There is no {character} here to talk to.")
	else:
		adv.say(f"You talk to {char.name}.")
		adv.say(char.description)


def prompt():
	ctx = adv.get_context()

	if ctx == "logged_in":
		return f"[bold green]gaster@LabPC[/]: [bold blue]{computer_interface.directory}[/]$ "
	else:
		return "> "


def no_command_matches(command):
	if computer_interface.logged_in:
		adv.console.print(f"-wish: {command}: command not found", end="")
	else:
		adv.say(f"\"{command}\" does nothing here.")


def start_game():
	adv.console.clear()
	adv.console.rule("[bold]Welcome to [italic]The Royal Scientist[/italic]![/bold]")
	adv.say("""You're Dr. WD Gaster, the royal scientist of the kingdom.

You have been working on a secret experiment in your laboratory,
but something has gone wrong. You wake up one day to find yourself
locked in your bedroom, with no memory of how you got there.


""")
	# print("Type 'help' for a list of commands.")
	adv.set_context(None)
	adv.prompt = prompt
	adv.no_command_matches = no_command_matches
	look()
	adv.start(help=False)
