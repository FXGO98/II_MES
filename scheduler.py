
from graph import Graph
from transformations import Transformations
import settings as st
import time
from datetime import datetime


class BasicScheduler():

    def __init__(self, tr, factory, db):
        self.active_tf_order = None
        self.backlog = []
        self.transmitter = tr
        self.trf = Transformations()
        self.g = Graph(factory)
        self.db = db
        self.waiting_for_warehouse_piece = False
        self.waiting_piece_type = 0

    def add(self, order):

        # assume order is a transformation_order
        full_order = self.trf.get_best_layout(
            order.from_, order.to)

        full_order['type'] = 'tf'
        full_order['from'] = order.from_
        full_order['to'] = order.to
        full_order['qty'] = int(order.qty)
        full_order['id'] = int(order.ID)
        full_order ['piece'] = 0

        full_order['listen'] = [x[0] for x in full_order['layout']]
        full_order['mach_working'] = [False for x in full_order['layout']]

        if order.deadline is None:
            full_order['deadline'] = datetime.fromtimestamp(time.time() + st.M)
        else:
            full_order['deadline'] = order.deadline

        print(full_order)

        full_order['directions'] = [self.g.directions_from_partial_layout(
            lyt) for lyt in full_order['layout']]

        print(full_order['directions'])

        # rough, rough estimate
        estimated_delta = 0
        for path_times in full_order['mach_times']:
            estimated_delta += max(path_times) * \
                (len(path_times) + full_order['qty'] - 1)

        estimated_delta /= full_order['num_paths']

        full_order['estimated'] = datetime.fromtimestamp(
            time.time() + estimated_delta)

        if self.active_tf_order is None:
            self.active_tf_order = full_order
            self.change_layout(full_order)
        else:
            self.backlog.append(full_order)

    def schedule(self):
        # self.orders = sorted(self.orders, key=lambda x: x['deadline'])
        # print(f'orders: {self.orders}')

        def _signal_warehouse_out():
            print(f'Signaling for {self.waiting_piece_type}')
            self.transmitter.get_node(
                f"{st.ROOT}.GVL.ST1_tp"
            ).set_value(st.as_piece(self.waiting_piece_type))
            peca = 'P'+str(self.waiting_piece_type)

            self.db.remove_piece_warehouse(peca)

        def _check_warehouse_available():
            idx = self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.idx").get_value()

            if idx == -1:
                print('Available!')

                # Incrementa o nº de peças na database quando a peca entra no armazem
                check_index = self.transmitter.get_node(f"{st.ROOT}.PLC_PRG.TAP_2.index_piece").get_value()
                if check_index>-1:
                    while(check_index>-1):
                        piece_type2 = self.transmitter.get_node(f"{st.ROOT}.PLC_PRG.TAP_2.Pieces_ID[{check_index}][2]").get_value()
                        piece_type3 = 'P'+str(piece_type2)
                        self.db.add_piece_warehouse(piece_type3)
                        for i in range(3):
                            self.transmitter.get_node(f"{st.ROOT}.PLC_PRG.TAP_2.Pieces_ID[{check_index}][{i}]").set_value(st.as_int(0))
                        check_index -=1
                        self.transmitter.get_node(f"{st.ROOT}.PLC_PRG.TAP_2.index_piece").set_value(st.as_int(check_index))


                return True
            print('Unavailable!')
            return False

        def _check_piece_here():
            return self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.SENS").get_value()

        def send_order(order, num_path):
            for i, dir_ in enumerate(order['directions'][num_path]):
                self.transmitter.get_node(
                    f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.dirs[{i}]"
                ).set_value(st.as_int(dir_))

            for i, elem in enumerate(order['sequences'][num_path]):
                typep = int(elem[1])
                print("TYPEP : " +str(typep))
                self.transmitter.get_node(
                    f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.piece_types[{i}]"
                ).set_value(st.as_int(typep))

            self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.idx"
            ).set_value(st.as_int(1))

            self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.piece_idx"
            ).set_value(st.as_int(0))

            self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.order_id"
            ).set_value(st.as_int(order['id']))

            self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.piece_id"
            ).set_value(st.as_int(order['piece']))

            """ self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.piece_types[1]"
            ).set_value(st.as_int(1))

            self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.piece_types[2]"
            ).set_value(st.as_int(2))

            self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.piece_types[3]"
            ).set_value(st.as_int(3))

            self.transmitter.get_node(
                f"{st.ROOT}.PLC_PRG.TAP_1.PIECE_T.piece_types[4]"
            ).set_value(st.as_int(4))
 """
        if not self.waiting_for_warehouse_piece:
            if _check_warehouse_available():
                # scan for machines that are free
                def _send_order_when_ready(order):
                    for num, listen in enumerate(order['listen'][::-1]):
                        n_path = order['num_paths'] - 1 - num

                        i = st.machs[listen]
                        val = self.transmitter.get_node(
                            f"{st.ROOT}.PLC_PRG.TAP_{i}.MAC_1.TIMES_MACHINED"
                        ).get_value()

                        print(f'n_path: {n_path}, val: {val}')

                        # machine resting
                        if val == 1:
                            # check if machine was previously
                            # caught machining
                            if not order['mach_working'][n_path]:
                                print('sending order!')
                                order['mach_working'][n_path] = True
                                send_order(order, n_path)
                                return True

                        # machine machining
                        elif val == 0:
                            # check if machine was previously
                            # caught resting
                            if order['mach_working'][n_path]:
                                order['mach_working'][n_path] = False

                    return False

                if self.active_tf_order is not None:
                    order = self.active_tf_order 

                    print(order['qty'])
                    if _send_order_when_ready(order):
                        self.waiting_for_warehouse_piece = True
                        self.waiting_piece_type = int(order['from'][1])
                        order['qty'] -= 1
                        order['piece'] += 1
                        _signal_warehouse_out()

                        if order['qty'] == 0:
                            self.active_tf_order = None
                        return

                # process other orders?

        if self.waiting_for_warehouse_piece:
            piece_here = _check_piece_here()
            print(f'Checking for piece... {piece_here}')

            if piece_here:
                self.waiting_for_warehouse_piece = False
                self.waiting_piece_type = 0
                # the magic bullet?
                _signal_warehouse_out()

                self.schedule()

    def change_layout(self, order):
        for num_path, partial_lyt in enumerate(order['layout']):
            mach_info = order['mach_info'][num_path]
            mach_times = order['mach_times'][num_path]

            for i, pos in enumerate(partial_lyt):
                idx = st.machs[pos]
                tool = int(mach_info[i][1])
                time = mach_times[i]

                print(f'idx: {idx}, tool: {tool}, time: {time}')

                self.transmitter.get_node(
                    f"{st.ROOT}.PLC_PRG.TAP_{idx}.MAC_1.TOOL"
                ).set_value(st.as_int(tool))

                self.transmitter.get_node(
                    f"{st.ROOT}.PLC_PRG.TAP_{idx}.MAC_1.TOOL_TIME"
                ).set_value(st.as_seconds(time))
