import psycopg2
import csv
import pygame
import pygame_menu


class CSVManager:
    def getAllEntries(self):
        dataSet = []
        with open("data/sample1.csv") as file:
            reader = csv.reader(file)
            for i in reader:
                dataSet.append(i)
        return dataSet[1:]


class DBManager:
    offset = 2
    limit = 5

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

    def insertData(self, user_name, user_phone):
        query = """CREATE OR REPLACE PROCEDURE insert_or_update_user(user_name VARCHAR(255), user_phone VARCHAR(20))
        LANGUAGE plpgsql
        AS $$
        BEGIN
            DECLARE user_id INTEGER;
            SELECT id INTO user_id FROM users WHERE name = user_name;
            IF user_id IS NOT NULL THEN
                UPDATE users SET phone = user_phone WHERE id = user_id;
            ELSE
                INSERT INTO users (name, phone) VALUES (user_name, user_phone);
            END IF;
        END;
        $$;"""
        self.cursor.callproc(query, (user_name, user_phone))


    def ASCOrder(self):
        query = f"""SELECT * FROM lab10.test.phonebook ORDER BY name ASC"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def insertDataFromSet(self, data):
        for i in data:
            self.insertData(name=i[0], phone=i[1])

    def pagination(self):
        query = f"""SELECT * FROM lab10.test.phonebook LIMIT {DBManager.limit} OFFSET {DBManager.offset}"""
        self.cursor.execute(query)
        DBManager.offset += DBManager.limit
        return self.cursor.fetchall()


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
            SELECT * FROM lab10.test.phonebook WHERE name LIKE '{name}'
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()

    def commit(self):
        self.conn.commit()

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
        
    def getPhonesByPattern(self, pattern):
        query = f"""
            SELECT * FROM lab10.test.phonebook WHERE name LIKE '%{pattern}%' OR phone LIKE '%{pattern}%'
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    

    def connect(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="lab10",
            user="postgres",
            port="5432",
            password="Prazdnik21")
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
                2 to filter data by name
                3 to add CSV file
                4 to write new data from console
                5 to delete by username
                6 to delete everything
                7 to find by pattern
                8 pagination
                9 asc order in name
                10 to update
            """)
        action = input("""Enter number: """)
        match action:
            case "1":
                print("*" * 8)
                output = self.db.getAllPhones()
                for i in output:
                    print(f"ID: {i[0]}, name: {i[2]}, phone: {i[1]}")
            case "2":
                name = input("Enter filter name: ")
                output = self.db.getPhonesByName(name)
                for i in output:
                    print(f"ID: {i[0]}, name: {i[2]}, phone: {i[1]}")
            case "3":
                self.db.addCSV()
                self.db.commit()
            case "4":
                name = input("Enter name: ")
                phone = input("Enter phone number: ")
                phone = phone[:11]
                try:
                    self.db.insertData(name, phone)
                    self.db.commit()
                    print("Added successfully")
                except Exception as e:
                    print(e)

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
            case "7":
                sample = input("Enter a pattern: ")
                output = self.db.getPhonesByPattern(sample)
                for element in output:
                    print(f"{element[2]}: {element[1]}")
            case "8":
                output = self.db.pagination()
                for element in output:
                    print(element)
            case "9":
                output = self.db.ASCOrder()
                for element in output:
                    print(element)
            case "10":
                whichName = input("Which contact to update (Enter name):")
                whichPhone = input("Which contact to update (Enter phone):")
                newName = input("Enter new name or leave blank:")
                newPhone = input("Enter new phone or leave blank:")
                try:
                    if whichName.strip() != "" and len(whichPhone) == 11:
                        self.db.updateDate(whichName, whichPhone, newName, newPhone)
                        self.db.commit()
                        print("OK")
                    else:
                        print("Invalid input")
                except Exception as e:
                    print(f"Something went wrong {e}")

        self.db.close()


mng = InteractionManagaer()
mng.start()
