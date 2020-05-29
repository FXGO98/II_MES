import interpreter
import scheduler
import database
# import init

from factory import Factory


class MES:
    def __init__(self):
        # self.mb_interp = interpreter.ModbusInterpreter()
        self.db = database.Database()
        self.opc_ua_interp = interpreter.OPC_UA_Interpreter()
        self.xml_interp = interpreter.XMLInterpreter()
        self.factory = Factory('io.csv')
        self.basic_scheduler = scheduler.BasicScheduler(
            self.opc_ua_interp.transmitter, self.factory, self.db)
        # self.initializer = init.Layout(
        #     self.opc_ua_interp.transmitter)
        # self.initializer.setup_tools()
        self.run()

    def run(self):
        self.running = 1
        while self.running:
            try:
                orders = self.xml_interp.recv()
                if orders is not None:
                    for order in orders:
                        print(order)
                        self.db.register_order(order)

                        if order.schedulable:
                            self.basic_scheduler.add(order)

                self.basic_scheduler.schedule()

            except KeyboardInterrupt:

                self.running = False
                self.opc_ua_interp.transmitter.disconnect()
                try:
                    self.xml_interp.shutdown()
                except Exception as e:
                    print(e)

                try:
                    self.db.conn.close()
                except Exception as e:
                    print(e)

                print('Goodbye!')
            # except Exception as e:
            #    print(f'run(): {e}')


if __name__ == "__main__":
    m = MES()
