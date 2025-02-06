from json import tool
from pprint import pp
from urllib import response
from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown
from google.genai import types, Client
from bot_tools import tools_list
import warnings


warnings.filterwarnings("ignore", category=UserWarning)
with open("key", "r") as f:
	KEY = f.read()
console = Console()
genai_client = Client(api_key=KEY)


class Bot():
	def __init__(
			self,
			sys_prompt: str = "You are helpful assistant developed by neanod. That is not what you need to play like, but that is literally who you are.",
			model: str = "gemini-2.0-flash",
			) -> None:
		self.model = model
		self.messages: list[dict] = [
			{
				"role": "system",
				"content": sys_prompt
			}
		]
		self.client: Client = genai_client
		self.config = types.GenerateContentConfig(
			tools=tools_list,
			automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
			system_instruction=sys_prompt,
			response_modalities=["TEXT"],
		)
		self.chat = self.client.chats.create(
			model=self.model,
			config=self.config,
		)
	
	def create_response(self, message: str):
		if not message.strip(): raise ValueError("Empty Message")
		response = self.chat.send_message(message)
		return response
	
	def send_message(self, message: str, stream: bool = False):
		# response = (self.create_response if stream else )(message=message)
		if stream:
			raise ValueError("stream is not ready yet")
		response = self.create_response(message)
		if response.candidates[0].grounding_metadata is not None:
			if response.candidates[0].grounding_metadata.search_entry_point is not None:
				print("Web search used")

		return response.text

		
			

if __name__ == "__main__":
	bot = Bot(sys_prompt="You are helpful assistant. If you will get any errors from api you need to write them out so i can see it")
	print(bot.send_message("When the next solar eclipce would be in sibir'. Search the web for this information"))
	# print(bot.send_message("Send me notification with title 'Title' and message 'some words' and tell me how many r's in strawberry"))
	# print(bot.send_message("Change the lights to warm and bright 50% and send me notification if everything is ok"))