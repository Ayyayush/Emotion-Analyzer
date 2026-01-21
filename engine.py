# ===================== IMPORTS =====================
import os
import sys
from groq import Groq
from dotenv import load_dotenv


# ===================== LOAD ENV =====================
load_dotenv()                                        # Loads .env file
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("❌ GROQ_API_KEY not found")
    sys.exit()


# ===================== MAIN APP CLASS =====================
class NLPApp:

    def __init__(self):
        """
        Constructor:
        - Initializes in-memory user database
        - Starts the first menu
        """
        self.__database = {}                          # {email: [name, password]}
        self.client = Groq(api_key=API_KEY)           # Groq client
        self.model = "llama-3.3-70b-versatile"
        self.__first_menu()


    # ===================== FIRST MENU =====================
    def __first_menu(self):
        first_input = input("""
        👋 Welcome to Emotion Analyzer!
        How would you like to proceed?

        1. Not a member? Register
        2. Already a member? Login
        3. Exit

        👉 Your choice: """)

        if first_input == '1':
            self.__register()
        elif first_input == '2':
            self.__login()
        else:
            print("👋 Exiting Emotion Analyzer. Bye!")
            sys.exit()


    # ===================== REGISTER =====================
    def __register(self):
        name = input("👤 Enter your name: ")
        email = input("📧 Enter your email: ")
        password = input("🔑 Enter your password: ")

        if email in self.__database:
            print("⚠️ Email already registered. Please login.")
            self.__first_menu()
        else:
            self.__database[email] = [name, password]
            print("✅ Registration successful! Please login.")
            self.__login()


    # ===================== LOGIN =====================
    def __login(self):
        email = input("📧 Enter your email: ")
        password = input("🔑 Enter your password: ")

        if email in self.__database and self.__database[email][1] == password:
            print(f"✅ Welcome, {self.__database[email][0]}!")
            self.__second_menu()
        else:
            print("❌ Invalid email or password.")
            self.__first_menu()


    # ===================== SECOND MENU =====================
    def __second_menu(self):
        second_input = input("""
        🧠 Emotion Analyzer Dashboard

        1. Named Entity Recognition (NER)
        2. Language Detection
        3. Emotion (Sentiment) Analysis
        4. Logout

        👉 Your choice: """)

        if second_input == '1':
            self.ner()
        elif second_input == '2':
            self.language_detection()
        elif second_input == '3':
            self.sentiment_analysis()
        elif second_input == '4':
            print("👋 Logged out successfully!")
            self.__first_menu()
        else:
            print("⚠️ Invalid choice.")
            self.__second_menu()


    # ===================== NER =====================
    def ner(self):
        text = input("📝 Enter text for NER: ")

        prompt = f"""
        Extract named entities from the text below.
        Categorize them into Person, Organization, Location.

        Text:
        "{text}"
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        print("📌 Entities Found:")
        print(response.choices[0].message.content.strip())

        self.__second_menu()


    # ===================== LANGUAGE DETECTION =====================
    def language_detection(self):
        text = input("🌐 Enter text for language detection: ")

        prompt = f"""
        Detect the language of the following text.
        Respond with only the language name.

        Text:
        "{text}"
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        print("🌍 Detected Language:")
        print(response.choices[0].message.content.strip())

        self.__second_menu()


    # ===================== SENTIMENT / EMOTION =====================
    def sentiment_analysis(self):
        text = input("💬 Enter text for emotion analysis: ")

        prompt = f"""
        Classify the emotion of the following text strictly as:
        Positive, Neutral, or Negative.

        Text:
        "{text}"

        Respond with only one word.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        print("📊 Emotion Result:")
        print(response.choices[0].message.content.strip())

        self.__second_menu()


# ===================== APP START =====================
if __name__ == "__main__":
    NLPApp()
