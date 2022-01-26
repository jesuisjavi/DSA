from Utils.Package import Package
import datetime


class PackageCluster:

    def __init__(self):
        self.packages = []
        self.truck_number = None
        self.is_ready = True
        self.deliver_by = datetime.time(23, 59)
        self.is_assigned = False

    def add_package(self, package: Package):
        self.packages.append(package)
        self.packages.sort(key=lambda x: x.deliver_deadline, reverse=False)
        if package.delivery_deadline < self.deliver_by:
            self.deliver_by = package.delivery_deadline

    def contains_package_with_id(self, package_id) -> bool:
        for package in self.packages:
            if package.package_id == package_id:
                return True

        return False
