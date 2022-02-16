import re

url = "https://www.cardekho.com/carmodels/Maruti/Maruti_Vitara_Brezza"
#url = "https://www.cardekho.com/mercedes-benz/amg-g-63"
#url = "https://www.cardekho.com/carmodels/Tata/Tata_New_Safari"
#url = "https://www.cardekho.com/land-rover/range-rover"

splitz = url.split('/')
brand = splitz[-2].replace('_', ' ').replace('-', ' ').title()
model = splitz[-1].replace('_', ' ').replace('-', ' ').title()

if re.search(brand, model):
    print(f"{brand} is present in {model}")
    model = model.replace(brand, '').strip()
else:
    print(f"{brand} is not present in {model}")

print(brand)
print(model)