import settings as st
import networkx as nx
import itertools as it


class Transformations():

    def __init__(self):
        self.g = nx.DiGraph()
        self.populate()

        # self.valid_pairs = self._compatible_pairs()

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
        self._gen_nodes()
        self._gen_edges()

    def _compute_transformation_path(self, source, target):
        # TODO: get all paths
        return nx.all_simple_paths(self.g,
                                   source=source,
                                   target=target)

    def get_list_machines(self, source, target):
        list_machines_all = []
        for path in self._compute_transformation_path(source, target):
            list_machines = []
            for i in range(len(path)-1):
                src = path[i]
                dest = path[i+1]
                list_machines.append((
                    self.g.get_edge_data(src, dest)['machine'],
                    self.g.get_edge_data(src, dest)['weight']
                ))

            list_machines_all.append(list_machines)

        return list_machines_all

    def _gen_nodes(self):
        for i in range(1, 9+1):
            self.g.add_node(f'P{i}')

    def _add_transformation(self, from_, to, time, machine):
        self.g.add_edge(from_, to, weight=time, machine=machine)

    def _gen_edges(self):
        self._add_transformation('P1', 'P2', 15, 'A1')
        self._add_transformation('P1', 'P3', 20, 'B1')
        self._add_transformation('P1', 'P4', 10, 'C1')

        self._add_transformation('P2', 'P3', 15, 'A1')
        self._add_transformation('P3', 'P4', 15, 'B1')
        self._add_transformation('P4', 'P5', 30, 'C1')

        self._add_transformation('P2', 'P6', 15, 'A2')
        self._add_transformation('P3', 'P7', 20, 'B2')
        self._add_transformation('P4', 'P8', 10, 'C2')

        self._add_transformation('P6', 'P9', 15, 'A3')
        self._add_transformation('P7', 'P9', 20, 'B3')
        self._add_transformation('P8', 'P9', 10, 'C3')

    def _get_all_possible_tfs(self, source, target):
        return [x for x in nx.all_simple_paths(self.g, source, target)]

    def _get_tf_machine_info(self, path):
        machine_info = []
        for i in range(len(path)-1):
            src = path[i]
            tgt = path[i+1]
            dt = self.g.get_edge_data(src, tgt)
            machine_info.append((dt['machine'], dt['weight']))

        return machine_info

    def _machine_info_total_time(self, mi):
        return sum([x[1] for x in mi])

    def _get_all_possible_tfs_sorted(self, source, target):
        times = []
        machine_infos = []
        paths = self._get_all_possible_tfs(source, target)
        for path in paths:
            machine_infos.append(self._get_tf_machine_info(path))
            times.append(self._machine_info_total_time(
                machine_infos[-1]))

        return sorted(
            [x for x in zip(paths, machine_infos, times)],
            key=lambda x: x[-1])

    def pair_is_compatible(self, a, b):
        if (a, b) in self.valid_pairs:
            return True
        if (b, a) in self.valid_pairs:
            return True
        return False

    def _compatible_pairs(self):
        # (P1, P5)
        all_pairs = list(it.combinations(list(self.g.nodes()), 2))
        # print(all_pairs)
        # print(len(all_pairs))

        # (P1, P3, ..., P5)
        all_paths = []
        for a, b in all_pairs:
            for path in nx.all_simple_paths(self.g, a, b):
                all_paths.append(path)

        # print(all_paths)
        # print(len(all_pairs))

        # ((P1, P2), (P1, P3))
        all_path_combos = list(it.combinations(all_paths, 2))
        # print(all_path_combos)
        # print(len(all_path_combos))

        valid_combos = []
        for path1, path2 in all_path_combos:
            mi_1 = self._get_tf_machine_info(path1)
            mi_2 = self._get_tf_machine_info(path2)

            def check_compatible(mi_1, mi_2):
                unique_machines1 = list(set([x[0] for x in mi_1]))
                unique_machines2 = list(set([x[0] for x in mi_2]))

                for machine_type in ['A', 'B', 'C']:
                    sum_1 = sum(
                        [1 for x in unique_machines1 if x[0] == machine_type])
                    sum_2 = sum(
                        [1 for x in unique_machines2 if x[0] == machine_type])

                    if sum_1 + sum_2 > 3:
                        # print((unique_machines1, unique_machines2))
                        return False

                return True

            if check_compatible(mi_1, mi_2):
                valid_combos.append((path1, path2))
            # else:
                # print((path1, path2))

        # print(len(valid_combos))
        return valid_combos

    def _all_path_combos(self, paths, num=0):
        # print(len(paths))

        # ((P1, P2), (P1, P3))
        path_combos = []
        if num == 0:
            iterable = range(1, len(paths) + 1)
        else:
            iterable = [num]

        for i in iterable:
            for combo in it.combinations_with_replacement(paths, i):
                machine_cnt = {'A': 0, 'B': 0, 'C': 0}
                for path in combo:
                    mi = self._get_tf_machine_info(path)
                    machines = [x[0] for x in mi]
                    # unique_machines = list(set(machines))
                    for machine_type in ['A', 'B', 'C']:
                        machine_cnt[machine_type] += sum(
                            [1 for x in machines  # unique_machines
                             if x[0] == machine_type])

                is_valid = True
                for key in machine_cnt.keys():
                    if machine_cnt[key] > 3:
                        is_valid = False

                if is_valid:
                    time = 0
                    for path in combo:
                        time += sum([x[1]
                                     for x in self._get_tf_machine_info(path)])
                    path_combos.append((combo, time))

        # print(all_path_combos)
        # print(len(path_combos))

        return path_combos

    def get_best_path_combo(self, source, target, num):
        tfs = self._get_all_possible_tfs(source, target)
        combos = sorted(self._all_path_combos(tfs, num), key=lambda x: x[-1])
        if len(combos) == 0:
            if num == 1:
                return None
            return self.get_best_path_combo(source, target, num-1)

        return combos[0]

    def get_best_layout(self, source, target, num=6):
        sequences = self.get_best_path_combo(source, target, num)[0]
        print(sequences)

        possible_layout_combos = []
        for sequence in sequences:
            path = self._get_tf_machine_info(sequence)
            machine_list = [x[0] for x in path]

            def _simple_layout(path):
                mach_pattern = [ord(x[0]) - ord('A') for x in path]
                # print(path)
                # print(mach_pattern)

                patt = [3*mach_pattern[0]]
                prev = mach_pattern[0]
                for i in range(1, len(mach_pattern)):
                    curr = mach_pattern[i]
                    if curr == prev:
                        patt.append(1 + patt[-1])
                    else:
                        diff = curr - prev
                        patt.append(3*diff + patt[-1])
                    prev = curr

                # print(patt)
                return patt

            def _get_layout_at_pos(layout, pos):
                return [x+pos for x in layout]

            def _possible_simple_layout_combos(layout):
                possible_lyts = []
                for pos in [0, 1, 2]:
                    lyt = _get_layout_at_pos(layout, pos)

                    valid = True
                    for cell in lyt:
                        if cell > 8:
                            valid = False
                            break

                    for row in [0, 1, 2]:
                        og_count = sum([1 for x in layout
                                        if (x >= 3*row) and (x < 3*(row+1))])
                        new_count = sum([1 for x in lyt
                                         if (x >= 3*row) and (x < 3*(row+1))])

                        if og_count != new_count:
                            valid = False
                            break

                    if valid:
                        possible_lyts.append(lyt)

                return possible_lyts

            simple_layout = _simple_layout(machine_list)
            possible_layout_combos.append(
                _possible_simple_layout_combos(simple_layout))

        # print(possible_layout_combos)
        # print(len(possible_layout_combos))

        full_layouts = []
        possible_full_layouts = sorted(
            list(it.product(*possible_layout_combos)))
        # print(possible_full_layouts)

        plain_layouts_explored = []
        for layout in possible_full_layouts:
            plain_layout = []
            for partial_layout in layout:
                plain_layout += partial_layout
            # print(plain_layout)

            # removes superfluous combos of the same precise layout
            if sorted(plain_layout) in plain_layouts_explored:
                continue

            plain_layouts_explored.append(sorted(plain_layout))

            if len(plain_layout) == len(list(set(plain_layout))):
                # partial layouts are compatible
                full_layouts.append(layout)

        # print(full_layouts)

        # TODO: sort for best layout
        print(full_layouts)
        full_lyt = full_layouts[0]

        mach_info = [self._get_tf_machine_info(path) for path in sequences]

        full_order = {}
        full_order['layout'] = full_lyt
        full_order['sequences'] = sequences

        times = []
        for info in mach_info:
            times.append([x[1] for x in info])

        machines = []
        for info in mach_info:
            machines.append([x[0] for x in info])

        full_order['mach_info'] = machines
        full_order['mach_times'] = times
        full_order['num_paths'] = len(times)

        return full_order


# machs = None
# valid = None
t = None
lyts = None
sequences = None
mach_info = None
if __name__ == "__main__":
    t = Transformations()
    # valid_pairs = t.valid_pairs

    full_order = t.get_best_layout('P1', 'P7')
    print(full_order)
