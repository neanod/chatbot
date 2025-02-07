import logging
from telegram import Update
from deep_bot import DeepBot
from google.genai import errors
from telegram.ext import (
	ApplicationBuilder,
	ContextTypes,
	MessageHandler,
	filters,
)

with open("tg_key", "r") as f:
	TOKEN = f.read()

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO
)
logger = logging.getLogger(__name__)

def generate_response(message: str) -> str:
	bot = DeepBot()
	if not message.strip():
		return "empty message detected"
	try:
		response = bot.send_message(message=message)
		return response
	except errors.ClientError as e:
		return f"resource exhausted {e}"
	except Exception as e:
		return(str(e.args))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	if update.message and update.message.text:
		user_text = update.message.text
		response = generate_response(user_text)
		await update.message.reply_text(response)
		with open("to_send.txt", "rb") as file:
			await update.message.reply_document(document=file, filename="to_send.txt")

def main():
	app = ApplicationBuilder().token(TOKEN).build()
	app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
	app.run_polling()

if __name__ == '__main__':
	main()
