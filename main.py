from client import Client
from mes import MES

cl = Client("sfs-1.1.4_plant-2020_1.4", "io.csv")

mes = MES()

orders = []

print("Listening")
while 1:
    try:
        req = mes.xml_interp.recv()
        if req is not None:
            for ord in req:
                # print('outside: got "{}"'.format(ord))
                orders.append(ord)
    except KeyboardInterrupt:
        break

# print(orders)
for ord in orders:
    print(ord)

"""
x = input()

res = cl.mb_client.read_coils(0)
print(res)
print(res.bits)

cl.read_discrete_inputs(0, True)
cl.read_discrete_inputs(1, True)
res = cl.mb_client.read_discrete_inputs(0, 9)
print(res.bits)
"""

cl.shutdown()
