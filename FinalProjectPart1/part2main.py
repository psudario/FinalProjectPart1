exec(open("main.py").read())


#read from FullInventory.csv and make a set of manufacturerers and item type
full_inventory={}
manufacturers=set()
item_types=set()
past_service_date=set()

with open("PastServiceDateInventory.csv", "r") as my_file: #populates past_service_date set for easy access
    line = my_file.readline()
    while line:
        items = line.split(",")[0:-1]
        past_service_date.add(int(items[0]))
        line = my_file.readline()
with open("FullInventory.csv", "r") as my_file:
    line=my_file.readline()
    while line:
        items=line.split(",")[0:-1]
        for i in range(len(items)): items[i]= items[i].strip() #strips white space for items
        manufacturers.add(items[1].lower()) #manufacturer is always second row
        item_types.add(items[2].lower()) #item type is always third row

        if len(items) < 6:
            full_inventory[int(items[0])] = (items[1].strip(),items[2].strip(), items[3].strip(), items[4])
        else:
            full_inventory[int(items[0])] = (items[1].strip(), items[2].strip(), items[3].strip(), items[4], "damaged")

        line=my_file.readline()

#Step 1
user_input = input("What do you want").lower()
while user_input != "q":
    user_manufacturer= None
    user_item_type= None
    manufacturer_makes_items = False
    multiple_types= False

    #split user_input into list and check if each word is in either manufacturers or item_types set
    user_input = user_input.split(" ")

    #for word in user_input:
     #   if word in manufacturers: user_manufacturer = word
     #   if word in item_types: user_item_type = word


    for word in user_input:
        if (user_manufacturer != None) and (word in manufacturers):
            multiple_types = True
            break
        if (user_item_type != None) and (word in item_types):
            multiple_types = True
            break


        if (user_manufacturer == None) and (word in manufacturers):
            user_manufacturer = word
        if (user_item_type == None) and (word in item_types):
            user_item_type = word


    #check if manufacturer makes the items
    for key, values in full_inventory.items():
        if (user_manufacturer != None and user_item_type != None) and values[0].lower() == user_manufacturer.lower() and values[1].lower() == user_item_type.lower():
            manufacturer_makes_items = True
            break


    #Item i
    if(user_manufacturer == None) or (user_item_type == None) or (manufacturer_makes_items == False) or (multiple_types == True):
        print("No such item in inventory")

    else:

        #item ii
        valid_items = []

        for key, values in full_inventory.items(): #populate valid_items with valid items
            if values[0].lower() == user_manufacturer.lower() and values[1].lower() == user_item_type.lower() and values[-1] != "damaged" and (key not in past_service_date):
                valid_items.append((key, values))


        valid_items.sort(key = lambda x: int(x[1][2])) #sort valid items in ascending order based on price
        returned_item = valid_items[-1]
        print("Your item is:",returned_item[0], returned_item[1][0], returned_item[1][1], returned_item[1][2])

        #item iii
        valid_alt_items=[]


        for key, values in full_inventory.items(): #populate valid_items with valid items
            if values[0].lower() != user_manufacturer.lower() and values[1].lower() == user_item_type.lower() and values[-1] != "damaged" and (key not in past_service_date):
                valid_alt_items.append((key, values))

        valid_alt_items.sort(key = lambda x: abs(int(returned_item[1][2]) - int(x[1][2]))) #sort valid items in ascending order based on price


        for i in range(4): #show the first four similar items thats closest in range
            if i >= len(valid_alt_items): break
            alt_item = valid_alt_items[i]
            print("You may also want to consider:" ,alt_item[0], alt_item[1][0], alt_item[1][1], alt_item[1][2])

    #item iiii
    user_input = input("Another Query or Enter q to quit")













