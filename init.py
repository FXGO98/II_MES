
import settings as st


class Layout():

    def __init__(self, tr):
        self.transmitter = tr
        self.setup_tools()
        print("O Layout foi inicializado ****")

    def setup_tools(self):
        conveyors = [[4, 5, 6], [16, 17, 18], [28, 29, 30]]

        for i in range(3):
            for j in range(3):
                self.transmitter.get_node(
                    f"{st.ROOT}.PLC_PRG.TAP_{conveyors[i][j]}.MAC_1.TOOL"
                ).set_value(st.as_int(j+1))
