
import settings as st
import networkx as nx

LINE_BASE = 100
MACHINE_BASE = 200

machines = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']


class Graph():

    def __init__(self, factory_):
        self.g = nx.DiGraph()
        self.id_dict = {}
        self.time_dict = {}
        self.f = factory_

        self.populate()

    def _get_unit_id(self, code):
        return int(self.id_dict[code])

    def _get_weight(self, uid1, uid2):
        return (self.time_dict[uid1] + self.time_dict[uid2]) / 2

    def _add_weighted_edge(self, code1, code2, dir, w=-1):
        u1 = self._get_unit_id(code1)
        u2 = self._get_unit_id(code2)
        if w == -1:
            w = self._get_weight(int(u1), int(u2))

        # both directions
        self.g.add_edge(u1, u2, weight=w, direction=dir)
        self.g.add_edge(u2, u1, weight=w,  direction=st.get_opp_dir(dir))

    def _add_weighted_edge_unid(self, code1, code2, dir, w=-1):
        u1 = self._get_unit_id(code1)
        u2 = self._get_unit_id(code2)
        if w == -1:
            w = self._get_weight(int(u1), int(u2))

        # one direction <3
        self.g.add_edge(u1, u2, weight=w, direction=dir)

    def populate(self):
        self._gen_dicts()
        self._gen_nodes()
        self._gen_edges_rows()
        self._gen_edges_columns()
        self.list_ops = self._gen_edges_machines()

    # Assumes a fixed columns 1, 2, 3 layout!
    '''
    def _compute_production_path(self, list_machines):

        def _add_to_path(path, add):
            if len(path):
                e = path.pop()
                assert(e == add[0])
            for node in add:
                path.append(node)

        path = []
        source = self.id_dict['AT1']

        time_to_finish = 0
        # list_machines = [(A1 t1), (B2, t2), ...]
        for machine, time in list_machines:
            # update time
            e = self.g.get_edge_data(*self.list_ops[machine])
            self.g.remove_edge(*self.list_ops[machine])
            self.g.add_edge(
                *self.list_ops[machine],
                weight=time, direction=e['direction'])

            target = self.list_ops[machine][1]
            _add_to_path(path,
                         nx.dijkstra_path(self.g,
                                          source=source,
                                          target=target))
            time_to_finish += nx.dijkstra_path_length(self.g,
                                                      source=source,
                                                      target=target)
            source = target

        target = self.id_dict['WH_IN']
        _add_to_path(path,
                     nx.dijkstra_path(self.g,
                                      source=source,
                                      target=target))
        time_to_finish += nx.dijkstra_path_length(self.g,
                                                  source=source,
                                                  target=target)

        return path, time_to_finish
    '''

    def get_directions(self, list_machines):
        path, time_to_finish = self._compute_production_path(list_machines)
        dirs = []
        for i in range(len(path)-1):
            src = path[i]
            dest = path[i+1]
            dirs.append(
                self.g.get_edge_data(src, dest)['direction'])

        dirs = [x for x in dirs if x is not None]
        return dirs, time_to_finish

    def directions_from_partial_layout(self, partial_lyt):
        def _compute_path_from_partial_layout(partial_lyt):
            def _add_to_path(path, add):
                if len(path):
                    e = path.pop()
                    assert(e == add[0])
                for node in add:
                    path.append(node)

            path = []
            source = self.id_dict['AT1']

            # list_machines = [A1, B2, ...]
            list_machines = [machines[pos] for pos in partial_lyt]

            target = None
            print(partial_lyt)
            if partial_lyt[0] in [0, 3, 6]:
                target = self.id_dict['C2T1']
            elif partial_lyt[0] in [1, 4, 7]:
                target = self.id_dict['C4T1']
            elif partial_lyt[0] in [2, 5, 8]:
                target = self.id_dict['C6T1']

            _add_to_path(path,
                         nx.dijkstra_path(self.g,
                                          source=source,
                                          target=target))
            source = target

            for machine in list_machines:
                target = self.list_ops[machine][1]
                _add_to_path(path,
                             nx.dijkstra_path(self.g,
                                              source=source,
                                              target=target))
                source = target

            target = self.id_dict['WH_IN']
            _add_to_path(path,
                         nx.dijkstra_path(self.g,
                                          source=source,
                                          target=target))

            return path  # , time_to_finish

        path = _compute_path_from_partial_layout(partial_lyt)
        dirs = []
        for i in range(len(path)-1):
            src = path[i]
            dest = path[i+1]
            dirs.append(
                self.g.get_edge_data(src, dest)['direction'])

        dirs = [x for x in dirs if x is not None]
        return dirs

    def _gen_nodes(self):

        self.id_dict['WH_IN'] = 0

        for unit in self.f.units:
            self.g.add_node(int(unit.id), name=unit.code)
            self.id_dict[unit.code] = int(unit.id)

        for line_num in range(1, 3+1):
            code = f'Line {line_num}'
            self.g.add_node(int(LINE_BASE+line_num), name=code)
            self.id_dict[code] = int(100+line_num)

        machine_num = 1
        for j in [1, 3, 5]:
            for i in [3, 4, 5]:
                code = f'M{j}T{i}'
                num = MACHINE_BASE + machine_num
                machine_num += 1

                self.g.add_node(int(num), name=code)
                self.id_dict[code] = int(num)

        # populate time_dict
        # set them all as time_med

    def _gen_dicts(self):
        small_ones = [3, 7, 9, 13, 15, 19, 21, 25, 27, 31, 33, 37, 41, 45]
        big_ones = [8, 10, 11, 12, 14, 20, 22, 23, 24, 26,
                    32, 34, 35, 36, 38, 39, 40, 42, 43, 44, 46, 47]

        for i in range(1, 60):
            self.time_dict[i] = st.time_med

        # set the small ones
        for i in small_ones:
            self.time_dict[i] = st.time_sml

        # machines
        for i in range(200, 210):
            self.time_dict[i] = st.time_sml

        # set the big ones
        for i in big_ones:
            self.time_dict[i] = st.time_big

    def _gen_edges_rows(self):

        d = st.RIGHT
        # top connections
        self._add_weighted_edge('AT1', 'C1T1', dir=d)

        for i in range(1, 6):
            self._add_weighted_edge(f'C{i}T1', f'C{i+1}T1', dir=d)

        self._add_weighted_edge('C6T1', 'C7T1a', dir=d)
        self._add_weighted_edge('C7T1a', 'C7T1b', dir=d)

        # bottom connections
        self._add_weighted_edge('WH_IN', 'AT2', w=0, dir=d)
        self._add_weighted_edge('AT2', 'C1T7', dir=d)

        for i in range(1, 6):
            self._add_weighted_edge(f'C{i}T7', f'C{i+1}T7', dir=d)

        self._add_weighted_edge('C6T7', 'C7T7a', dir=d)
        self._add_weighted_edge('C7T7a', 'C7T7b', dir=d)

    def _gen_edges_columns(self):

        d = st.DOWN

        # columns
        for n, j in enumerate([2, 4, 6]):
            # insert line load nodes between top row and columns
            # TODO: change these arbitrary weights
            self._add_weighted_edge_unid(
                f'C{j}T1', f'Line {n+1}', dir=None, w=2)
            self._add_weighted_edge_unid(
                f'Line {n+1}', f'C{j}T2', dir=d, w=2)

            for i in range(2, 6+1):
                self._add_weighted_edge(
                    f'C{j}T{i}', f'C{j}T{i+1}', dir=d)

        # last column
        self._add_weighted_edge(f'C7T1a', f'C7T2', dir=d)
        for i in range(2, 6):
            self._add_weighted_edge(f'C7T{i}', f'C7T{i+1}', dir=d)
        self._add_weighted_edge(f'C7T6', f'C7T7a', dir=d)

    def _gen_edges_machines(self):
        # machines
        list_ops = {}
        # order is top to bottom, left to right
        name = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']

        num = 0
        for j in [1, 3, 5]:
            for i in range(3, 5+1):
                conveyor = f'C{j+1}T{i}'
                machine_belt = f'C{j}T{i}'
                machine = f'M{j}T{i}'

                self._add_weighted_edge_unid(
                    conveyor, machine, dir=st.LEFT)
                self._add_weighted_edge_unid(
                    machine, machine_belt, w=0, dir=None)
                self._add_weighted_edge_unid(
                    machine_belt, conveyor, dir=st.RIGHT)

                list_ops[name[num]] = (self._get_unit_id(f'C{j+1}T{i}'),
                                       self._get_unit_id(f'M{j}T{i}'))
                num += 1

        # link conveyors to right-side machines
        for j in [2, 4]:
            for i in range(3, 5+1):
                conveyor = f'C{j}T{i}'
                # machine_belt = f'C{j}T{i}'
                machine = f'M{j+1}T{i}'

                # make it so you can't go back to the
                # conveyor, avoid congestion?
                # TODO: see if this restriction
                # is necessary in practice
                self._add_weighted_edge_unid(
                    conveyor, machine, dir=st.RIGHT)

        return list_ops


f = None
g = None

if __name__ == "__main__":
    import factory

    f = factory.Factory('io.csv')
    g = Graph(f)
