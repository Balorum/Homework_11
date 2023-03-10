from collections import UserDict
from datetime import datetime, date


class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    def __init__(self, name):
        self.name = name


class Phone(Field):
    @property
    def value(self):
        return self.__phone

    @value.setter
    def value(self, new_value):
        self.__phone = None
        if len(new_value) > 13:
            print(f"{new_value} is too long phone")
        elif len(new_value) < 10:
            print(f"{new_value} is too short phone")
        elif not new_value[1:].isdigit():
            print(f"{new_value} phone can consist only from numbers")
        else:
            self.__phone = new_value


class Birthday(Field):
    @property
    def value(self):
        return self.__birthday

    @value.setter
    def value(self, new_value):
        self.__birthday = None
        birth_split = new_value.split("-")
        birthday = datetime(
            year=int(birth_split[-1]),
            month=int(birth_split[1]),
            day=int(birth_split[0]),
        )
        if birthday > datetime.now():
            print("you haven't been born yet :)")
        else:
            self.__birthday = birthday


class Record:
    phones = []
    birthday = datetime(year=1000, month=1, day=1)

    def __init__(self, name):
        self.name = name

    def change_phone(self, phone):
        self.phones = phone

    def del_phone(self, ind):
        self.phones.pop(ind)

    def days_to_birthday(self):
        new_date = date(
            datetime.now().year,
            self.birthday.value.month,
            self.birthday.value.day,
        )
        today_day = datetime.now().date()
        if today_day > new_date:
            new_date = date(
                datetime.now().year + 1,
                self.birthday.value.month,
                self.birthday.value.day,
            )
        days_to_birth = new_date - today_day
        return days_to_birth.days


class AddressBook(UserDict):
    counter = 0

    def add_record(self, record):
        self.data[record[0]] = record

    def iterator(self, counts):
        print(
            "You have selected the display mode 2 contacts at a time, to exit it - enter '.'"
        )
        flag = ""
        myiter = iter(self)
        while flag != ".":
            flag = input("Enter next for next page or '.' to exit: ")
            if flag == "next":
                for i in range(int(counts)):
                    print(next(myiter))

    def __iter__(self):
        return self

    def __next__(self):
        counter = AddressBook.counter
        result = []
        if counter >= len(self.data):
            AddressBook.counter = 0
            counter = 0
        if counter < len(self.data):
            names = list(self.data.keys())
            result.append(self.data[names[counter]])
            res = ""
            for val in result:
                res += f"{val.name.name}: "
                if val.phones:
                    res += f"{list(map(lambda x: x.value, val.phones))}: "
                if val.birthday != datetime(year=1000, month=1, day=1):
                    res += f"{val.birthday.value.date()}"
        AddressBook.counter += 1
        return res


record_1 = Record(Name("Marina"))
record_1.phones = [Phone("+32524546346"), Phone("+23432557346")]
record_1.birthday = Birthday("22-11-2000")

record_2 = Record(Name("Ivan"))
record_2.phones = [
    Phone("+32524546346"),
    Phone("+234325457346"),
    Phone("+364575846834"),
]
record_2.birthday = Birthday("02-01-1993")

record_3 = Record(Name("Peter"))
record_3.phones = [Phone("+32524546346")]
record_3.birthday = Birthday("17-05-1997")

record_4 = Record(Name("Edward"))
record_4.phones = [Phone("+86707808436"), Phone("+9845726457")]
record_4.birthday = Birthday("18-02-1992")

record_5 = Record(Name("Bill"))
record_5.birthday = Birthday("18-06-1989")

record_6 = Record(Name("Klim"))
record_6.phones = [Phone("+634746858674"), Phone("+458568675674")]

book = AddressBook(
    {
        "Marina": record_1,
        "Ivan": record_2,
        "Peter": record_3,
        "Edward": record_4,
        "Bill": record_5,
        "Klim": record_6,
    }
)


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError as val:
            print(f"{args[0][2:]} is not a correct value")
        except KeyError as key:
            print(f"{args[0][1]} is not your contact or telephone is incorrect")
        except IndexError as ind:
            print("You entered an invalid command")

    return wrapper


