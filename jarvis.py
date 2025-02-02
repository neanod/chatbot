from openai import OpenAI
from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown


with open("key", "r") as f:
	KEY = f.read()

console = Console()
oai_client = OpenAI(
	api_key=KEY,
	base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class Bot():
	def __init__(
			self,
			sys_prompt: str = "You are JARVIS.",
			model: str = "gemini-2.0-flash-exp",
			) -> None:
		self.model = model
		self.messages: list[dict] = [
			{
				"role": "system",
				"content": sys_prompt
			}
		]
		self.all_text = ""
		self.client: OpenAI = oai_client
		self.temperature: float = 0.7

	def get_response_stream(self, prompt: str):
		try:
			self.messages.append(
				{
					"role": "user",
					"content": prompt,
				}
			)
			response = self.client.chat.completions.create(
				model="gemini-2.0-flash-exp",
				messages=self.messages,
				stream=True,
				temperature=self.temperature,
			)
			full_response: str = str()
			for chunk in response:
				if chunk.choices[0].delta.content is not None:
					full_response += chunk.choices[0].delta.content
					yield chunk.choices[0].delta.content
			self.messages.append(
				{
					"role": "assistant",
					"content": full_response
				}
			)
		except Exception as e:
			print("An unexcepted exception occured during generation.")
			if isinstance(e.args[0], str):
				if "User location is not supported for the API use." in e.args[0]:
					print(ConnectionError("VPN is not enabled!"))
					quit(-1)
			print(e)
			quit(-1)
	
	def get_response(self, prompt: str, md: bool = True) -> str:
		full_response: str = str()
		for chunk in self.get_response_stream(prompt=prompt):
			full_response += chunk
		if md:
			full_response = Markdown(full_response)
		return full_response
	
	def print_response_stream(self, prompt: str) -> None:
		generator = self.get_response_stream(prompt=prompt)
		with Live(console=console, refresh_per_second=10) as live:
			for chunk in generator:
				self.all_text += chunk
				md = Markdown(self.all_text)
				live.update(md)

