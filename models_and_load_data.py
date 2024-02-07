import json
from mongoengine import connect, Document, StringField, DateTimeField, ListField
from datetime import datetime

from mongoengine import connect, Document, StringField, DateTimeField, ListField, ReferenceField
from datetime import datetime

# Оголошення моделі для авторів
class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

# Оголошення моделі для цитат
class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

# Підключення до MongoDB
connect('your_database_name', host='mongodb+srv://romapy04:12000202@romapycluster.5gcjtap.mongodb.net/?retryWrites=true&w=majority')


# Скрипт для завантаження даних з файлів у базу даних
def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            born_date = datetime.strptime(author_data['born_date'], "%B %d, %Y")
            author = Author(
                fullname=author_data['fullname'],
                born_date=born_date,
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

def load_quotes():
    with open('./quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                quote = Quote(
                    tags=quote_data['tags'],
                    author=author,
                    quote=quote_data['quote']
                )
                quote.save()

# Виклик функцій для завантаження даних
load_authors()
load_quotes()
