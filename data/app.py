from bson.objectid import ObjectId
from flask import Flask, render_template
from markdown import markdown
from pymongo import MongoClient

app = Flask(__name__)
import os

from dotenv import load_dotenv

load_dotenv()
# MongoDB setup
print("Connecting to MongoDB...")
if not os.environ.get("MONGODB_HOST"):
    raise ValueError("MONGODB_HOST environment variable is not set.")
collection = MongoClient(os.environ.get("MONGODB_HOST"))["chat-history"]["sessions"]


@app.route("/")
def home():
    chats = list(collection.find().sort("updated_at", -1))

    for chat in chats:
        full_chat_md = ""
        for message in chat.get("chat_history", []):
            role = message.get("role", "").capitalize()
            content = message.get("content", "")
            full_chat_md += f"**{role}:**\n\n{content}\n\n---\n\n"
        chat["rendered_markdown"] = markdown(full_chat_md)

    return render_template("index.html", chats=chats)


if __name__ == "__main__":
    app.run(debug=True)
