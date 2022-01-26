import datetime

from Utils.HashTable import HashTable
from Utils.LoadPackages import load_package_data
from Utils.LoadAddressesAndDistances import load_address_and_distance_data
from Utils.Truck import Truck
from Utils.Package import Package
from Utils.PackageCluster import PackageCluster

table = HashTable()
load_package_data(table)
print(table)

addresses = []
distances = []
load_address_and_distance_data(addresses, distances)

package_clusters = []


def distance_between(address1: str, address2: str) -> float:
    index1 = get_address_index(address1)
    index2 = get_address_index(address2)

    if index1 < index2:
        return distances[index2][index1]
    return distances[index1][index2]


def get_address_index(address: str) -> int:
    for i in range(len(addresses)):
        if addresses[i][0] == address:
            return i

    return -1


def package_with_min_distance_from(from_address: str, truck_packages: []) -> str:
    min_distance = 1000
    min_distance_package = None

    for package in truck_packages:
        distance = distance_between(from_address, package.delivery_address)

        if distance < min_distance:
            min_distance = distance
            min_distance_package = package

    return min_distance_package


def set_package_clusters():
    clusters = []

    packages_at_the_hub = table.get_packages_at_the_hub()
    for package in packages_at_the_hub:
        cluster = PackageCluster()
        cluster.add_package(package)
        clusters.append(cluster)

    print(' ****************** Add Package Constraints **************** ')

    while True:
        package_id = int(input('Enter package ID (Type -1 to skip): ').strip().lower())
        if package_id == -1:
            break

        this_package = None
        for package in packages_at_the_hub:
            if package.package_id == package_id:
                this_package = package
                break

        if this_package is not None:
            truck_number = int(input('This package must be delivered by truck number (Type -1 to skip): ')
                               .strip().lower())

            with_packages = []
            while True:
                with_package = int(input('This package must be delivered with the package with Id (Type -1 to skip): ')
                                   .strip().lower())
                if with_package != -1:
                    with_packages.append(with_package)
                else:
                    break

            is_ready = int(input('Is this package ready to leave the HUB? Type 1 for YES, 0 for NO, -1 to skip: ')
                           .strip().lower())

            cluster = PackageCluster()
            if truck_number != -1:
                cluster.truck_number = truck_number
            for package in packages_at_the_hub:
                if with_packages.count(package.package_id) > 0:
                    cluster.add_package(package)

            cluster.package_is_ready = is_ready

            clusters.append(cluster)
        else:
            print("There is no package with such Id at the HUB.")

    # Add individual package to clusters
    for package in packages_at_the_hub:
        for cluster in clusters:
            if cluster.contains_package_with_id(package.package_id):
                break

        # Package is not already in a cluster, so it will be its own cluster
        cluster = PackageCluster()
        cluster.add_package(package)
        clusters.append(cluster)

    return clusters


def truck_load_packages(trucks: [Truck]):
    clusters = set_package_clusters()

    # Order clusters by delivery deadline
    clusters.sort(key=lambda x: x.deliver_by, reverse=False)

    for truck in trucks:
        packages = 0
        cluster_index = 0

        while cluster_index < len(clusters) and packages < 16:
            cluster = clusters[cluster_index]
            if not cluster.is_assigned():
                if cluster.truck_number != truck.truck_id or not cluster.is_ready or len(
                        cluster.packages) > 16 - packages:
                    continue
                else:
                    packages = packages + len(cluster.packages)
                    for package in cluster.packages:
                        package.delivery_status = "En route"
                        truck.load_package(package)
                cluster_index = cluster_index + 1


def truck_deliver_packages(truck: Truck):
    truck_time = datetime.time(8, 0)
    truck_address = "HUB"
    miles = 0

    print("Truck " + str(truck.truck_id) + ": Starting route...")
    print("It is " + str(truck_time))

    for package in truck.cargo:
        miles = miles + distance_between(truck_address, package.delivery_address)
        time_to_deliver = distance_between(truck_address, package.delivery_address) / 18
        truck_time = truck_time + datetime.timedelta(0, time_to_deliver * 60)
        package.delivery_status = "Delivered"
        print("Delivered: " + str(package) + " At: " + str(truck_time))

    print("Truck " + str(truck.truck_id) + ": All packages have been delivered...")
    print("It is " + str(truck_time))
    print("I traveled " + str(miles) + " miles")
