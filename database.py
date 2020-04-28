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

    def register_order(self, order):
        print(order)
        # order.ID
        # order.from_
        # order.to
        # order.qty
        # order.deadline
        self.conn.execute(f'insert into orders (orderId) values ({order.ID});')
        to = 'insert into transformOrders (transformOrderId, fromPiece,' + \
            'toPiece, qty, deadline, currStatus) values ' + \
            f'({order.ID}, "{order.from_}", "{order.to}", ' + \
            f'{order.qty}, "{order.deadline}", "working on it");'

        # print(to)
        self.conn.execute(to)
        self.conn.commit()
