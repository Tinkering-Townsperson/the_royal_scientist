import richeradventurelib as adv
from . import items, characters  # noqa


class Room(adv.Room):
	def __init__(self, name, short_description, description):
		super().__init__(short_description + "\n" + description)
		self.name = name
		self.locked_exits = {
			"north": False,
			"south": False,
			"east": False,
			"west": False,
		}
		self.items = adv.Bag()
		self.characters = adv.Bag()
		self.interactive_objects = adv.Bag()
		self.short_desc = short_description


# Define the rooms

bedroom = Room(
	"Bedroom",
	"Your bedroom.",
	"There is a bed and a bookshelf with worn books splattered in a mysterious substance. A red book lies suspiciously askew on the shelf.",  # noqa
)

bedroom.items.add(items.red_book)

laboratory = Room(
	"Laboratory",
	"Your laboratory.",
	"There are various scientific instruments and experiments here. There is a desk with an old computer on it.",
)

laboratory.items.add(items.computer)

lab_entrance = Room(
	"Laboratory Entrance",
	"The entrance to the laboratory.",
	"There is an elevator to the north which leads to the castle, and a door to the east which leads back to your laboratory.",
)

elevator = Room(
	"Elevator",
	"The elevator.",
	"There is a button here to go up to the castle, and a button to go down to the laboratory.",
)

# elevator.locked_exits["north"] = True

castle_entrance = Room(
	"Castle Entrance",
	"The entrance to the castle.",
	"There is a large wooden door here, with a brass handle and a keyhole.",
)

throne_room = Room(
	"Throne Room",
	"The throne room.",
	"There are two large thrones here for the king and queen.",
)

throne_room.characters.add(
	characters.asgore
)


# Connect the rooms

bedroom.south = laboratory
laboratory.west = lab_entrance
lab_entrance.north = elevator
elevator.north = castle_entrance
castle_entrance.north = throne_room

# check /map.excalidraw for a visual representation of the map
