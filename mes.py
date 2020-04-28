import interpreter
import scheduler
import database


class MES:
    def __init__(self):
        # self.mb_interp = interpreter.ModbusInterpreter()
        self.opc_ua_interp = interpreter.OPC_UA_Interpreter()
        self.xml_interp = interpreter.XMLInterpreter()
        self.basic_scheduler = scheduler.BasicScheduler(
            self.opc_ua_interp.transmitter)
        self.db = database.Database()

    def run(self):
        while 1:
            try:
                orders = self.xml_interp.recv()
                if orders is not None:
                    for order in orders:
                        self.basic_scheduler.add(order)
                        self.db.register_order(order)
                        self.basic_scheduler.schedule()

            except KeyboardInterrupt:
                self.opc_ua_interp.transmitter.disconnect()
                self.xml_interp.shutdown()
                self.db.conn.close()
                print('Goodbye!')
            except Exception as e:
                print(f'run: {e}')
