from functools import wraps
from time import sleep, perf_counter
from rich.console import Console

PASSWORD = "wingdings"


class Computer:
	def __init__(self, console: Console):
		self.start_time = perf_counter()
		self.logged_in = False
		self.directory = "/"
		self.console = console

		self.directory_tree = {
			"/": {
				"readme.txt": """# NOTES

in order to unlock the elevator, you need to unscramble the clues in the files in this directory.

Very very interesting...""",
			}
		}

	def log_on(self):
		password = self.console.input("password: [italic]").strip()

		if password == PASSWORD:
			self.console.print("Access granted.")
			self.logged_in = True
			self.set_context("logged_in")
			self.wingfetch()
		else:
			self.console.print("Incorrect password.")

	def log_off(self):
		self.logged_in = False
		self.set_context(None)
		self.console.print("You log off the computer.")

	def wingfetch(self):
		"""neofetch but fictional"""

		widget = f"""\
[black on white]░░░░░░░░░░░░░░░░░░░░░░░░░[/]⠀[bold cyan]gaster[white]@[cyan]LabPC[/][/bold cyan]
[black on white]░░██═╗░░░░░░░░░░░░░░╔██╗░[/]⠀────────────
[black on white]░████████╗░░░░╔═████████╗[/]⠀[bright_yellow]OS:[/] DELTA
[black on white]░███░░█████████████░░███║[/]⠀[bright_yellow]Kernel:[/] Linux 6.6.6
[black on white]░████░░░███░░░███░░░████║[/]⠀[bright_yellow]Host:[/]
[black on white]░█████░░░███░███░░░█████║[/]⠀[bright_yellow]Uptime:[/] {perf_counter() - self.start_time:.2f} seconds
[black on white]░╚█████████████████████╔╝[/]⠀[bright_yellow]Shell:[/] wish v6.6
[black on white]░░╚█████░███████░█████╔╝░[/]⠀[bright_yellow]Terminal:[/] tty0
[black on white]░░░╚███░░░█████░░░███╔╝░░[/]⠀[bright_yellow]
[black on white]░░░░░╚█████░░░█████╔═╝░░░[/]⠀[bright_yellow]
[black on white]░░░░░░░╚████░████╔═╝░░░░░[/]⠀[bright_yellow]
[black on white]░░░░░░░░░╚█████╔═╝░░░░░░░[/]⠀[black]██[red]██[green]██[yellow]██[blue]██[magenta]██[cyan]██[white]██[/]
[black on white]░░░░░░░░░░╚════╝░░░░░░░░░[/]⠀[brighT_black]██[bright_red]██[bright_green]██[bright_yellow]██[bright_blue]██[bright_magenta]██[bright_cyan]██[bright_white]██[/]"""  # noqa,

		for line in widget.splitlines():
			self.console.print(line)
			sleep(0.1)

	def check_logged_in(self, function):
		@wraps(function)
		def wrapper(*args, **kwargs):
			if self.logged_in:
				return function(*args, **kwargs)

			self.console.print("You need to log in to use the computer... try typing 'logon'")

		return wrapper
