import xml.etree.ElementTree as ET
from datetime import datetime
import time


class Order:
    def __init__(self):
        pass

    def __str__(self):
        return "(Order ID: None) An abstract Order"


class TransformOrder(Order):
    def __init__(self, ID, from_, to, qty, max_delay):
        self.ID = ID
        self.from_ = from_
        self.to = to
        self.qty = qty
        self.deadline = datetime.fromtimestamp(time.time() + max_delay)

    def __str__(self):
        return "(Order ID: {}) Transform {} {} into {} {}".format(
            self.ID, self.qty, self.from_, self.qty, self.to,
        ) + "(before {:02d}:{:02d}:{:02d})".format(
            self.deadline.hour, self.deadline.minute, self.deadline.second,
        )


class UnloadOrder(Order):
    def __init__(self, ID, type, dest, qty):
        self.ID = ID
        self.type = type
        self.dest = dest
        self.qty = qty

    def __str__(self):
        return "(Order ID: {}) Unload {} {} onto {}".format(
            self.ID, self.qty, self.type, self.dest
        )


class RequestStoresOrder(Order):
    def __str__(self):
        return "(Order ID: None) Request Stores"


def from_XML(request):
    def _from_XML(el):
        if el.tag == "Order":

            ID = int(el.attrib["Number"])

            els = [c for c in el]
            assert len(els) == 1

            el = els[0]
            attr = el.attrib
            if el.tag == "Transform":
                return TransformOrder(
                    ID,
                    from_=attr["From"],
                    to=attr["To"],
                    qty=attr["Quantity"],
                    max_delay=int(attr["MaxDelay"]),
                )

            elif el.tag == "Unload":
                return UnloadOrder(
                    ID,
                    qty=attr["Quantity"],
                    type=attr["Type"],
                    dest=attr["Destination"],
                )

        elif el.tag == "Request_Stores":
            return RequestStoresOrder()

        else:
            raise NotImplementedError

    root = ET.fromstring(request)

    try:
        if root.tag == "ORDERS":
            return [_from_XML(c) for c in root]

    except Exception as e:
        print(f'from_XML: {e}')
        return None
