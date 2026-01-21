import os
from tkinter import *
from tkinter import messagebox
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env file")


class Database:
    def __init__(self):
        self.file = "db.json"
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump({}, f)

    def add_data(self, name, email, password):
        with open(self.file, "r") as f:
            data = json.load(f)

        if email in data:
            return False

        data[email] = [name, password]

        with open(self.file, "w") as f:
            json.dump(data, f)

        return True

    def search(self, email, password):
        with open(self.file, "r") as f:
            data = json.load(f)

        return email in data and data[email][1] == password


class EmotionEngine:
    def __init__(self):
        self.client = Groq(api_key=API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def sentiment(self, text):
        prompt = f"""
        Classify the emotion of the text strictly as:
        Positive, Neutral, or Negative.

        Text: "{text}"

        Respond with only one word.
        """
        res = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return res.choices[0].message.content.strip()

    def language(self, text):
        prompt = f"""
        Detect the language of the text.
        Respond with only the language name.

        Text: "{text}"
        """
        res = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return res.choices[0].message.content.strip()

    def ner(self, text):
        prompt = f"""
        Extract named entities from the text.
        Categorize into Person, Organization, Location.

        Text: "{text}"
        """
        res = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return res.choices[0].message.content.strip()


class EmotionAnalyzerGUI:
    def __init__(self):
        self.db = Database()
        self.engine = EmotionEngine()

        self.root = Tk()
        self.root.title("Emotion Analyzer")
        self.root.geometry("420x520")
        self.root.configure(bg="#E8F5FD")
        self.root.iconbitmap("resources/favicon.ico")

        self.login_gui()
        self.root.mainloop()

    def clear(self):
        for w in self.root.pack_slaves():
            w.destroy()

    def login_gui(self):
        self.clear()

        Label(self.root, text="Emotion Analyzer",
              bg="#E8F5FD", fg="#1DA1F2",
              font=("Verdana", 24, "bold")).pack(pady=30)

        Label(self.root, text="Email", bg="#E8F5FD").pack()
        self.email = Entry(self.root, width=40)
        self.email.pack(ipady=5)

        Label(self.root, text="Password", bg="#E8F5FD").pack(pady=10)
        self.password = Entry(self.root, width=40, show="*")
        self.password.pack(ipady=5)

        Button(self.root, text="Login", width=30, height=2,
               bg="#1DA1F2", fg="white",
               command=self.login).pack(pady=15)

        Button(self.root, text="Register", width=30, height=2,
               command=self.register_gui).pack()

    def login(self):
        if self.db.search(self.email.get(), self.password.get()):
            self.home_gui()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register_gui(self):
        self.clear()

        Label(self.root, text="Register",
              bg="#E8F5FD", fg="#1DA1F2",
              font=("Verdana", 22, "bold")).pack(pady=30)

        self.name = Entry(self.root, width=40)
        self.name.pack(ipady=5)
        self.email = Entry(self.root, width=40)
        self.email.pack(ipady=5, pady=10)
        self.password = Entry(self.root, width=40, show="*")
        self.password.pack(ipady=5)

        Button(self.root, text="Create Account",
               width=30, height=2,
               bg="#1DA1F2", fg="white",
               command=self.register).pack(pady=15)

        Button(self.root, text="Back", width=30,
               command=self.login_gui).pack()

    def register(self):
        if self.db.add_data(self.name.get(), self.email.get(), self.password.get()):
            messagebox.showinfo("Success", "Account created")
            self.login_gui()
        else:
            messagebox.showerror("Error", "Email already exists")

    def home_gui(self):
        self.clear()

        Label(self.root, text="Dashboard",
              bg="#E8F5FD", fg="#1DA1F2",
              font=("Verdana", 22, "bold")).pack(pady=30)

        Button(self.root, text="Sentiment Analysis",
               width=30, height=2,
               command=self.sentiment_gui).pack(pady=10)

        Button(self.root, text="Named Entity Recognition",
               width=30, height=2,
               command=self.ner_gui).pack(pady=10)

        Button(self.root, text="Language Detection",
               width=30, height=2,
               command=self.language_gui).pack(pady=10)

        Button(self.root, text="Logout",
               width=30, height=2,
               command=self.login_gui).pack(pady=20)

    def sentiment_gui(self):
        self.task_gui("Sentiment Analysis", self.engine.sentiment)

    def language_gui(self):
        self.task_gui("Language Detection", self.engine.language)

    def ner_gui(self):
        self.task_gui("Named Entity Recognition", self.engine.ner)

    def task_gui(self, title, func):
        self.clear()

        Label(self.root, text=title,
              bg="#E8F5FD", fg="#1DA1F2",
              font=("Verdana", 20, "bold")).pack(pady=20)

        text = Text(self.root, height=6, width=40)
        text.pack(pady=10)

        def run():
            result = func(text.get("1.0", END).strip())
            messagebox.showinfo("Result", result)

        Button(self.root, text="Analyze",
               width=30, height=2,
               command=run).pack(pady=10)

        Button(self.root, text="Go Back",
               width=30, height=2,
               command=self.home_gui).pack()


EmotionAnalyzerGUI()
