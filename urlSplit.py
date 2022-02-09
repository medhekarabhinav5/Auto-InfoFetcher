from sqlalchemy import intersect


#url = "https://www.cardekho.com/carmodels/Maruti/Maruti_Vitara_Brezza"
#url = "https://www.cardekho.com/mercedes-benz/amg-g-63"
#url = "https://www.cardekho.com/carmodels/Tata/Tata_New_Safari"
url = "https://www.cardekho.com/land-rover/range-rover"

replacableItemsList = ['-','_','/',':',',']
splitz = url.split('/')
brand = splitz[-2].replace('_', ' ').replace('-', ' ').title().split(' ')
model = splitz[-1].replace('_', ' ').replace('-', ' ').title().split(' ')
#print(brand)
#print(model)
if brand in model:
    #print("Exist")
    model = model.replace(brand, "").strip()
    #print(model)
str = "Land Rover Range Rover".split(' ')
#str = "Tata Safari".split(' ')

brand_set1 = set(brand)# Tata
brand_set2 = set(str)# Tata Safari

brand_set2.intersection(brand_set1)

model_set1 = set(model) # Tata New Safari
model_set2 = set(str) # Tata Safari
z = ' '.join(list(model_set2.symmetric_difference(model_set1)))
brand_set1 = list(brand_set1)
model_set1.remove(brand_set1[0])
model_list = list(model_set1)

final_model =  ' '.join(model_list)
final_brand = ' '.join(brand_set1)

print(final_brand)
print(final_model)