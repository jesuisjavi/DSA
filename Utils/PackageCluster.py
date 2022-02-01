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
        cluster_package = ClusterPackage(package.package_id, package.delivery_deadline)
        self.packages.append(cluster_package)
        self.packages.sort(key=lambda x: x.deliver_by, reverse=False)
        if package.delivery_deadline < self.deliver_by:
            self.deliver_by = package.delivery_deadline

    def contains_package_with_id(self, package_id) -> bool:
        for cluster_package in self.packages:
            if cluster_package.package_id == package_id:
                return True

        return False

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.packages, self.truck_number, self.is_ready, self.ready_time,
                                           self.deliver_by, self.is_assigned)


class ClusterPackage:

    def __init__(self, package_id: int, deliver_by: datetime.time):
        self.package_id = package_id
        self.deliver_by = deliver_by
