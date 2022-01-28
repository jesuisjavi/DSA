from Utils.Package import Package
import datetime

"""
Truck class.

Represents a truck and delivers up to 16 packages at a time.
"""


class Truck:

    def __init__(self, truck_id: int):
        self.cargo = []
        self.truck_id = truck_id
        self.truck_time = datetime.time(8, 0)
        self.truck_address = "HUB"

    def load_package(self, package: Package):
        self.cargo.append(package)

    def reset_truck(self):
        self.cargo = []
