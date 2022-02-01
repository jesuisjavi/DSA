"""
@author: Javier Perez Leon
Student ID: #009460534
"""

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

    print(' ****************** Add Package Constraints **************** ')

    while True:
        package_id = int(input('Enter package ID (Type -1 to skip): ').strip().lower())
        print(package_id)
        if package_id == -1:
            break

        this_package = table.search(package_id)

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

            ready_time = None
            if is_ready == 0:
                time = input('What time will this package be ready? Enter time in the format HH:MM: ').strip().lower()
                ready_time = datetime.time(int(time[0:2]), int(time[3:5]))

                address_change = int(input('Does the package delivery address need to be changed? Type 1 for YES, '
                                           '0 for NO, -1 to skip: ').strip().lower())

                if address_change == 1:
                    address = input('Enter the correct address: ')
                    this_package.delivery_address = address

            cluster = PackageCluster()
            cluster.add_package(this_package)
            if truck_number != -1:
                cluster.truck_number = truck_number
            if len(with_packages) > 0:
                for package_id in with_packages:
                    package = table.search(package_id)
                    if package is not None:
                        cluster.add_package(package)
            if is_ready == 0:
                cluster.is_ready = False
                cluster.ready_time = ready_time

            clusters.append(cluster)
        else:
            print("There is no package with such Id at the HUB.")

    # Add individual package to clusters
    # O(n)
    for package in table.get_packages_at_the_hub():
        already_in_cluster = False
        # O(n)
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


def truck_load_packages(clusters, trucks: [Truck], amount):
    for cluster in clusters:
        for truck_index in range(len(trucks)):
            truck = trucks[truck_index]

            if not cluster.is_assigned:
                if not cluster.is_ready:
                    if cluster.ready_time <= truck.truck_time:
                        cluster.is_ready = True
                    else:
                        break

                if (cluster.truck_number is not None and cluster.truck_number != truck.truck_id) or len(
                        cluster.packages) > amount - len(truck.cargo):
                    continue

                else:
                    cluster.is_assigned = True

                    for cluster_package in cluster.packages:
                        package = table.search(cluster_package.package_id)
                        package.delivery_status = "En route"
                        package.left_hub_at = truck.truck_time
                        truck.load_package(package)
                    break


def truck_deliver_packages(truck: Truck) -> float:
    miles = 0

    print("Truck " + str(truck.truck_id) + ": Starting route...")
    print("It is " + str(truck.truck_time))

    for i in range(len(truck.cargo)):
        # Deliver trucks in order of delivery deadline and distance within those with the same delivery deadline time

        min_time = datetime.time(23, 59)
        for package in truck.cargo:
            if package.delivery_deadline < min_time and package.delivery_status == "En route":
                min_time = package.delivery_deadline
        packages = []
        for package in truck.cargo:
            if package.delivery_deadline == min_time and package.delivery_status == "En route":
                packages.append(package)

        package = package_with_min_distance_from(truck.truck_address, packages)
        miles = miles + distance_between(truck.truck_address, package.delivery_address)
        time_to_deliver = distance_between(truck.truck_address, package.delivery_address) / 18
        print("The distance from my present address to the nearest package delivery location is " + str(
            distance_between(truck.truck_address, package.delivery_address)) + " miles.")
        print("It will take me " + str(time_to_deliver * 60) + " minutes to arrive.")
        truck_time = (datetime.datetime(2022, 1, 26, truck.truck_time.hour, truck.truck_time.minute,
                                        truck.truck_time.second) + datetime.timedelta(
            seconds=time_to_deliver * 60 * 60)).time()
        print(truck.truck_time)
        truck.truck_time = truck_time
        package.delivery_status = "Delivered"
        package.delivered_at = truck.truck_time
        truck.truck_address = package.delivery_address
        print("Delivered: " + str(package) + " At: " + str(truck_time))

    print("Truck " + str(truck.truck_id) + ": All packages from this load have been delivered...")
    print("It is " + str(truck.truck_time))
    print("I traveled " + str(miles) + " miles")
    print()

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

    truck_load_packages(clusters, [trucks[0]], 8)
    truck_load_packages(clusters, [trucks[1]], 16)

    for truck in trucks:
        total_mileage = total_mileage + truck_deliver_packages(truck)
        total_packages_delivered = total_packages_delivered + len(truck.cargo)

    while total_packages_delivered < total_packages:
        if trucks[0].truck_time < trucks[1].truck_time:
            trucks[0].reset_truck()
            truck_load_packages(clusters, [trucks[0]], 16)
            miles_to_hub = distance_between(trucks[0].truck_address, "HUB")
            total_mileage = total_mileage + miles_to_hub
            print("Truck 1: Driving to the HUB to pick up more packages...")
            time_to_deliver = distance_between(trucks[0].truck_address, "HUB") / 18
            truck_time = (
                    datetime.datetime(2022, 1, 26, trucks[0].truck_time.hour, trucks[0].truck_time.minute,
                                      trucks[0].truck_time.second) + datetime.timedelta(
                seconds=time_to_deliver * 60 * 60)).time()
            trucks[0].truck_time = truck_time
            trucks[0].truck_address = "HUB"
            total_mileage = total_mileage + truck_deliver_packages(trucks[0])
            total_packages_delivered = total_packages_delivered + len(trucks[0].cargo)
        else:
            trucks[1].reset_truck()
            truck_load_packages(clusters, [trucks[1]], 16)
            miles_to_hub = distance_between(trucks[1].truck_address, "HUB")
            total_mileage = total_mileage + miles_to_hub
            print("Truck 2: Driving to the HUB to pick up more packages...")
            time_to_deliver = distance_between(trucks[1].truck_address, "HUB") / 18
            truck_time = (
                    datetime.datetime(2022, 1, 26, trucks[1].truck_time.hour, trucks[1].truck_time.minute,
                                      trucks[1].truck_time.second) + datetime.timedelta(
                seconds=time_to_deliver * 60 * 60)).time()
            trucks[1].truck_time = truck_time
            trucks[1].truck_address = "HUB"
            total_mileage = total_mileage + truck_deliver_packages(trucks[1])
            total_packages_delivered = total_packages_delivered + len(trucks[1].cargo)

    print(total_packages_delivered)

    print(total_mileage)


def get_total_mileage_at(time: datetime.time):
    print()


deliver_packages()

while True:
    package_id = int(input('Enter package ID (Type -1 to end program): ').strip().lower())
    print(package_id)
    if package_id == -1:
        break

    time = input('Enter time in the format HH:MM: ').strip().lower()
    snapshot_time = datetime.time(int(time[0:2]), int(time[3:5]))

    package = table.search(package_id)

    if package is not None:
        if snapshot_time < package.left_hub_at:
            temp_package = Package(package.package_id, package.delivery_address, package.delivery_deadline,
                                   package.delivery_city, package.delivery_zipcode, package.package_weight,
                                   "At the HUB")
            print(temp_package)
        elif package.left_hub_at <= snapshot_time < package.delivered_at:
            temp_package = Package(package.package_id, package.delivery_address, package.delivery_deadline,
                                   package.delivery_city, package.delivery_zipcode, package.package_weight,
                                   "En route")
            print(temp_package)
        else:
            print(package)
    else:
        print("There is no package with such Id at the HUB.")
