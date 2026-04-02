import sqlite3
import hashlib

class LibraryDB:
    def __init__(self, db_name="library_final.db"):
        self.db_name = db_name
        self._create_tables()
        self._seed_data()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        with self._get_connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS users 
                (username TEXT PRIMARY KEY, email TEXT, password TEXT, role TEXT, identifier TEXT)""")
            conn.execute("""CREATE TABLE IF NOT EXISTS books 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, isbn TEXT, title TEXT, author TEXT, status TEXT DEFAULT 'Available')""")

    def _seed_data(self):
        books_to_add = [
            ("978-0132350884", "Clean Code", "Robert C. Martin"), ("978-0201616224", "The Pragmatic Programmer", "Andrew Hunt"),
            ("978-1593279288", "Python Crash Course", "Eric Matthes"), ("978-0134685991", "Effective Java", "Joshua Bloch"),
            ("978-0596007126", "Head First Design Patterns", "Eric Freeman"), ("978-0131103627", "The C Programming Language", "Kernighan"),
            ("978-0262033848", "Introduction to Algorithms", "CLRS"), ("978-1449355739", "Learning Python", "Mark Lutz"),
            ("978-0134494166", "Clean Architecture", "Robert C. Martin"), ("978-1118008188", "HTML and CSS", "Jon Duckett"),
            ("978-1118531648", "JavaScript and JQuery", "Jon Duckett"), ("978-1491901427", "Fluent Python", "Luciano Ramalho"),
            ("978-0321125217", "Domain-Driven Design", "Eric Evans"), ("978-0596517747", "JS: The Good Parts", "Douglas Crockford"),
            ("978-0135957059", "The Clean Coder", "Robert C. Martin"), ("978-1491950296", "Building Microservices", "Sam Newman"),
            ("978-1449340377", "Python for Data Analysis", "Wes McKinney"), ("978-0321573513", "Algorithms", "Robert Sedgewick"),
            ("978-0132126953", "Compilers", "Aho & Ullman"), ("978-1449331818", "Learning PHP & MySQL", "Robin Nixon"),
            ("978-1593276034", "Automate Boring Stuff", "Al Sweigart"), ("978-1491903995", "Deep Learning", "Ian Goodfellow"),
            ("978-0596805524", "TDD by Example", "Kent Beck"), ("978-1449303587", "Node.js in Action", "Cantelon"),
            ("978-1449369415", "Docker: Up & Running", "Matthias"), ("978-0134093413", "Operating Systems", "Stallings"),
            ("978-0321751041", "Art of Programming", "Donald Knuth"), ("978-1593275990", "Linux Command Line", "Shotts"),
            ("978-1119546122", "Network Security Bible", "Cole"), ("978-0134190563", "Android Programming", "Phillips"),
            ("978-1491910399", "React Native", "Eisenman"), ("978-1491918890", "Learning React", "Alex Banks"),
            ("978-1449319243", "NLP with Python", "Steven Bird"), ("978-0596520687", "SQL Cookbook", "Molinaro"),
            ("978-0132350800", "OO Analysis & Design", "Grady Booch"), ("978-1593278908", "Cracking Codes", "Al Sweigart"),
            ("978-1118907443", "Professional C++", "Marc Gregoire"), ("978-1492041139", "Cloud Native Patterns", "Cornelia Davis"),
            ("978-0136083238", "Computer Networking", "Kurose"), ("978-1491952245", "Hands-On ML", "Geron"),
            ("978-1491962299", "Designing Data Apps", "Kleppmann"), ("978-0134177304", "Effective C++", "Scott Meyers"),
            ("978-1449367671", "Database Systems", "Connolly"), ("978-1449370824", "High Perf Browsing", "Grigorik"),
            ("978-0134757599", "Refactoring", "Martin Fowler"), ("978-1492037811", "Java Performance", "Scott Oaks"),
            ("978-1593278892", "The Rust Programming", "Klabnik"), ("978-1492056300", "Kubernetes Up", "Burns"),
            ("978-0134177298", "C++ Primer", "Lippman"), ("978-0131103627", "The C Language", "Ritchie")
        ]
        with self._get_connection() as conn:
            if conn.execute("SELECT COUNT(*) FROM books").fetchone()[0] == 0:
                conn.executemany("INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)", books_to_add)

    def create_user(self, u, e, p, r, i):
        try:
            hp = hashlib.sha256(p.encode()).hexdigest()
            with self._get_connection() as conn:
                conn.execute("INSERT INTO users VALUES (?,?,?,?,?)", (u, e, hp, r, i))
            return True
        except: return False

    def verify_user(self, u, p):
        hp = hashlib.sha256(p.encode()).hexdigest()
        with self._get_connection() as conn:
            return conn.execute("SELECT username, role, identifier FROM users WHERE username=? AND password=?", (u, hp)).fetchone()

    def add_book(self, i, t, a):
        with self._get_connection() as conn:
            conn.execute("INSERT INTO books (isbn, title, author) VALUES (?,?,?)", (i, t, a))

    def fetch_books(self):
        with self._get_connection() as conn:
            return conn.execute("SELECT * FROM books").fetchall()

    def update_book_status(self, bid, stat):
        with self._get_connection() as conn:
            conn.execute("UPDATE books SET status=? WHERE id=?", (stat, bid))