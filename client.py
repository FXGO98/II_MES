from pymodbus.client.sync import ModbusTcpClient
from factory import Factory
import subprocess
from shlex import split as shsplit
import os


class Client:

    MAX_TRIES = 20

    def __init__(self, sfs_path, csv_file):
        os.chdir(sfs_path)
        self.ud = Factory(csv_file)
        self.sfs = subprocess.Popen(shsplit("java -jar sfs.jar"))
        os.chdir("..")

        tries = 0
        success = False
        while tries < self.MAX_TRIES:
            try:
                xdt = subprocess.run(
                    shsplit(
                        'xdotool search --onlyvisible --name "{}"'.format(
                            "Shop Floor Simulator"
                        )
                    ),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                if xdt.stdout is None:
                    tries += 1
                else:
                    win = int(xdt.stdout)
                    # print(win)
                    xdt = subprocess.run(
                        shsplit("xdotool windowmove {} 1500 300".format(win)),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    success = True
                    break

            except Exception:
                tries += 1
                # print(e)

        if not success:
            print("Could not reposition SFS window!")
        else:
            print("SFS window repositioned!")

        self.mb_client = ModbusTcpClient("127.0.0.1", 5502)

        if self.mb_client.connect():
            print("Connected to server!")
        else:
            print("Could not connect to server!")

    def shutdown(self):
        self.mb_client.close()
        print("Client shutting down!")

        self.sfs.terminate()
        print("SFS shutting down!")

    def read_discrete_inputs(self, start_address, debug=False):
        res = self.mb_client.read_discrete_inputs(start_address)
        if debug:
            print(
                'Read discrete input: "{}" at address {}!'.format(
                    res.bits[0], start_address
                )
            )
        return res.bits[0]
