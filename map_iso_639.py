import csv

with open("./iso-639-3.tab", "r") as f:
    reader = csv.DictReader(f, delimiter="\t")

    for row in reader:
        if(row["Part1"]):
            print(row)
            