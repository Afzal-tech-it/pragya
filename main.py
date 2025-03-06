import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your actual Telegram Bot Token
BOT_TOKEN = "7494544837:AAFMouohAjg58JegavaMNNWkd75JQvFwc3A"

# Replace with your SerpAPI key
SERPAPI_KEY = "c19ad7790d39936fa397e268018b1e660065facb7c4eabaafef8e31b76497176"

def search_google(query):
    """Fetch direct answers from Google using SerpAPI."""
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": SERPAPI_KEY
    }
    response = requests.get(url, params=params).json()

    # Debug: Print response to check what SerpAPI returns
    print("DEBUG RESPONSE:", response)

    # Extract direct answer if available
    answer_box = response.get("answer_box", {})
    if "answer" in answer_box:
        return f"✅ {answer_box['answer']}"
    elif "snippet" in answer_box:
        return f"✅ {answer_box['snippet']}"

    # Extract organic search results (fallback)
    organic_results = response.get("organic_results", [])
    if organic_results:
        title = organic_results[0]["title"]
        link = organic_results[0]["link"]
        snippet = organic_results[0].get("snippet", "")
        return f"🔎 *{title}*\n_{snippet}_\n[Read more]({link})"

    return f"❌ Sorry! I couldn't find a direct answer.\n🔍 [Search on Google](https://www.google.com/search?q={query.replace(' ', '+')})"


async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the user starts the bot."""
    username = update.effective_user.first_name
    await update.message.reply_text(f"Hello, {username}! 🤖\nAsk me anything, and I'll find answers for you!")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle user queries and fetch answers from Google."""
    query = update.message.text
    response = search_google(query)
    await update.message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=True)

def main():
    """Main function to run the bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
