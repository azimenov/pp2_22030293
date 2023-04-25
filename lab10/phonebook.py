import psycopg2
import csv


class CSVManager:
    def getAllEntries(self):
        dataSet = []
        with open("data/sample.csv") as file:
            reader = csv.reader(file)
            for i in reader:
                dataSet.append(i)
        return dataSet[1:]


class DBManager:

    def __init__(self, fileM):
        self.conn = None
        self.fileM = fileM
        self.cursor = None

    def checkIfExists(self, table_name):
        query = f"""
            SELECT *
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'test'
            AND TABLE_NAME = '{table_name}'
            """

        self.cursor.execute(query)
        return bool(self.cursor.fetchone())

    def createTable(self):
        query = """
            CREATE TABLE lab10.test.PhoneBook(
                id SERIAL,
                phone VARCHAR(11),
                name VARCHAR(255)
            )
            """

        self.cursor.execute(query)

    def insertData(self, name, phone):
        query = f"""
            INSERT INTO lab10.test.phonebook ("phone", "name")
            VALUES ('{phone}', '{name}')
        """
        self.cursor.execute(query)

    def updateDate(self, whichName, whichPhone, name, phone):
        updatedFields = ""
        if len(phone) > 1:
            updatedFields += f"phone = '{phone[:11]}',"
        if len(name) > 1:
            updatedFields += f"name = '{name}',"

        if updatedFields:
            query = f"""UPDATE lab10.test.phonebook 
            SET {updatedFields[:-1]} WHERE name = '{whichName}' AND phone = '{whichPhone}'"""
            self.cursor.execute(query)
        else:
            raise Exception("Empty fields")

    def insertDataFromSet(self, data):
        for i in data:
            self.insertData(name=i[0], phone=i[1])

    def addCSV(self):
        newData = self.fileM.getAllEntries()
        oldData = [[i[2], i[1]] for i in self.getAllPhones()]
        filtered = [i for i in newData if i not in oldData]
        self.insertDataFromSet(filtered)

    def deleteAllPhones(self):
        query = """DELETE FROM lab10.test.phonebook"""
        self.cursor.execute(query)

    def deleteById(self, id):
        query = f"""DELETE FROM lab10.test.phonebook WHERE id = '{id}'"""
        self.cursor.execute(query)

    def getAllPhones(self):
        query = """
            SELECT * FROM lab10.test.phonebook
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def getPhonesByName(self, name):
        query = f"""
            SELECT * FROM lab10.test.phonebook WHERE name = '{name}'
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()

    def commit(self):
        self.conn.commit()

    def connect(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="lab10",
            user="postgres",
            port="5432",
            password="Dias2004")
        self.cursor = self.conn.cursor()
        # execute a statement

        if not self.checkIfExists("phonebook"):
            self.createTable()
            self.commit()


class InteractionManagaer:
    def __init__(self):
        self.fileM = CSVManager()
        self.db = DBManager(self.fileM)
        self.db.connect()

    def start(self):
        print("""
                1 to get all data
                1.1 to filter data by name
                2 to add CSV file
                3 to write new data from console
                4 to update data
                5 to delete by username
                6 to delete everything
            """)
        action = input("""Enter number: """)
        match action:
            case "1":
                print("*" * 8)
                output = self.db.getAllPhones()
                for i in output:
                    print(f"ID: {i[0]}, name: {i[2]}, phone: {i[1]}")
            case "1.1":
                name = input("Enter filter name: ")
                output = self.db.getPhonesByName(name)
                for i in output:
                    print(f"ID: {i[0]}, name: {i[2]}, phone: {i[1]}")
            case "2":
                self.db.addCSV()
                self.db.commit()
            case "3":
                name = input("Enter name: ")
                phone = input("Enter phone number: ")
                phone = phone[:11]
                try:
                    self.db.insertData(name, phone)
                    self.db.commit()
                    print("Added successfully")
                except Exception as e:
                    print("Error")
            case "4":
                whichName = input("Which contact to update (Enter name):")
                whichPhone = input("Which contact to update (Enter phone):")
                newName = input("Enter new name or leave blank:")
                newPhone = input("Enter new password or leave blank:")
                try:
                    if whichName.strip() != "" and len(whichPhone) == 11:
                        self.db.updateDate(whichName, whichPhone, newName, newPhone)
                        self.db.commit()
                        print("OK")
                    else:
                        print("Invalid input")
                except Exception as e:
                    print(f"Something went wrong {e}")

            case "5":
                name = input("Enter name: ")
                try:
                    output = self.db.getPhonesByName(name)
                    for i in output:
                        print(f"--> ID: {i[0]}, name: {i[2]}, phone: {i[1]}")
                    if output:
                        phoneId = input("Enter id to delete: ")
                        self.db.deleteById(phoneId)
                        self.db.commit()
                        print("Deleted")
                    else:
                        print("Nothing to delete")
                except Exception as e:
                    print(f"Something went wrong {e}")
            case "6":
                self.db.deleteAllPhones()
                self.db.commit()
        self.db.close()


mng = InteractionManagaer()
mng.start()
