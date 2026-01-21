import json

class Database:
    def add_data(self, name, email, password):

        try:
            with open("db.json", "r") as rf:
                database = json.load(rf)
        except (FileNotFoundError, json.JSONDecodeError):
            database = {}                     # 🔹 Handle empty or missing file safely

        if email in database:
            return 0
        else:
            database[email] = [name, password]

            with open("db.json", "w") as wf:
                json.dump(database, wf, indent=4)

            return 1


    def search(self, email, password):

        try:
            with open("db.json", "r") as rf:
                database = json.load(rf)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

        if email in database and database[email][1] == password:
            return 1
        return 0
