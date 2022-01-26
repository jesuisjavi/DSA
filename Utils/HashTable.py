from Utils.Package import Package

"""
Chaining Hashtable class.

Will hold the packages to be delivered on a given day.

Size by default: 50

References: https://westerngovernorsuniversity-my.sharepoint.com/personal/cemal_tepe_wgu_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fcemal%5Ftepe%5Fwgu%5Fedu%2FDocuments%2FMyDocs%2FC950%2FWebinar%2FC950%20%2D%20Webinar%2D1%20%2D%20Let%27s%20Go%20Hashing%2Epdf&parent=%2Fpersonal%2Fcemal%5Ftepe%5Fwgu%5Fedu%2FDocuments%2FMyDocs%2FC950%2FWebinar
"""


class HashTable:

    def __init__(self, size=50):
        self.table = []
        for i in range(size):
            self.table.append([])

    # Inserts a package id - package pair into tne Has Table
    def insert(self, package_id: int, package: Package) -> None:
        bucket = package.package_id % len(self.table)
        bucket_list = self.table[bucket]

        bucket_list.append([package_id, package])

    # Retrieves a Package, if ei exists in the table, by its package id
    def search(self, package_id: int) -> Package:
        bucket = package_id % len(self.table)
        bucket_list = self.table[bucket]

        for id_package_pair in bucket_list:
            if id_package_pair[0] == package_id:
                return id_package_pair[1]

        return None

    # Removes a Package, if ei exists in the table, by its package id
    def remove(self, package_id: int) -> None:
        bucket = package_id % len(self.table)
        bucket_list = self.table[bucket]

        for id_package_pair in bucket_list:
            if id_package_pair[0] == package_id:
                bucket_list.remove([id_package_pair[0], id_package_pair[1]])

    def __str__(self):
        for bucket in self.table:
            for id_package_pair in bucket:
                print("Package Id: " + str(id_package_pair[0]), "- Package: " + str(id_package_pair[1]))
