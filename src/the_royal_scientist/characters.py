import richeradventurelib as adv


class Character(adv.Item):
	def __init__(self, name, description, context):
		super().__init__(name)
		self.description = description
		self.context = context
		self.current_quest = ""


asgore = Character(
	"asgore",
	"The king of the underground. He has a long beard and wears a crown.",
	"king",
)
