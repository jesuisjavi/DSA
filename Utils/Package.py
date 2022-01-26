import datetime

"""
 Package class

 Represents a package to be delivered on a given day.
"""


class Package:

    def __init__(self, package_id: int, delivery_address: str, delivery_deadline: datetime.time, delivery_city: str,
                 delivery_zipcode: int, package_weight: int, delivery_status: str):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.delivery_deadline = delivery_deadline
        self.delivery_city = delivery_city
        self.delivery_zipcode = delivery_zipcode
        self.package_weight = package_weight
        self.delivery_status = delivery_status

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.delivery_address, self.delivery_city,
                                               self.delivery_zipcode, self.delivery_deadline, self.package_weight,
                                               self.delivery_status)
