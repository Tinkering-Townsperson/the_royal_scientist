from functools import wraps

PASSWORD = "wingdings"


class Computer:
	def __init__(self):
		self.logged_in = False
		self.directory = "/"

		self.directory_tree = {
			"/": {
				"readme.txt": "Very very interesting...",
			}
		}

	def log_on(self):
		password = input("password:\n> ")

		if password == PASSWORD:
			print("Access granted.")
			self.logged_in = True
			self.set_context("logged_in")
		else:
			print("Incorrect password.")

	def log_off(self):
		self.logged_in = False
		self.set_context(None)
		print("You log off the computer.")

	def check_logged_in(self, function):
		@wraps(function)
		def wrapper(*args, **kwargs):
			if not self.logged_in:
				if not self.get_current_room().items.find("computer"):
					print("There is no computer here.")
					return

				print("You need to log in to use the computer.")
				return

			return function(*args, **kwargs)

		return wrapper
