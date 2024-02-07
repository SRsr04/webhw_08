import json
import uuid
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField
import pika

# Підключення до MongoDB
connect('your_database_name', host='mongodb+srv://romapy04:12000202@romapycluster.5gcjtap.mongodb.net/?retryWrites=true&w=majority')

# Оголошення моделі для контакту
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

# Параметри підключення до RabbitMQ
connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
channel.queue_declare(queue='email_queue')

fake = Faker()

# Генерація фейкових контактів та їх запис у базу даних та в RabbitMQ чергу
for _ in range(5):  # Замініть 5 на бажану кількість контактів
    contact = Contact(
        full_name=fake.name(),
        email=fake.email(),
    ).save()

    # Отримання ObjectId збереженого контакту та відправлення його в RabbitMQ чергу
    contact_id = str(contact.id)
    message_body = json.dumps({'contact_id': contact_id})
    channel.basic_publish(exchange='', routing_key='email_queue', body=message_body)

print("Contacts generated and sent to RabbitMQ queue")

# Закриття з'єднання з RabbitMQ
connection.close()