@input_error
def hello_handler(*args):
    if len(args[0]) != 1:
        raise IndexError
    print("How can I help you?")


@input_error
def add_handler(*args):
    flag = True
    if len(args[0]) < 2:
        raise IndexError
    name = Name(args[0][1])
    record = Record(name)
    if "-" in args[0][-1]:
        birth_date = Birthday(args[0][-1])
        if birth_date.value:
            record.birthday = birth_date
        if len(args[0]) > 3:
            phone = []
            for i in range(len(args[0]) - 3):
                phone.append(Phone(args[0][i + 2]))
                if not phone[i].value:
                    flag = False
            if flag:
                record.phones = phone
    elif len(args[0]) > 2:
        phone = []
        for i in range(len(args[0]) - 2):
            phone.append(Phone(args[0][i + 2]))
            if not phone[i].value:
                flag = False
            if flag:
                record.phones = phone
    book[record.name.name] = record


@input_error
def show_handler(*args):
    if len(args[0]) != 2:
        raise IndexError
    print("Your contacts")
    for val in book.data.values():
        result = f"{val.name.name}: "
        if val.phones:
            result += f"{list(map(lambda x: x.value, val.phones))}: "
        if val.birthday != datetime(year=1000, month=1, day=1):
            result += f"{val.birthday.value.date()}"
        print(result)


@input_error
def phone_handler(*args):
    if len(args[0]) != 2:
        raise IndexError
    if args[0][1] not in book.data.keys():
        raise KeyError
    else:
        phone_list = list(map(lambda x: x.value, book.data[args[0][1]].phones))
        for i in phone_list:
            print(i)


@input_error
def change_handler(*args):
    if args[0][1] not in book.data.keys():
        raise KeyError
    else:
        new_phone = []
        for i in range(len(args[0]) - 2):
            new_phone.append(Phone(args[0][i + 2]))
        change_record = book.data[args[0][1]]
        change_record.change_phone(new_phone)
        book[change_record.name.name] = change_record


@input_error
def del_handler(*args):
    if args[0][1] not in book.data.keys():
        raise KeyError
    else:
        if args[0][2] in list(map(lambda x: x.value, book.data[args[0][1]].phones)):
            phone_list = list(map(lambda x: x.value, book.data[args[0][1]].phones))
            new_record = book.data[args[0][1]]
            new_record.del_phone(phone_list.index(args[0][2]))
            book[new_record.name.name] = new_record
        else:
            raise KeyError


def iterat_handler(*args):
    book.iterator(args[0][1])


def birth_handler(*args):
    if args[0][1] not in book.data.keys():
        raise KeyError
    else:
        contacts_record = book.data[args[0][1]]
        print(contacts_record.days_to_birthday())


@input_error
def exit_handler(*args):
    if len(args[0]) > 2:
        raise IndexError
    print("Good bye!")
    return "Good bye!"


COMMANDS = {
    "hello": hello_handler,
    "change": change_handler,
    "add": add_handler,
    "phone": phone_handler,
    "show": show_handler,
    "close": exit_handler,
    "exit": exit_handler,
    "good": exit_handler,
    "delete": del_handler,
    "birthday": birth_handler,
    "records": iterat_handler,
}


def get_handler(handler):
    return COMMANDS[handler]


def main():
    print(
        """
Hello, I am assistant-bot. My commands: \n
hello
add ...
change ...
phone ...
delete ...
birthday (????\'?? ????????????????)
show all
close/exit/good bye 
"""
    )
    while True:
        handler = input("?????????????? ??????????????: ")
        command_list = handler.lower().split(" ")
        event_handler_list = handler.split(" ")
        if handler == ".":
            break
        event_handler = get_handler(command_list[0])
        end_flag = event_handler(event_handler_list)
        if end_flag == "Good bye!":
            break
        else:
            continue


if __name__ == "__main__":
    main()
