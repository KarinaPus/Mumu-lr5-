import csv
import pickle
import os
from typing import List, Optional


class Person:
    def __init__(self, surname: str, gender: str, height: int):
        self.surname = surname
        self.gender = gender.upper()
        self.height = int(height)

    def to_dict(self):
        return {"surname": self.surname, "gender": self.gender, "height": self.height}

    @staticmethod
    def from_dict(d):
        return Person(d["surname"], d["gender"], int(d["height"]))


class Group:
    def __init__(self, persons: Optional[List[Person]] = None):
        self.persons = persons or []

    @classmethod
    def from_dict(cls, dct):
        persons = [Person(surn, g, h) for surn, (g, h) in dct.items()]
        return cls(persons)

    def average_female_height(self) -> Optional[float]:
        females = [p.height for p in self.persons if p.gender.startswith('F') or p.gender == 'Ж' or p.gender == 'W']
        if not females:
            return None
        return sum(females) / len(females)

    def tallest_male_surname(self) -> Optional[str]:
        males = [p for p in self.persons if p.gender.startswith('M') or p.gender == 'М' or p.gender == 'H']
        if not males:
            return None
        tallest = max(males, key=lambda p: p.height)
        return tallest.surname

    def has_duplicate_heights(self) -> bool:
        heights = [p.height for p in self.persons]
        return len(heights) != len(set(heights))

    def find_by_surname(self, surname: str) -> Optional[Person]:
        s = surname.strip()
        for p in self.persons:
            if p.surname.lower() == s.lower():
                return p
        return None


class Serializer:
    @staticmethod #периписать ,медиана и мод карточки где регуляоки и на классы 
    def save_csv(path: str, group: Group):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['surname', 'gender', 'height'])
            for p in group.persons:
                writer.writerow([p.surname, p.gender, p.height])

    @staticmethod
    def load_csv(path: str) -> Group:
        persons = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                persons.append(Person.from_dict({
                    'surname': row['surname'],
                    'gender': row['gender'],
                    'height': int(row['height'])
                }))
        return Group(persons)

    @staticmethod
    def save_pickle(path: str, group: Group):
        with open(path, 'wb') as f:
            pickle.dump([p.to_dict() for p in group.persons], f)

    @staticmethod
    def load_pickle(path: str) -> Group:
        with open(path, 'rb') as f:
            data = pickle.load(f)
        persons = [Person.from_dict(d) for d in data]
        return Group(persons)


def demo():
    # Исходные данные (словарь: фамилия -> (пол, рост))
    initial = {
        'Ivanov': ('M', 180),
        'Petrova': ('F', 165),
        'Sidorov': ('M', 190),
        'Kuznetsova': ('F', 170),
        'Smirnov': ('M', 175),
        'Lenina': ('F', 160),
        'Orlov': ('M', 190)  # duplicate height with Sidorov to test duplicates
    }

    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, 'people.csv')
    pkl_path = os.path.join(base_dir, 'people.pkl')

    group = Group.from_dict(initial)

    # Сохранение в оба формата
    Serializer.save_csv(csv_path, group)
    Serializer.save_pickle(pkl_path, group)

    print('Данные сохранены в', csv_path, 'и', pkl_path)

    # Выбор формата для чтения
    fmt = input('Выберите формат для загрузки (csv/pickle) [csv]: ').strip().lower() or 'csv'
    if fmt == 'pickle' or fmt == 'pkl':
        group = Serializer.load_pickle(pkl_path)
    else:
        group = Serializer.load_csv(csv_path)

    # Запросы
    avg_female = group.average_female_height()
    if avg_female is None:
        print('В группе нет женщин.')
    else:
        print(f'Средний рост женщин: {avg_female:.2f} см')

    tallest_male = group.tallest_male_surname()
    if tallest_male is None:
        print('В группе нет мужчин.')
    else:
        print('Фамилия самого высокого мужчины:', tallest_male)

    dup = group.has_duplicate_heights()
    print('Есть ли хотя бы два человека одного роста?:', 'Да' if dup else 'Нет')

    # Поиск по фамилии, введённой с клавиатуры
    q = input('Введите фамилию для поиска: ').strip()
    if q:
        person = group.find_by_surname(q)
        if person:
            print('Найдено: ', person.to_dict())
        else:
            print('Человек с фамилией', q, 'не найден.')


if __name__ == '__main__':
    demo()
#абстранктный и вм зип рекулярку и буквы и примеры как в карточкай и про ооп инит мексины абстрактные классовые методы 
