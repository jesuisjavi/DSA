from Utils.Package import Package
from Utils.HashTable import HashTable
import csv


def load_package_data(table: HashTable):
    with open('Utils/WGUPS Package File.csv') as packages_file:
        packages = csv.reader(packages_file, delimiter=',')
        next(packages)  # skip header

        for package_row in packages:
            package_id = package_row[0]
            delivery_address = package_row[1]
            delivery_deadline = package_row[5]
            delivery_city = package_row[2]
            delivery_zipcode = package_row[4]
            package_weight = package_row[6]
            delivery_status = "At the HUB"

            package = Package(int(package_id), delivery_address, delivery_deadline, delivery_city, int(delivery_zipcode)
                              , int(package_weight), delivery_status)

            table.insert(int(package_id), package)
