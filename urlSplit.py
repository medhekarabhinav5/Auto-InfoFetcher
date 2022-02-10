from sqlalchemy import intersect


#url = "https://www.cardekho.com/carmodels/Maruti/Maruti_Vitara_Brezza"
#url = "https://www.cardekho.com/mercedes-benz/amg-g-63"
#url = "https://www.cardekho.com/carmodels/Tata/Tata_New_Safari"
url = "https://www.cardekho.com/land-rover/range-rover"

replacableItemsList = ['-','_','/',':',',']
splitz = url.split('/')
brand = splitz[-2].replace('_', ' ').replace('-', ' ').title().split(' ')
model = splitz[-1].replace('_', ' ').replace('-', ' ').title().split(' ')

brand_list = brand
model_list = model
originalBrandModel = "Land Rover Range Rover".split(' ')
originalmodel = [brand for brand in originalBrandModel if brand != brand_list[0]]
originalBrand = [model for model in originalBrandModel if model != originalmodel[0]]

print(originalmodel)
print(originalBrand)

'''if brand in model:
    #print("Exist")
    model = model.replace(brand, "").strip()
    #print(model)
#str = "Land Rover Range Rover".split(' ')
originalBrandModel = "Tata Safari".split(' ')

brand_set = set(brand)# Tata
brand_list = list(brand_set)
model_list = model
originalBrandModel.remove(brand_list[0])

if len(model) != len(originalBrandModel):
    print(model)
    print(originalBrandModel)


final_model =  ' '.join(model_list)
final_brand = ' '.join(brand_set)

print(final_brand)
print(final_model)'''