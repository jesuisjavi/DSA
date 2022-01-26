from Utils.Package import Package
from Utils.HashTable import HashTable
import csv
import datetime


def load_package_data(table: HashTable):
    with open('Utils/WGUPS Package File.csv') as packages_file:
        packages = csv.reader(packages_file, delimiter=',')
        next(packages)  # skip header

        for package_row in packages:
            package_id = package_row[0]
            delivery_address = package_row[1]
            deadline = package_row[5]
            if deadline == "EOD":
                delivery_deadline = datetime.time(23, 59)
            else:
                if deadline[-2:] == "AM":
                    delivery_deadline = datetime.time(int(deadline[0:2]), int(deadline[3:5]))
                else:
                    delivery_deadline = datetime.time(int(deadline[0:2]) + 12, int(deadline[3:5]))
            delivery_city = package_row[2]
            delivery_zipcode = package_row[4]
            package_weight = package_row[6]
            delivery_status = "At the HUB"

            package = Package(int(package_id), delivery_address, delivery_deadline, delivery_city, int(delivery_zipcode)
                              , int(package_weight), delivery_status)

            table.insert(int(package_id), package)
