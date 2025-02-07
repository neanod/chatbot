from ast import For
from bot import Bot, helper_tool_list, tools_list, genai_client
from google.genai import types
from prompts import bot_helper_prompt, deep_bot_prompt
from colorama import Fore
from datetime import datetime
import colorama


colorama.init()


class DeepBot:
    def __init__(
        self,
        model: str = "gemini-2.0-flash",
        call_limit: int = 10,
    ):
        self.model = model
        self.call_limit = call_limit
        self.slave = Bot(
            sys_prompt=bot_helper_prompt,
            toolset=helper_tool_list,
        )
        self.client = genai_client
        self.toolset = tools_list
        self.sys_prompt = deep_bot_prompt
        self.config = types.GenerateContentConfig(
			automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
			system_instruction=self.sys_prompt,
			tools=self.toolset,
			response_modalities=["TEXT"],
			safety_settings=[
				types.SafetySetting(
					category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
					threshold=types.HarmBlockThreshold.BLOCK_NONE,
				),
				types.SafetySetting(
					category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
					threshold=types.HarmBlockThreshold.BLOCK_NONE,
				),
				types.SafetySetting(
					category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
					threshold=types.HarmBlockThreshold.BLOCK_NONE,
				),
				types.SafetySetting(
					category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
					threshold=types.HarmBlockThreshold.BLOCK_NONE,
				),
			]
		)
        self.chat = self.client.chats.create(
            model=self.model,
            config=self.config,
        )
    
    def send_message(self, message: str) -> str:
        print("Generating Research")
        filename = f"./logs/{datetime.now().time()}.txt".replace(":", ".")
        with open(file=filename, mode="w") as f:
            f.write("LOGGING\n")
        log_file = open(filename, "a")
        
        # creating master_response from user text
        master_response = self.chat.send_message(message=message).text.replace("SUBTASK SUBTASK SUBTASK", "")
        to_log = f"{Fore.YELLOW}<<<MASTER: {master_response}{Fore.RESET}"
        log_file.write("\n" + to_log)
        print(to_log)
        i = 0
        while True:
            if "FINALANSWER" in master_response.upper().replace(" ", ""):
                # final answer, obviosly
                log_file.write("\n" + "-" * 30 + "\n" + master_response)
                log_file.close()
                log_file = open(filename, "r")
                log_log = log_file.read()
                log_file.close()
                with open("to_send.txt", "w") as f:
                    f.write(log_log)
                return master_response
            if i >= self.call_limit:
                to_log = f"{Fore.CYAN}Research attempt failed, retrying{Fore.RESET}"
                log_file.write("\n" + to_log)
                final_result = self.send_message(message=message)
                return final_result
            i += 1
            slave_response = self.slave.send_message(message=master_response)
            to_log = f"{Fore.GREEN}<<<SLAVE: {slave_response}{Fore.RESET}"
            log_file.write("\n" + to_log)
            print(to_log)
            master_response = self.chat.send_message(message=slave_response)
            if master_response.text is None:
                print("master_response text is None")
                print(*master_response.candidates)
                continue
            master_response = master_response.text.replace("SUBTASK SUBTASK SUBTASK", "")
            to_log = f"{Fore.YELLOW}<<<MASTER: {master_response}{Fore.RESET}"
            log_file.write("\n" + to_log)
            print(to_log)


if __name__ == "__main__":
    response=DeepBot().send_message("hi")
    # response=DeepBot().send_message("Run pyton code to get sum of first n prime numbers (test it on some numbers that youll choose). It is requied to RUN code, not just guess its result")
    print("-"*40)
    print(f"{Fore.RED}{response}{Fore.RESET}")