from Utils.Package import Package

"""
Truck class.

Represents a truck and delivers up to 16 packages at a time.
"""


class Truck:

    def __init__(self, truck_id: int):
        self.cargo = []
        self.truck_id = truck_id

    def load_package(self, package: Package):
        self.cargo.append(package)

