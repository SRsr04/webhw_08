from models_and_load_data import Author, Quote

while True:
    command = input("Enter command (e.g., 'name: Steve Martin', 'tag:life', 'tags:life,live', 'exit'): ").split(':')
    
    if command[0] == 'exit':
        break
    elif command[0] == 'name':
        author_name = command[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(f"{author.fullname}: {quote.quote}")
        else:
            print(f"No author found with name '{author_name}'")
    elif command[0] == 'tag':
        tag = command[1].strip()
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            print(f"{quote.author.fullname}: {quote.quote}")
    elif command[0] == 'tags':
        tags = command[1].split(',')
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print(f"{quote.author.fullname}: {quote.quote}")
    else:
        print("Invalid command format. Please try again.")
