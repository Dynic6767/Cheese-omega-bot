import sqlite3

def create_database():
    conn = sqlite3.connect('cheese_catalog.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tastes (
            taste_id INTEGER PRIMARY KEY AUTOINCREMENT,
            taste_name TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cheeses (
            cheese_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cheese_name TEXT NOT NULL,
            taste_id INTEGER,
            price REAL NOT NULL,
            FOREIGN KEY (taste_id) REFERENCES tastes(taste_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cheese_pairings (
            pairing_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cheese_id INTEGER,
            paired_with TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (cheese_id) REFERENCES cheeses(cheese_id)
        )
    ''')

    conn.commit()
    conn.close()

def populate_data():
    conn = sqlite3.connect('cheese_catalog.db')
    cursor = conn.cursor()

    tastes = [
        ('Вкусный',),
        ('Средний',),
        ('Невкусный',)
    ]
    cursor.executemany('INSERT OR IGNORE INTO tastes (taste_name) VALUES (?)', tastes)

    cheeses = [
        ('Маасдам', 3, 850),
        ('Пармезан', 3, 1200),
        ('Бри', 1, 950),
        ('Горгонзола', 1, 1100),
        ('Гауда', 2, 750),
        ('Чеддер', 2, 800),
        ('Эмменталь', 2, 900),
        ('Рокфор', 3, 1300),
        ('Камамбер', 1, 880),
        ('Грюйер', 2, 1050)
    ]
    cursor.executemany(
        'INSERT INTO cheeses (cheese_name, taste_id, price) VALUES (?, ?, ?)',
        cheeses
    )

    pairings = [
        (1, 'Вино белое', 'Отлично сочетается с лёгкими белыми винами'),
        (1, 'Груша', 'Сладкая груша подчёркивает вкус Маасдама'),
        (2, 'Красное вино', 'Пармезан идеален с красными винами'),
        (2, 'Мёд', 'Сочетание пармезана с мёдом — классика'),
        (3, 'Багет', 'Бри прекрасно подходит к свежему багета'),
        (3, 'Клубника', 'Необычное, но вкусное сочетание'),
        (4, 'Грецкие орехи', 'Орехи дополняют пикантный вкус горгонзолы'),
        (4, 'Груши', 'Сладкие груши уравновешивают остроту'),
        (5, 'Яблоки', 'Свежие яблоки хорошо сочетаются с Гаудой'),
        (6, 'Пиво', 'Чеддер отлично подходит к тёмному пиву'),
        (7, 'Вино розовое', 'Лёгкое сочетание для Эмменталя'),
        (8, 'Инжир', 'Сладкий инжир и солёный Рокфор'),
        (9, 'Багет с маслом', 'Классическое сочетание для Камамбера'),
        (9, 'Вино красное', 'Подходит к выдержанному Камамберу'),
        (10, 'Груши', 'Грюйер и груши — гармоничное сочетание')
        #Да я это загуглил я не ботаник по кто с кем сочитается
    ]

    cursor.executemany(
        'INSERT INTO cheese_pairings (cheese_id, paired_with, description) VALUES (?, ?, ?)',
        pairings
    )

    conn.commit()
    conn.close()

def cheese_info():
    conn = sqlite3.connect('cheese_catalog.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.cheese_name, t.taste_name, c.price
        FROM cheeses c
        JOIN tastes t ON c.taste_id = t.taste_id
        ORDER BY c.cheese_name
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

def get_cheapest_by_taste():
    conn = sqlite3.connect('cheese_catalog.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.taste_name, c.cheese_name, MIN(c.price)
        FROM cheeses c
        JOIN tastes t ON c.taste_id = t.taste_id
        GROUP BY t.taste_name
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

def get_most_expensive_by_taste():
    conn = sqlite3.connect('cheese_catalog.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.taste_name, c.cheese_name, MAX(c.price)
        FROM cheeses c
        JOIN tastes t ON c.taste_id = t.taste_id
        GROUP BY t.taste_name
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

def get_cheese_pairings(cheese_name=None):
    conn = sqlite3.connect('cheese_catalog.db')
    cursor = conn.cursor()

    if cheese_name:
        cursor.execute('''
            SELECT c.cheese_name, cp.paired_with, cp.description
            FROM cheese_pairings cp
            JOIN cheeses c ON cp.cheese_id = c.cheese_id
            WHERE c.cheese_name = ?
        ''', (cheese_name,))
    else:
        cursor.execute('''
            SELECT c.cheese_name, cp.paired_with, cp.description
            FROM cheese_pairings cp
            JOIN cheeses c ON cp.cheese_id = c.cheese_id
            ORDER BY c.cheese_name
        ''')

    result = cursor.fetchall()
    conn.close()
    return result

if __name__ == "__main__":
    create_database()  
    populate_data()    