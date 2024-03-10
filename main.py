from AddressBook import AddressBook, Record, Name, Phone
from get_birthdays_per_week import get_birthdays_per_week
from datetime import datetime


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except ValueError:
            return "Give me name and phone please."

    return inner


@input_error
def add_contact(args, contacts: AddressBook):
    name, phone = args
    record = contacts.find(name)
    if record == None:
        record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."


@input_error
def add_birthday(args, contacts: AddressBook):
    name, birthday = args
    record = contacts.find(name)
    if record == None:
        return "Contact not found"
    record.add_birthday(birthday)
    return "Birthday added"


@input_error
def show_birthday(args, contacts: AddressBook):
    name = args
    name = name[0]

    record = contacts.find(name)
    if record == None:
        return "contact not found"

    return record.birthday.value


@input_error
def change_contact(args, contacts: AddressBook):
    name, old_phone, new_phone = args
    record = contacts.find(name)

    if record == None:
        return "contact not found"

    record.edit_phone(old_phone, new_phone)
    return "contact updated"


def output_error(func):
    def inner(args, kwargs):
        try:
            return func(args, kwargs)
        except IndexError:
            return "Give me name"

    return inner


@output_error
def show_phone(args, contacts: AddressBook):
    name = args

    if name == []:
        raise IndexError

    record = contacts.find(name[0])

    if record == None:
        return "contact not found"

    return record


def show_all(args, contacts: AddressBook):
    for name, record in contacts.data.items():
        yield record


def show_upcoming_birthdays(args, contacts: AddressBook):
    user_list = list()
    date_format = '%Y-%m-%d'
    for name, contact in contacts.items():
        if contact.birthday != None:
            user_list.append({
                "name": name,
                "birthday": datetime.strptime(contact.birthday.value, date_format)
            })
    get_birthdays_per_week(user_list)
    return "Done"


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        commands = {
            "add": add_contact,
            "change": change_contact,
            "phone": show_phone,
            "add-birthday": add_birthday,
            "show-birthday": show_birthday,
            "birthdays": show_upcoming_birthdays,
        }

        if command == "hello":
            print("How can I help you?")
        elif command == "all":
            for line in show_all(args, contacts):
                print(line)
        elif command in commands:
            print(commands[command](args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
