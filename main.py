from Utils.HashTable import HashTable
from Utils.LoadPackages import load_package_data
from Utils.LoadAddressesAndDistances import load_address_and_distance_data

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


def package_with_min_distance_from(from_address: str, truck_packages: []) -> str:
    min_distance = 1000
    min_distance_package = None

    for package in truck_packages:
        distance = distance_between(from_address, package.delivery_address)

        if distance < min_distance:
            min_distance = distance
            min_distance_package = package

    return min_distance_package
