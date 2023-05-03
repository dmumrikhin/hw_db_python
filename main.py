import psycopg2

def create_tables(conn):

    with conn.cursor() as cur:
        # удаление таблиц
        cur.execute("""
        DROP TABLE IF EXISTS phones;
        DROP TABLE IF EXISTS customers;
        """)

        # создание таблиц
        cur.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            customer_id SERIAL PRIMARY KEY,
	        first_name VARCHAR(80) NOT NULL,
	        second_name VARCHAR(80) NOT NULL,
	        e_mail VARCHAR(80) NOT NULL UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            phone_id SERIAL PRIMARY KEY,
	        phone_number VARCHAR(80),
	        customer_id INTEGER NOT NULL REFERENCES customers(customer_id)
        );
        """)
        conn.commit()  # фиксируем в БД

        cur.execute("""
        INSERT INTO customers(customer_id, first_name, second_name, e_mail) VALUES
            (1, 'Ivanov', 'Ivan', 'ivanov@mail.org'),
            (2, 'Petrov', 'Petr', 'petrov@mail.org'),
            (3, 'Sidorov', 'Sidor', 'sidorov@mail.org');
        INSERT INTO phones(phone_number, customer_id) VALUES
            ('7-495-111-11-11', 1),
            ('7-495-111-11-12', 1),
            ('7-495-111-11-13', 1),
            ('7-495-111-11-21', 2),
            ('7-495-111-11-22', 2);
        """)
        conn.commit()  # фиксируем в БД

def add_customer(conn):
    first_name = input('Введите фамилию: ')
    second_name = input('Введите имя: ')
    e_mail = input('Введите e-mail: ')
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO customers(customer_id, first_name, second_name, e_mail) VALUES
            (%s, %s, %s, %s);
        """, (4, first_name, second_name, e_mail))
        conn.commit()  # фиксируем в БД
    print('Новый клиент добавлен')

def add_phone(conn):
    customer_id = input('Введите id клиента: ')
    phone_number = input('Введите номер телефона: ')
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phones(phone_number, customer_id) VALUES
            (%s, %s);
        """, (phone_number, customer_id))
        conn.commit()  # фиксируем в БД
    print('Новый телефон добавлен')

def change_data(conn):
    customer_id = input('Введите id клиента: ')
    print('Введите номер пункта для изменения\n', '1. Фамилии\n', 
          '2. Имени\n', '3. Почты')
    column_nr = input()
    new_data = input('Введите новое значение: ')
    if column_nr == '1':
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE customers SET first_name=%s WHERE customer_id=%s;
            """, (new_data, customer_id))
            conn.commit()  # фиксируем в БД
            print('Данные обновлены')
    elif column_nr == '2':
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE customers SET second_name=%s WHERE customer_id=%s;
            """, (new_data, customer_id))
            conn.commit()  # фиксируем в БД
            print('Данные обновлены')
    elif column_nr == '3':
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE customers SET e_mail=%s WHERE customer_id=%s;
            """, (new_data, customer_id))
            conn.commit()  # фиксируем в БД
            print('Данные обновлены')
    else:
        print('Ошибка, попробуйте еще раз')
        
def delete_phone(conn):
    customer_id = input('Введите id клиента: ')
    with conn.cursor() as cur:
        cur.execute("""
        SELECT phone_id, phone_number FROM phones WHERE customer_id=%s;
        """, (customer_id))
        conn.commit()  # фиксируем в БД
        for id, phone in cur.fetchall():
            print(f"id:{id} телефон: {phone}")
    phone_id = input('Введите id телефона: ')
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones WHERE phone_id=%s;
        """, (phone_id))
        conn.commit()  # фиксируем в БД    
        print('Телефон удален')

def delete_customer(conn):
    customer_id = input('Введите id клиента: ')
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones WHERE customer_id=%s;
        """, (customer_id))
        conn.commit()  # фиксируем в БД    
    
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM customers WHERE customer_id=%s;
        """, (customer_id))
        conn.commit()  # фиксируем в БД    
        print('Клиент удален')

def get_customers_info(conn):
    customer_info = input('Введите фамилию, имя, почту или телефон клиента: ')
    with conn.cursor() as cur:
        cur.execute("""
        SELECT first_name, second_name, e_mail FROM customers c
        LEFT JOIN phones p ON c.customer_id = p.customer_id
        WHERE first_name=%s
        OR second_name=%s
        OR e_mail=%s
        OR phone_number=%s;
        """, (customer_info, customer_info, customer_info, customer_info))
        conn.commit()  # фиксируем в БД
        for f_name, s_name, e_mail in cur.fetchall():
            print(f"{f_name} {s_name}, {e_mail}")

def run_menu():
    print(f'УПРАВЛЕНИЕ КЛИЕНТАМИ\n 1.Создать структуру БД\n 2.Добавить клиента\n'
          f' 3.Добавить номер телефона\n 4.Изменить данные о клиенте\n'
          f' 5.Удалить телефон клиента\n 6.Удалить клиента\n 7.Получить информацию '
          f'о клиенте')
    menu = input('Введите пункт меню: ')
    if menu == '1':
        create_tables(conn)
    elif menu == '2':
        add_customer(conn)
    elif menu == '3':
        add_phone(conn)
    elif menu == '4':
        change_data(conn)
    elif menu == '5':
        delete_phone(conn)
    elif menu == '6':
        delete_customer(conn)
    elif menu == '7':
        get_customers_info(conn)
    else:
        print('Ошибка, повторите ввод')
    
with psycopg2.connect(database="postgres", user="postgres", password="") as conn:
    run_menu()
conn.close()