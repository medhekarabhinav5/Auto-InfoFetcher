from sqlalchemy import intersect


#url = "https://www.cardekho.com/carmodels/Maruti/Maruti_Vitara_Brezza"
#url = "https://www.cardekho.com/mercedes-benz/amg-g-63"
url = "https://www.cardekho.com/carmodels/Tata/Tata_New_Safari"
replacableItemsList = ['-','_','/',':',',']
splitz = url.split('/')
brand = splitz[-2].replace('_', ' ').replace('-', ' ').title()
model = splitz[-1].replace('_', ' ').replace('-', ' ').title()
print(brand)
print(model)
if brand in model:
    print("Exist")
    model = model.replace(brand, "").strip()
    print(model)

set1 = {"Tata", "New" , "Safari"}
set2 = {"Safari"}

set1.intersection(set2)
print(set1)

set1 = {"Tata", "New" , "Safari"}
set2 = {"Tata"}

set1.intersection(set2)
print(set1)

x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}

z = x.symmetric_difference(y)

print(z)