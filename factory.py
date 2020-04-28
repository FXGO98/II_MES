import csv


class Factory:
    def __init__(self, csv_path):
        self.units = []
        self._populate(csv_path)

    def _populate(self, csv_path):
        if len(self.units) != 0:
            raise Exception

        def _create_unit(csv_data):
            id = csv_data[0][0]
            code = csv_data[0][1]
            name = csv_data[0][2]

            try:
                if name == "Warehouse Out":
                    return WarehouseOut(csv_data)
                elif name == "Warehouse In":
                    return WarehouseIn(csv_data)
                elif name == "Rotator":
                    return Rotator(csv_data)
                elif name == "Conveyor":
                    return Conveyor(csv_data)
                elif name == "Machine":
                    return Machine(csv_data)
                elif name == "Pusher":
                    return Pusher(csv_data)
                elif name == "Roller":
                    return Roller(csv_data)
                else:
                    raise NotImplementedError

            except Exception as e:
                print(e)
                raise e

            for line in csv_data:
                assert (id, code, name) == (line[0], line[1], line[2])
                # print(line)

        with open(csv_path, "r") as f:
            rows = csv.reader(f)
            code = 1
            lines = []
            for row in rows:
                if code != int(row[0]):
                    self.units.append(_create_unit(lines))
                    print(self.units[-1])
                    code = int(row[0])
                    lines = []

                lines.append(row)


class Unit:
    def __init__(self, csv_data):
        try:
            self.id, self.code, self.name = csv_data[0][0:3]
            self.io = []
            for line in csv_data:
                type_, name, location = line[3], line[4], line[5]
                # class_type = {"O": Output(), "I": Input(), "R": Register()}
                # self.io.append(class_type[type_].from_params(name, location))
                if type_ == "O":
                    self.io.append(Output(name, location))
                elif type_ == "I":
                    self.io.append(Input(name, location))
                elif type_ == "R":
                    self.io.append(Register(name, location))
                else:
                    raise NotImplementedError

            # for io in self.io:
            #    print(io)

        except Exception as e:
            print(e)
            return None

    def __str__(self):
        s = "{} (id: {}, {}) ".format(self.name, self.id, self.code)
        for io in self.io:
            s += "\n\t" + io.__str__()
        return s


class Rotator(Unit):
    pass


class Conveyor(Unit):
    pass


class Machine(Unit):
    pass


class WarehouseIn(Unit):
    pass


class WarehouseOut(Unit):
    pass


class Pusher(Unit):
    pass


class Roller(Unit):
    pass


class IO:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __str__(self):
        s = type(self).__name__ + " '{}' @{}".format(self.name, self.location)
        return s


class Output(IO):
    pass


class Input(IO):
    pass


class Register(IO):
    pass
