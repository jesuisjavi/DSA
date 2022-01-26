import Package

"""
Truck class.

Represents a truck and delivers up to 16 packages at a time.
"""


class Truck:

    def __init__(self):
        self.cargo = []

    def load(self, package: Package):
        self.cargo.append(package)
