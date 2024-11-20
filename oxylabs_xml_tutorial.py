import xml.etree.ElementTree as ET
root = ET.parse("sample.xml")

parsed_dict = dict()

for child in root.iter():
   if child.text.strip():
       parsed_dict[child.tag] = child.text


# print(parsed_dict)

import untangle
parsed_xml = untangle.parse("sample.xml")

data = []
for food in parsed_xml.metadata.food:
    item_name = food.item.cdata
    item_type = food.item["type"]
    price = food.price.cdata
    description = food.description.cdata
    calories = food.calories.cdata
    ingredients = [ingredient.cdata for ingredient in food.ingredients.ingredient]

    data.append({
        "item_name": item_name,
        "item_type": item_type,
        "price": price,
        "description": description,
        "calories": calories,
        "ingredients": ingredients
    })

# print(data)

parsed_xml = untangle.parse("activity_17561885211.tcx")

# print(parsed_xml.TrainingCenterDatabase.Activities.Activity)

for Lap in parsed_xml.TrainingCenterDatabase.Activities.Activity.Lap:
    print(Lap.TotalTimeSeconds.cdata + " " + Lap.DistanceMeters.cdata +  " " + str(float(Lap.DistanceMeters.cdata)/float(Lap.TotalTimeSeconds.cdata)))