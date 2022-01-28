from Utils.Package import Package
import datetime


class PackageCluster:

    def __init__(self):
        self.packages = []
        self.truck_number = None
        self.is_ready = True
        self.ready_time = datetime.time(8, 0)
        self.deliver_by = datetime.time(23, 59)
        self.is_assigned = False

    def add_package(self, package: Package):
        self.packages.append(package)
        self.packages.sort(key=lambda x: x.delivery_deadline, reverse=False)
        if package.delivery_deadline < self.deliver_by:
            self.deliver_by = package.delivery_deadline

    def contains_package_with_id(self, package_id) -> bool:
        for package in self.packages:
            if package.package_id == package_id:
                return True

        return False

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.packages, self.truck_number, self.is_ready, self.ready_time,
                                           self.deliver_by, self.is_assigned)
