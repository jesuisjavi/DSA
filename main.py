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

# Load Package data from file into Hashtable
table = HashTable()
load_package_data(table)

# load addresses and distance data from file
addresses = []
distances = []
load_address_and_distance_data(addresses, distances)

# This list will keep a list for each truck with the mileage driven for each package when it is delivered and the time
# when it happened, to calculate the total mileage at any point in time
trucks_time_mileage = []


# Calculates the distance between two addresses
def distance_between(address1: str, address2: str) -> float:
    index1 = get_address_index(address1)
    index2 = get_address_index(address2)

    if index1 < index2:
        return distances[index2][index1]
    return distances[index1][index2]


# Gets index from address in the distance matrix
def get_address_index(address: str) -> int:
    for i in range(len(addresses)):
        if addresses[i][0] == address:
            return i

    return -1


# Determines the package that is closer to the provided address from those in the truck's cargo
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


# Sets package clusters by asking the user to enter constraints.
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
            # Truck number where the package needs to be delivered
            truck_number = int(input('This package must be delivered by truck number (Type -1 to skip): ')
                               .strip().lower())

            # packages that must be delivered together with the present package
            with_packages = []
            while True:
                with_package = int(input('This package must be delivered with the package with Id (Type -1 to skip): ')
                                   .strip().lower())
                if with_package != -1:
                    with_packages.append(with_package)
                else:
                    break

            # If package is not ready, the time at which it will be ready is needed. The address of the package
            # can be changed as well
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
    # Get all packages
    for package in table.get_packages_at_the_hub():
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

    return clusters


# Loads trucks with up to the amount of packages per truck provided
def truck_load_packages(clusters, trucks: [Truck], amount):
    for cluster in clusters:
        for truck_index in range(len(trucks)):
            truck = trucks[truck_index]

            if not cluster.is_assigned:
                if not cluster.is_ready:
                    # if cluster is not ready but its ready time has already passed, it can be set to ready and loaded
                    # into truck
                    if cluster.ready_time <= truck.truck_time:
                        cluster.is_ready = True
                    else:
                        break

                # If this cluster has a truck number assigned and this is not that truck, skip this truck
                # OR
                # If truck does not have enough space to load this package cluster, skip this truck
                if (cluster.truck_number is not None and cluster.truck_number != truck.truck_id) or len(
                        cluster.packages) > amount - len(truck.cargo):
                    continue

                else:
                    cluster.is_assigned = True

                    # Load packages in truck
                    for cluster_package in cluster.packages:
                        package = table.search(cluster_package.package_id)
                        package.delivery_status = "En route"
                        package.left_hub_at = truck.truck_time
                        truck.load_package(package)
                    break


# Delivers packages from a truck. Returns the number of miles driven
def truck_deliver_packages(truck: Truck, total_mileage: float) -> float:
    miles = 0

    print("Truck " + str(truck.truck_id) + ": Starting route...")
    print("It is " + str(truck.truck_time))

    for i in range(len(truck.cargo)):
        # Deliver trucks in order of delivery deadline and distance within those with the same delivery deadline time

        # Determine minimum delivery deadline from packages that have not been delivered
        min_time = datetime.time(23, 59)
        for package in truck.cargo:
            if package.delivery_deadline < min_time and package.delivery_status == "En route":
                min_time = package.delivery_deadline
        packages = []

        # Get packages with delivery time equals to min_time
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

        # Update package and truck after delivering the package
        truck.truck_time = truck_time
        package.delivery_status = "Delivered"
        package.delivered_at = truck.truck_time
        trucks_time_mileage[truck.truck_id - 1].append([truck.truck_time, miles])
        truck.truck_address = package.delivery_address
        print("Delivered: " + str(package) + " At: " + str(truck_time))

    print("Truck " + str(truck.truck_id) + ": All packages from this load have been delivered...")
    print("It is " + str(truck.truck_time))
    print("I traveled " + str(miles) + " miles")
    print()

    return miles


# Trucks available. In this case only 2 trucks because there are only 2 drivers available
trucks = [Truck(1), Truck(2)]


# Deliver all packages
def deliver_packages():
    # Number of packages to deliver
    total_packages = 40
    # Packages delivered so far
    total_packages_delivered = 0
    # Total mileage from all trucks
    total_mileage = 0

    # Set package clusters
    clusters = set_package_clusters()
    print("Clusters set")

    # Order clusters by delivery deadline
    clusters.sort(key=lambda x: x.deliver_by, reverse=False)

    # Load packages into trucks
    truck_load_packages(clusters, [trucks[0]], 8)
    truck_load_packages(clusters, [trucks[1]], 16)

    # Deliver each truck's first load of packages
    for truck in trucks:
        trucks_time_mileage.append([])
        total_mileage = total_mileage + truck_deliver_packages(truck, total_mileage)
        total_packages_delivered = total_packages_delivered + len(truck.cargo)

    # Until all packages have been delivered send back trucks to the HUB to load and deliver
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
            total_mileage = total_mileage + truck_deliver_packages(trucks[0], total_mileage)
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
            total_mileage = total_mileage + truck_deliver_packages(trucks[1], total_mileage)
            total_packages_delivered = total_packages_delivered + len(trucks[1].cargo)

    print("Number of packages delivered: " + str(total_packages_delivered))

    print("Total mileage driven by all trucks: " + str(total_mileage))

    print()


# Determine the mileage driven at a specific time of the day
def get_total_mileage_at(at_time: datetime.time):
    mileage = 0

    for truck in trucks:
        for pair in trucks_time_mileage[truck.truck_id]:
            if pair[0] <= at_time:
                mileage = mileage + pair[1]

    return mileage


# Deliver all packages
deliver_packages()

# After all packages have been delivered, the user can enter a package id and a time and the status of such package
# at that time will de printed, as well as the total mileage driven by all trucks until that time
while True:
    package_id = int(input('Enter package ID (Type -1 to end program): ').strip().lower())
    print(package_id)
    if package_id == -1:
        break

    time = input('Enter time in the format HH:MM: ').strip().lower()
    snapshot_time = datetime.time(int(time[0:2]), int(time[3:5]))

    pckg = table.search(package_id)

    if pckg is not None:
        if snapshot_time < pckg.left_hub_at:
            temp_package = Package(pckg.package_id, pckg.delivery_address, pckg.delivery_deadline,
                                   pckg.delivery_city, pckg.delivery_zipcode, pckg.package_weight,
                                   "At the HUB")
            print(temp_package)
            print("Total mileage driven by all trucks until this time is: " + str(get_total_mileage_at(snapshot_time)))
        elif pckg.left_hub_at <= snapshot_time < pckg.delivered_at:
            temp_package = Package(pckg.package_id, pckg.delivery_address, pckg.delivery_deadline,
                                   pckg.delivery_city, pckg.delivery_zipcode, pckg.package_weight,
                                   "En route")
            print(temp_package)
            print("Total mileage driven by all trucks until this time is: " + str(
                get_total_mileage_at(snapshot_time)))
        else:
            print(pckg)
            print("Total mileage driven by all trucks until this time is: " + str(
                get_total_mileage_at(snapshot_time)))
    else:
        print("There is no package with such Id at the HUB.")
