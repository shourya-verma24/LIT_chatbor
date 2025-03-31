import os
import discord
import nltk
import threading
from flask import Flask, render_template, request
from dotenv import load_dotenv
from nltk.chat.util import Chat, reflections
from discord.ext import commands

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Define chatbot responses
pairs = [
    [r"hi|hello|hey", ["Hello! How can I assist you today?"]],
    [r"(.*)admission(.*)", ["Admission details are available on our website."]],
    [r"(.*)courses(.*)", ["We offer B.Tech, M.Tech, MBA, and PhD programs."]],
    [r"(.*)fees(.*)", ["The fee structure varies by course. Please check our finance section."]],
    [r"(.*)library(.*)", ["The library is open from 9 AM to 7 PM on weekdays."]],
    [r"bye|goodbye", ["Goodbye! Have a great day!"]],
    [r"(.*)", ["I'm not sure about that. Please contact the college helpdesk."]]
]

chatbot = Chat(pairs, reflections)

# Flask app setup
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def chatbot_response():
    user_message = request.args.get("msg")
    response = chatbot.respond(user_message)
    return response

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    response = chatbot.respond(message.content)
    await message.channel.send(response)

# Run Flask in a separate thread
def run_flask():
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    # Start Flask in a new thread
    threading.Thread(target=run_flask, daemon=True).start()

    # Run Discord bot
    bot.run(TOKEN)
