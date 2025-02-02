from jarvis import Bot
import colorama


alex = Bot("Your name is Alex. Your color is blue. You are from Minecraft")
steve = Bot("Your name is Steve. Your color is red. You are from Minecraft")

response2 = "Hi"
input()
for i in range(20):
	print(colorama.Fore.BLUE)
	response1 = alex.get_response(response2)
	print(response1)
	print(colorama.Fore.RED)
	response2 = steve.get_response(response1)
	print(response2)
	print(colorama.Fore.RESET)