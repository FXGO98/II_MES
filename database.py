import sqlite3
import os
from datetime import datetime


class Database:

    def __init__(self):

        file_ = ''
        files = [f for f in os.listdir() if f.endswith('.db')]
        if len(files) == 1:
            file_ = files[0]
            print(f'Database file found! Loading: {file_}')
        elif len(files) == 0:
            file_ = f'{datetime.now().strftime("%d_%B_%Y_%Ih%M%p")}.db'
            print(f'Database file not found! Creating a new one: {file_}')
        elif len(files) > 1:
            while(1):
                print(f'Many database files found! Choose which to use:')
                for num, f in enumerate(files):
                    print(f'({num}) {f}')
                try:
                    pick = int(input())
                    if pick < 0:
                        raise Exception

                    file_ = files[pick]
                    print(f'Database file chosen! Loading: {file_}')
                    break
                except Exception:
                    for i in range(100):
                        print()
                    print('Choose a valid number')

        self.conn = sqlite3.connect(file_)
        self.conn.execute("PRAGMA foreign_keys = on")
        self.cur = self.conn.cursor()
        self.cur.executescript(open('create_tables.sql', 'r').read())
        self.conn.commit()

        print('Database initialized successfully!')

    def register_order(self, order_):
        o = order_.to_sql()
        # print(to)
        self.conn.execute(o)
        self.conn.commit()

    # Alterei esta função, ela agora já atualiza o armazem
    def add_piece_warehouse(self, piece_type):
        self.cur.execute("SELECT * FROM warehouse WHERE piece = :piece", {'piece': piece_type})
        curr_qty1 = self.cur.fetchall()
        
        if len(curr_qty1) < 1:
            return False

        quantity3 = curr_qty1[0]

        quantity2 = quantity3[1]+1

        o = f"UPDATE warehouse SET quantity = {quantity2} WHERE piece = '{piece_type}'"
        self.cur.execute(o)
        self.conn.commit()
        return True

    def remove_piece_warehouse(self, piece_type):

        self.cur.execute("SELECT * FROM warehouse WHERE piece = :piece", {'piece': piece_type})
        curr_qty = self.cur.fetchall()


        if len(curr_qty) < 1:
            return False

        quantity1 = curr_qty[0]

        quantity = quantity1[1]-1

        
        o = f"UPDATE warehouse SET quantity = {quantity} WHERE piece = '{piece_type}'"
        self.cur.execute(o)
        self.conn.commit()
        return True
