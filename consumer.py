import json
import pika
from time import sleep
from mongoengine import connect, Document, StringField, BooleanField

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

def send_email(contact_id):
    # Функція-заглушка для імітації надсилання повідомлення по email
    print(f"Sending email to contact with ID {contact_id}")
    sleep(2)  # Імітація тривалості відправлення
    print(f"Email sent to contact with ID {contact_id}")

def callback(ch, method, properties, body):
    # Обробка повідомлень з RabbitMQ черги
    contact_data = json.loads(body)
    contact_id = contact_data.get('contact_id')

    if contact_id:
        contact = Contact.objects(id=contact_id, message_sent=False).first()
        if contact:
            send_email(contact_id)
            contact.message_sent = True
            contact.save()

# Підписка на отримання повідомлень з RabbitMQ
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Consumer is waiting for messages. To exit press CTRL+C')
channel.start_consuming()
