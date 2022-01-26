import csv


def load_address_and_distance_data(address_data: [], distance_data: []):

    with open('Utils/WGUPS Distance Table.csv') as distances_file:
        distances = csv.reader(distances_file, delimiter=',')
        next(distances)  # skip header

        for distance_row in distances:
            address_data.append([distance_row[0][0:-8], int(distance_row[0][-6:-1])])

            temp = []
            for i in range(1, len(distance_row)):
                temp.append(float(distance_row[i]))

            distance_data.append(temp)
