my_dict={}                                                  #Jalen Combong 2038587
manufacturer_list=[]
price_list=[]
service_dates_list=[]
types=set()

#reading from input files and storing them into lists
with open("PriceList(1).csv", "r") as my_file:
    line=my_file.readline()
    while line:
        price_list.append(line[0:-1])
        line=my_file.readline()

with open("ManufacturerList(3).csv", "r") as my_file:
    line=my_file.readline()
    while line:
        manufacturer_list.append(line[0:-2])
        line=my_file.readline()

with open("ServiceDatesList(3).csv", "r") as my_file:
    line=my_file.readline()
    while line:
        service_dates_list.append(line[0:-1])
        line=my_file.readline()


#formatting the data in lists into a dictionary
for entry in manufacturer_list:
    line=entry.split(",")

    if len(line) < 4:
        my_dict[int(line[0])] = (line[1].strip(), line[2].strip())
    else:
        my_dict[int(line[0])] = (line[1].strip(), line[2].strip(), "damaged")


for entry in price_list:
    line=entry.split(",") #split the lines based off the commas
    id_values= list(my_dict[int(line[0])]) #search for id in dictionary
    id_values.append(int(line[1])) #append price to values of the id
    my_dict[int(line[0])] = tuple(id_values)

for entry in service_dates_list:
    line=entry.split(",")
    id_values= list(my_dict[int(line[0])])
    id_values.append(line[1])
    my_dict[int(line[0])] = tuple(id_values)

for key, value in my_dict.items(): #find the different types of things
    types.add(value[1])

#part a output
with open("FullInventory.csv", "w") as my_file:
    for key, values in my_dict.items():
        line = str(key)
        damaged= "damaged" in values #checking if items are damaged
        for value in values: #adds to line in csv
            if not value == "damaged":
                line += ", " + str(value)
        if damaged:         #append it to the end of the line
            line +=", damaged"
        my_file.write(line + ",\n")

#part b output
for type in types:
    filename = type + "inventory.csv"
    filename= filename[0].upper() + filename[1:]

    output_lines=[]
    with open(filename, "w") as my_file:
        for key, values in my_dict.items():
            if values[1] ==type:
                line = str(key)
                damaged= "damaged" in values
                for value in values:
                    if not value == "damaged" and not value == type:
                        line += ", " + str(value)
                if damaged:
                    line +=", damaged"
                output_lines.append(line)
        output_lines.sort(key = lambda x : int(x[0:x.find(",")]))
        with open(filename, "w") as my_file:
            for output_line in output_lines:
                my_file.write(output_line+", \n")

#part c output
from datetime import datetime as date
outdated =[]
for key, values in my_dict.items():
    month, day, year= tuple(values[-1].split("/"))
    month, day, year= int(month), int(day), int(year)
    if(date(year, month,day)) < date.now():
        line = str(key)
        damaged = "damaged" in values
        for value in values:
            if not value == "damaged":
                line += ", " + str(value)
        if damaged:
            line +=", damaged"
        outdated.append(line)

def return_date_object(entry):              #function to return date given a csv line entry
    index = -2 if entry.split(",")[-1] == "damaged" else -1

    month, day, year= tuple(entry.split(",")[index].split("/"))
    month, day, year= int(month), int(day), int(year)
    return date(year, month, day)

outdated.sort(key= lambda x : return_date_object(x))

with open("PastServiceDateInventory.csv", "w") as my_file:
    for line in outdated:
        my_file.write(line +", \n")

#part d output
damaged_items=[]
for key, values in my_dict.items():
    if "damaged" in values:
        line= [key]
        for value in values:
            if value != "damaged":
                line.append(value)
        damaged_items.append(line)
damaged_items.sort(key=lambda x: x[-2], reverse=True)
with open("DamagedInventory.csv", "w") as my_file:
    for damaged_item in damaged_items:
        line = ""
        for item in damaged_item:
            line += str(item) + ","
        my_file.write(line + "\n")













