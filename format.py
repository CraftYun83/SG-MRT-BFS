import csv, json

count = 1

dic = {

}

with open('MRT.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for i in csv_reader:
        if i[0] != "stn_code" and i[0] != "":
            if i[1] not in dic.keys():
                dic[i[1]] = [count, [i[0]]]
                count += 1
            else:
                dic[i[1]][1].append(i[0])

with open('formatted.json', "w") as file:
    json.dump(dic, file, indent=4)