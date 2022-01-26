from Utils.HashTable import HashTable
from Utils.LoadPackages import load_package_data
from Utils.LoadAddressesAndDistances import load_address_and_distance_data

table = HashTable()
load_package_data(table)

addresses = []
distances = []
load_address_and_distance_data(addresses, distances)


def distance_between(address1, address2):
    index1 = get_address_index(address1)
    index2 = get_address_index(address2)

    if index1 < index2:
        return distances[index2][index1]
    return distances[index1][index2]


def get_address_index(address):
    for i in range(len(addresses)):
        if addresses[i][0] == address:
            return i

    return -1


