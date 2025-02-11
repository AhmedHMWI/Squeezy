import json

class Complaint:
    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    def save_complaint(self):
        """ Save the complaint to a JSON file """
        complaint_data = {
            "name": self.name,
            "email": self.email,
            "message": self.message
        }

        try:
            with open("complaints.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(complaint_data)

        with open("complaints.json", "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def get_complaints():
        """ Retrieve all complaints from the JSON file """
        try:
            with open("complaints.json", "r") as file:
                data = json.load(file)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

