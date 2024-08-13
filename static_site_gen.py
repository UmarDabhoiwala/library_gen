import os
import markdown2
import json
from datetime import datetime

def parse_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.split('\n')
    book = {}
    current_key = None

    for line in lines:
        if line.startswith('# '):
            if current_key == 'Review':
                book[current_key] = book.get(current_key, '').strip()
            current_key = line[2:].strip()
            book[current_key] = ''
        elif current_key:
            book[current_key] += line + '\n'

    # Clean up all fields
    for key in book:
        book[key] = book[key].strip()

    # Convert review to HTML
    book['Review'] = markdown2.markdown(book['Review'])

    # Parse tags
    book['Tags'] = [tag.strip() for tag in book.get('Tags', '').split(',')]

    # Convert rating to integer
    book['Rating'] = int(book.get('Rating', '0'))

    return book

def generate_static_site(input_dir, output_dir):
    books = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(input_dir, filename)
            book = parse_md_file(file_path)
            books.append(book)

    # Sort books by Date Read (most recent first)
    def safe_date_parse(date_string):
        try:
            return datetime.strptime(date_string, '%Y-%m-%d')
        except ValueError:
            print(f"Warning: Invalid date format for '{date_string}'. Using minimum date.")
            return datetime.min

    books.sort(key=lambda x: safe_date_parse(x['Date Read']), reverse=True)

    # Generate JSON data file
    with open(os.path.join(output_dir, 'books.json'), 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    # Copy HTML, CSS, and JS files
    for file in ['index.html', 'styles.css', 'script.js']:
        with open(file, 'r', encoding='utf-8') as source_file:
            with open(os.path.join(output_dir, file), 'w', encoding='utf-8') as dest_file:
                dest_file.write(source_file.read())

if __name__ == "__main__":
    input_dir = "book_md_files"
    output_dir = "output"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_static_site(input_dir, output_dir)
    print(f"Static site generated in {output_dir}")
