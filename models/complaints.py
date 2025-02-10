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

        # Read the existing complaints from the file
        try:
            with open("complaints.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Append the new complaint
        data.append(complaint_data)

        # Write the updated list of complaints back to the file
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

