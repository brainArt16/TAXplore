from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    Application,
    ContextTypes,
)
from .rag import CoherePDFRAG
import logging

logger = logging.getLogger(__name__)


class TelegramChannel:
    def __init__(
        self, token: str, initial_text: str, help_text: str, bot_username: str = None
    ):
        self.initial_text = initial_text
        self.help_text = help_text
        self.bot_username = bot_username
        self.rag = CoherePDFRAG()
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(
            MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message)
        )
        self.app.add_error_handler(self.error)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(self.initial_text)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(self.help_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        question = update.message.text
        chat_type = update.message.chat.type
        collection_name = "default_collection"  # Modify dynamically if needed

        logger.info(
            f"Received question from {update.message.chat.id} in {chat_type}: {question}"
        )

        if chat_type == "group" and self.bot_username not in question:
            return

        response = self.process_chat_request(question, collection_name)
        await update.message.reply_text(
            response.get("result", "Sorry, I couldn't process your request.")
        )

    def process_chat_request(self, question, collection_name):
        try:
            vectorstore = self.rag.load_vectorstore_db(collection_name=collection_name)
            chain = self.rag.create_chain(vectorstore)
            return self.rag.get_answer(chain=chain, question=question)
        except Exception as e:
            logger.error(f"Error processing chat request: {e}")
            return {"result": "An error occurred while processing your request."}

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f"Update {update} caused error {context.error}")

    def start_polling(self):
        logger.info("Starting the bot...")
        self.app.run_polling()
