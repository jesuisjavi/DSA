import datetime

from Utils.HashTable import HashTable
from Utils.LoadPackages import load_package_data
from Utils.LoadAddressesAndDistances import load_address_and_distance_data
from Utils.Truck import Truck
from Utils.Package import Package
from Utils.PackageCluster import PackageCluster

table = HashTable()
load_package_data(table)

addresses = []
distances = []
load_address_and_distance_data(addresses, distances)


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


def package_with_min_distance_from(from_address: str, truck_packages: []) -> Package:
    min_distance = 1000
    min_distance_package = None

    for package in truck_packages:
        if package.delivery_status == "En route":
            distance = distance_between(from_address, package.delivery_address)

            if distance < min_distance:
                min_distance = distance
                min_distance_package = package

    return min_distance_package


def set_package_clusters():
    clusters = []

    packages_at_the_hub = table.get_packages_at_the_hub()

    print(' ****************** Add Package Constraints **************** ')

    while True:
        package_id = int(input('Enter package ID (Type -1 to skip): ').strip().lower())
        print(package_id)
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

            print(with_packages)
            cluster = PackageCluster()
            cluster.add_package(this_package)
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
        already_in_cluster = False
        for cluster in clusters:
            if cluster.contains_package_with_id(package.package_id):
                already_in_cluster = True
                break

        # Package is not already in a cluster, so it will be its own cluster
        if not already_in_cluster:
            cluster = PackageCluster()
            cluster.add_package(package)
            clusters.append(cluster)

    for cluster in clusters:
        print(cluster)

    return clusters


def truck_load_packages(clusters, trucks: [Truck]):
    truck_index = 0
    packages = 0

    for cluster in clusters:
        truck = trucks[truck_index]

        if not cluster.is_assigned:
            if (cluster.truck_number is not None and cluster.truck_number != truck.truck_id) or not cluster.is_ready \
                    or len(cluster.packages) > 16 - len(truck.cargo):
                continue
            else:
                cluster.is_assigned = True
                packages = packages + len(cluster.packages)
                for package in cluster.packages:
                    package.delivery_status = "En route"
                    truck.load_package(package)

                if truck_index == len(trucks) - 1:
                    truck_index = 0
                else:
                    truck_index = truck_index + 1


def truck_deliver_packages(truck: Truck) -> float:
    truck_time = datetime.time(8, 0)
    truck_address = "HUB"
    miles = 0

    print("Truck " + str(truck.truck_id) + ": Starting route...")
    print("It is " + str(truck_time))

    for i in range(len(truck.cargo)):
        package = package_with_min_distance_from(truck_address, truck.cargo)
        miles = miles + distance_between(truck_address, package.delivery_address)
        time_to_deliver = distance_between(truck_address, package.delivery_address) / 18
        print(distance_between(truck_address, package.delivery_address))
        print(time_to_deliver)
        truck_time = (datetime.datetime(2022, 1, 26, truck_time.hour, truck_time.minute) + datetime.timedelta(
            seconds=time_to_deliver * 60 * 60)).time()
        print(truck_time)
        truck.truck_time = truck_time
        package.delivery_status = "Delivered"
        truck_address = package.delivery_address
        print("Delivered: " + str(package) + " At: " + str(truck_time))

    print("Truck " + str(truck.truck_id) + ": All packages have been delivered...")
    print("It is " + str(truck_time))
    print("I traveled " + str(miles) + " miles")

    return miles


def deliver_packages():
    trucks = [Truck(1), Truck(2)]

    total_mileage = 0

    total_packages = 40
    total_packages_delivered = 0

    # Set clusters
    clusters = set_package_clusters()
    print("Clusters set")
    print(clusters)

    # Order clusters by delivery deadline
    clusters.sort(key=lambda x: x.deliver_by, reverse=False)

    truck_load_packages(clusters, trucks)

    for truck in trucks:
        total_mileage = total_mileage + truck_deliver_packages(truck)
        total_packages_delivered = total_packages_delivered + len(truck.cargo)

    if trucks[0].truck_time < trucks[1].truck_time:
        trucks[0].reset_truck()
        truck_load_packages(clusters, [trucks[0]])
        total_mileage = total_mileage + truck_deliver_packages(trucks[0])
        total_packages_delivered = total_packages_delivered + len(trucks[0].cargo)
    else:
        trucks[1].reset_truck()
        truck_load_packages(clusters, [trucks[1]])
        total_mileage = total_mileage + truck_deliver_packages(trucks[1])
        total_packages_delivered = total_packages_delivered + len(trucks[1].cargo)

    print(total_packages_delivered)

    print(total_mileage)


deliver_packages()
