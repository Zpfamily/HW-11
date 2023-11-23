from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Phone should be 10 digits and only numbers')

class Birthday:
    def __init__(self):
        self._dates = []

    def add_date(self, date_birthday):
        try:
            date_birthday = datetime.strptime(date_birthday, '%d.%m.%Y').date()
        except ValueError:
            return "Invalid date format. Example: day.month.year(01.01.2000)"

        if date_birthday in self._dates:
            return "Date already exists"

        self._dates.append(date_birthday)
        return None  # No error

    def days_to_next_birthday(self):
        today = datetime.now().date()

        if not self._dates:
            return None

        next_birthday = min(
            (date.replace(year=today.year) if date.replace(year=today.year) >= today
             else date.replace(year=today.year + 1))
            for date in self._dates
        )

        days_to_birthday_value = (next_birthday - today).days
        return days_to_birthday_value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday()

    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {[str(phone) for phone in self.phones]}, date of birthday: {', '.join(date.strftime('%d-%m-%Y') for date in self.birthday._dates)}, days_to_birthday: {self.birthday.days_to_next_birthday()} days)"

    def __str__(self):
        return f"Contact name: {self.name.value},phones: {[str(p) for p in self.phones]},date of birthday: {', '.join(date.strftime('%d-%m-%Y') for date in self.birthday._dates)},days to birthday: {self.birthday.days_to_next_birthday()} days"

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone:
            phone.value = new_phone
        else:
            raise ValueError('Old phone not found')

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError('Phone not found')

    def add_birthday(self, date_birthday):
        return self.birthday.add_date(date_birthday)

    def days_to_birthday(self):
        return self.birthday.days_to_next_birthday()

class AddressBook(UserDict):
            
    def add_record(self, record: Record):
        if record.name.value in self.data:
            raise ValueError('Record already exists')
        else:
            self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)
   
    def delete(self, name: str):
        self.data.pop(name, None)
    
   
    def iterator(self, item_number):
        counter = 0
        result = ''
        
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
      

book = AddressBook()


    # Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("1234567890")
john_record.add_birthday('01.01.2006')
    # Додавання запису John до адресної книги
book.add_record(john_record)
# for name, record in book.data.items():
    # print(record)


   # Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday('15.02.1990')
book.add_record(jane_record)

boris_record = Record("Borys")
boris_record.add_phone("1234567895")
boris_record.add_birthday('01.05.1990')
book.add_record(boris_record)


    # Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)
    


    # Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555


for records_chunk in book.iterator(3):
    print(records_chunk)

     # Видалення запису Jane

book.delete("Jane")

