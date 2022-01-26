from Utils.Package import Package
import datetime


class PackageCluster:

    def __init__(self):
        self.packages = []
        self.truck_number = None
        self.package_is_ready = True
        self.deliver_by = datetime.time(23, 59)

    def add_package(self, package: Package):
        self.packages.append(package)
        if package.delivery_deadline < self.deliver_by:
            self.deliver_by = package.delivery_deadline

    def contains_package_with_id(self, package_id) -> bool:
        for package in self.packages:
            if package.package_id == package_id:
                return True

        return False
