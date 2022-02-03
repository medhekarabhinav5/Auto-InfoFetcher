from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
CHROMEDRIVER_PATH = "/Users/Abhinav/Desktop/chromedriver" # Chrome Driver Path
CHROME_PATH = ""
WINDOW_SIZE = "1280,800" # Screen Size
chrome_options = Options()
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("--headless")
chrome_options.binary_location = CHROME_PATH
CHROME_PATH
prefs = {'profile.managed_default_content_settings.images' : 2}
chrome_options.add_experimental_option("prefs", prefs)
#url = "https://autoportal.com/newcars/car-finder/page/1/price/1/"
chrome_options
driver = webdriver.Chrome(
executable_path = CHROMEDRIVER_PATH,
    chrome_options = chrome_options
) # Initiate browser
#PHANTOMDRIVER_PATH = "/Users/Abhinav/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs"
#driver = webdriver.PhantomJS(PHANTOMDRIVER_PATH, service_args=["--load-images=no"])
#driver.set_window_size(1280, 800)
unused_links = []
used_links = []
def check_exists_by_xpath(xpath): # Checking whether xpath is available
    
    try:

        driver.find_element_by_xpath(xpath)

    except:
        return False
    return True
#//*[@id="content"]/div[2]/div[6]/div[2]/div[4]/div[1]/div[1]/div/div[2]/div[1]/div[1]/p/a


status=True # Status of 
count = 1
            
#getting latest details from site
while status:
    url = "https://autoportal.com/newcars/car-finder/page/" + str(count) + "/price/1/"
    request = requests.get(url) # checking whether url exists
    if request.status_code == 200: # if  status of url is 200 then it will proceed.
        driver.get(url)
        false_link_count = 0
        for i in range(1,30): # each page approx have 30 links. Some are false and of no use.
            if false_link_count < 20: # segragating false from true
                status = True
                xpath = '//*[@id="content"]/div[2]/div[6]/div[2]/div[4]/div[' + str(i) + ']/div[1]/div/div[2]/div[1]/div[1]/p/a'
                response = check_exists_by_xpath(xpath)
                if response == True:
                    link_element = driver.find_element_by_xpath(xpath)
                    link = link_element.get_attribute('href') + 'specifications/'
                    print(link)
                    unused_links.append(link) # Saving links
                else:
                    false_link_count = false_link_count + 1
            else:
                status = False
        count = count + 1
    else:
        status = False
driver.quit()
import time
import pprint
import re
from selenium.webdriver.support.select import Select
#time.sleep(20)
counter = 0
carInfoFull = pd.DataFrame()

col_list = ['Make', 'Model', 'Variant', 'Ex-Showroom_Price', 'Displacement', 'Cylinders', 'Valves_Per_Cylinder', 'Drivetrain', 'Cylinder_Configuration', 'Emission_Norm', 'Engine_Location', 'Fuel_System', 'Fuel_Tank_Capacity', 'Fuel_Type', 'Height', 'Length', 'Width', 'Body_Type', 'Doors', 'City_Mileage', 'Highway_Mileage', 'ARAI_Certified_Mileage', 'ARAI_Certified_Mileage_for_CNG', 'Kerb_Weight', 'Gears', 'Ground_Clearance', 'Front_Brakes', 'Rear_Brakes', 'Front_Suspension', 'Rear_Suspension', 'Front_Track', 'Rear_Track', 'Front_Tyre_&_Rim', 'Rear_Tyre_&_Rim', 'Power_Steering', 'Power_Windows', 'Power_Seats', 'Keyless_Entry', 'Power', 'Torque', 'Odometer', 'Speedometer', 'Tachometer', 'Tripmeter', 'Seating_Capacity', 'Seats_Material', 'Type', 'Wheelbase', 'Wheels_Size', 'Start_/_Stop_Button','12v_Power_Outlet' ,'Audiosystem','Aux-in_Compatibility' ,'Average_Fuel_Consumption' ,'Basic_Warranty' ,'Bluetooth' ,'Boot-lid_Opener' ,'Boot_Space' ,'CD_/_MP3_/_DVD_Player' ,'Central_Locking' ,'Child_Safety_Locks' ,'Clock' ,'Cup_Holders' ,'Distance_to_Empty' ,'Door_Pockets' ,'Engine_Malfunction_Light' ,'Extended_Warranty' ,'FM_Radio' ,'Fuel-lid_Opener' ,'Fuel_Gauge' ,'Handbrake' ,'Instrument_Console' ,'Low_Fuel_Warning' ,'Minimum_Turning_Radius' ,'Multifunction_Display' ,'Sun_Visor' ,'Third_Row_AC_Vents' ,'Ventilation_System' ,'Auto-Dimming_Rear-View_Mirror' ,'Hill_Assist' ,'Gear_Indicator' ,'3_Point_Seat-Belt_in_Middle_Rear_Seat' ,'Ambient_Lightning' ,'Cargo/Boot_Lights' ,'Drive_Modes' ,'Engine_Immobilizer' ,'High_Speed_Alert_System' ,'Lane_Watch_Camera/_Side_Mirror_Camera' ,'Passenger_Side_Seat-Belt_Reminder' ,'Seat_Back_Pockets' ,'Voice_Recognition' ,'Walk_Away_Auto_Car_Lock' ,'ABS_(Anti-lock_Braking_System)' ,'Headlight_Reminder' ,'Adjustable_Headrests' ,'Gross_Vehicle_Weight' ,'Airbags' ,'Door_Ajar_Warning' ,'EBD_(Electronic_Brake-force_Distribution)' ,'Fasten_Seat_Belt_Warning' ,'Gear_Shift_Reminder' ,'Number_of_Airbags' ,'Compression_Ratio' ,'Adjustable_Steering_Column' ,'Other_Specs' ,'Other_specs' ,'Parking_Assistance' ,'Key_Off_Reminder' ,'USB_Compatibility' ,'Android_Auto' ,'Apple_CarPlay' ,'Cigarette_Lighter' ,'Infotainment_Screen' ,'Multifunction_Steering_Wheel' ,'Average_Speed' ,'EBA_(Electronic_Brake_Assist)' ,'Seat_Height_Adjustment' ,'Navigation_System' ,'Second_Row_AC_Vents' ,'Tyre_Pressure_Monitoring_System' ,'Rear_Center_Armrest' ,'iPod_Compatibility' ,'ESP_(Electronic_Stability_Program)' ,'Cooled_Glove_Box' ,'Recommended_Tyre_Pressure' ,'Heated_Seats' ,'Turbocharger' ,'ISOFIX_(Child-Seat_Mount)' ,'Rain_Sensing_Wipers', 'Paddle_Shifters' ,'Leather_Wrapped_Steering' ,'Automatic_Headlamps' ,'Engine_Type', 'ASR_/_Traction_Control' ,'Cruise_Control' ,'USB_Ports','Heads-Up_Display','Welcome_Lights' ,'Battery' ,'Electric_Range']
for unused in unused_links:
    print(unused)
test_links = ['https://autoportal.com/newcars/renault/kwid/specifications/','https://autoportal.com/newcars/datsun/go/specifications/']
for link in test_links:
    print(link)
import random
unused_count = len(unused_links)
while unused_count != 0:
    for unused in unused_links:
        driver = webdriver.Chrome(
        executable_path = CHROMEDRIVER_PATH,
        chrome_options = chrome_options
        ) # Initiate browser
        #driver = webdriver.PhantomJS(PHANTOMDRIVER_PATH, service_args=["--load-images=no"])
        #driver.set_window_size(1280, 800)
        #print(link)
        link_process_flag = False
        attempt_count = 1
        while link_process_flag == False and attempt_count < 4:
            try:
                print(unused)
                driver.get(unused) 
                mySelect = Select(driver.find_element_by_name("variant_key")) #getting element by variant dropdown
                variants = len(mySelect.options) # getting number of variant
                variant_count = 0 # variant Count
                carInfo = pd.DataFrame()  # to store final data of cars # Empty Dataframe
                for i in range(0,variants):
                    counter = counter + 1
                    variant_count = variant_count + 1 
                    mySelect = Select(driver.find_element_by_name("variant_key"))
                    status = mySelect.select_by_index(i) # selecting Variant
                    time.sleep(15)    # wait till page changes
                    acar_info_dict = {} # to store data of each model-variant
                    ################################################################
                    make_final = '' # final value of make
                    model_final = ''  # final value of model
                    variant_final = '' # final value of variant

                    make = unused.split("/")[4].strip() # fetching make name from link 
                    make_model_xpath = '//*[@id="content"]/div/div[9]/div[1]/section/h2' # getting string from page where only make and model is mentioned- No variant mentioned
                    make_model_variant_xpath = '//*[@id="content"]/div/div[10]/p' # getting  string from page where all 3 are mentioned
                    make_model = driver.find_element_by_xpath(make_model_xpath).text.split("of ",1)[1] # Splitting Make_model String
                    make_model_variant = driver.find_element_by_xpath(make_model_variant_xpath).text.rsplit(' ', 1)[0].split("of ",1)[1] # Splitting make_model_variant string and removeing last word from it
                    model_label = 'Model' # make label
                    make_label = 'Make' # model label
                    variant_label = 'Variant' # variant label

                    for make_name in make_model.lower().split(): # for loop for make model split
                        if make_name.lower() in make.lower(): # checking whether work matched woth make string
                            make_final = make_final + "" + make_name.title() + " " # appending

                    for model_name in make_model.lower().split(): # for loop for make model split
                        if model_name.lower() not in make.lower(): # Checking whether splits are not matching woth make # not making will be in list
                            model_final = model_final + "" + model_name.title() + " " # appending

                    make_model_split = make_model.lower().split() # make model stplit variable
                    make_model_variant_split = make_model_variant.lower().split() # make model variant split variable

                    variant = [ ele for ele in make_model_variant_split ] # getting world wise split in list
                    for a in make_model_split: 
                        if a in make_model_variant_split:  # checking if matches
                            variant.remove(a) # if matches , removed from list. remaining will be variant

                    for i in variant:
                        variant_final = variant_final + "" + i.title() + " " # Appending
                    acar_info_dict[make_label] = make_final.rstrip() # adding to dictionary
                    acar_info_dict[model_label] = model_final.rstrip() # adding to dictionary
                    acar_info_dict[variant_label] = variant_final.rstrip() # adding to dictionary
                    ################################################################        
                    price_xpath = '//*[@id="content"]/div/div[10]/div/div[1]/ul/li[1]/div/div[2]/p' # price Path
                    price_label = 'Ex-Showroom_Price'# price label
                    price = driver.find_element_by_xpath(price_xpath).text # getting price text from xpath
                    acar_info_dict[price_label] = price # adding price to dictionary
                    ################################################################
                    tech_specs = True # status of lop
                    tech_specs_count = 1 # for looping
                    while tech_specs:
                        # Checking if label exists
                        label_check = check_exists_by_xpath('//*[@id="content"]/div/section[1]/div[1]/div[' + str(tech_specs_count) + ']/div[1]')
                        # Checking if value exists
                        value_check = check_exists_by_xpath('//*[@id="content"]/div/section[1]/div[1]/div[' + str(tech_specs_count) + ']/div[2]')
                        if (label_check == True) and (value_check == True): # if both true, label and value exists
                            tech_specs = True
                            element1 = (driver.find_element_by_xpath('//*[@id="content"]/div/section[1]/div[1]/div[' + str(tech_specs_count) + ']/div[1]').text).replace(" ", "_")
                            element2 = driver.find_element_by_xpath('//*[@id="content"]/div/section[1]/div[1]/div[' + str(tech_specs_count) + ']/div[2]').text
                            acar_info_dict[element1] = element2 # saving details in dictionary
                            tech_specs_count = tech_specs_count + 1
                        elif (label_check == True) and (value_check == False): # if value is false then it is of no use. Skipping it
                            tech_specs = True
                            tech_specs_count = tech_specs_count + 1    
                        else:
                            tech_specs = False
                    ##################################################################        
                    features_specs = True # status of lop
                    features_specs_count = 1 # for looping
                    while features_specs:
                        # Checking if label exists
                        label_check = check_exists_by_xpath('//*[@id="content"]/div/section[1]/div[2]/div[' + str(features_specs_count) + ']/div[1]')
                        # Checking if value exists
                        value_check = check_exists_by_xpath('//*[@id="content"]/div/section[1]/div[2]/div[' + str(features_specs_count) + ']/div[2]')
                        if (label_check == True) and (value_check == True): # if both true, label and value exists
                            features_specs = True
                            element1 = (driver.find_element_by_xpath('//*[@id="content"]/div/section[1]/div[2]/div[' + str(features_specs_count) + ']/div[1]').text).replace(" ", "_")
                            element2 = driver.find_element_by_xpath('//*[@id="content"]/div/section[1]/div[2]/div[' + str(features_specs_count) + ']/div[2]').text
                            acar_info_dict[element1] = element2 # saving details in dictionary
                            features_specs_count = features_specs_count + 1
                        elif (label_check == True) and (value_check == False): # if value is false then it is of no use. Skipping it
                            features_specs = True
                            features_specs_count = features_specs_count + 1    
                        else:
                            features_specs = False
                    #####################################################################  
                    dims_specs = True # status of lop
                    dims_specs_count = 1 # for looping
                    while dims_specs:
                        # Checking if label exists
                        label_check = check_exists_by_xpath('//*[@id="content"]/div/section[1]/div[3]/div[' + str(dims_specs_count) + ']/div[1]')
                        # Checking if value exists
                        value_check = check_exists_by_xpath('//*[@id="content"]/div/section[1]/div[3]/div[' + str(dims_specs_count) + ']/div[2]')
                        if (label_check == True) and (value_check == True): # if both true, label and value exists
                            dims_specs = True
                            element1 = (driver.find_element_by_xpath('//*[@id="content"]/div/section[1]/div[3]/div[' + str(dims_specs_count) + ']/div[1]').text).replace(" ", "_")
                            element2 = driver.find_element_by_xpath('//*[@id="content"]/div/section[1]/div[3]/div[' + str(dims_specs_count) + ']/div[2]').text
                            acar_info_dict[element1] = element2 # saving details in dictionary
                            dims_specs_count = dims_specs_count + 1
                        elif (label_check == True) and (value_check == False): # if value is false then it is of no use. Skipping it
                            dims_specs = True
                            dims_specs_count = dims_specs_count + 1    
                        else:
                            dims_specs = False
                    #print(acar_info_dict)
                    carInfo = carInfo.append(acar_info_dict, ignore_index=True)
                    carInfoFull = carInfoFull.append(acar_info_dict, ignore_index=True)
                print(counter)
                #carInfo.reindex(columns=col_list).to_csv(r'/Users/Abhinav/Movies/DataSets/cars_ds_' + make_final.strip().replace(" ", "_") + '_' + model_final.strip().replace(" ", "_") + '.csv',header=True)
                link_process_flag = True
                used_links.append(unused)
                unused_links.remove(unused)
                unused_count = len(unused_links)
                print("Unused Links count is " + str(unused_count))
                driver.quit()
            except:
                unused_count = len(unused_links)
                print("Unused Links count is " + str(unused_count))
                attempt_count = attempt_count + 1
                print("Attempts for " + make_final.strip() + " " + model_final.strip() + "is" + str(attempt_count))
                link_process_flag = False
            
carInfoFull

#carInfoFull.to_csv(r'/Users/Abhinav/Movies/DataSets/cars_ds.csv',header=True ,cols=['Make', 'Model', 'Variant', 'Ex-Showroom_Price', 'Displacement', 'Cylinders', 'Valves_Per_Cylinder', 'Drivetrain', 'Cylinder_Configuration', 'Emission_Norm', 'Engine_Location', 'Fuel_System', 'Fuel_Tank_Capacity', 'Fuel_Type', 'Height', 'Length', 'Width', 'Body_Type', 'Doors', 'City_Mileage', 'Highway_Mileage', 'ARAI_Certified_Mileage', 'ARAI_Certified_Mileage_for_CNG', 'Kerb_Weight', 'Gears', 'Ground_Clearance', 'Front_Brakes', 'Rear_Brakes', 'Front_Suspension', 'Rear_Suspension', 'Front_Track', 'Rear_Track', 'Front_Tyre_&_Rim', 'Rear_Tyre_&_Rim', 'Power_Steering', 'Power_Windows', 'Power_Seats', 'Keyless_Entry', 'Power', 'Torque', 'Odometer', 'Speedometer', 'Tachometer', 'Tripmeter', 'Seating_Capacity', 'Seats_Material', 'Type', 'Wheelbase', 'Wheels_Size', 'Start_/_Stop_Button','12v_Power_Outlet','Audiosystem','Aux-in_Compatibility','Average_Fuel_Consumption','Basic_Warranty' ,'Bluetooth','Boot-lid_Opener' ,'Boot_Space' ,'CD_/_MP3_/_DVD_Player' ,'Central_Locking' ,'Child_Safety_Locks' ,'Clock' ,'Cup_Holders' ,'Distance_to_Empty' ,'Door_Pockets' ,'Engine_Malfunction_Light' ,'Extended_Warranty' ,'FM_Radio' ,'Fuel-lid_Opener' ,'Fuel_Gauge' ,'Handbrake' ,'Instrument_Console' ,'Low_Fuel_Warning' ,'Minimum_Turning_Radius' ,'Multifunction_Display' ,'Sun_Visor' ,'Third_Row_AC_Vents' ,'Ventilation_System' ,'Auto-Dimming_Rear-View_Mirror' ,'Hill_Assist' ,'Gear_Indicator' ,'3_Point_Seat-Belt_in_Middle_Rear_Seat' ,'Ambient_Lightning' ,'Cargo/Boot_Lights' ,'Drive_Modes' ,'Engine_Immobilizer' ,'High_Speed_Alert_System' ,'Lane_Watch_Camera/_Side_Mirror_Camera' ,'Passenger_Side_Seat-Belt_Reminder' ,'Seat_Back_Pockets' ,'Voice_Recognition' ,'Walk_Away_Auto_Car_Lock' ,'ABS_(Anti-lock_Braking_System)' ,'Headlight_Reminder' ,'Adjustable_Headrests' ,'Gross_Vehicle_Weight' ,'Airbags' ,'Door_Ajar_Warning' ,'EBD_(Electronic_Brake-force_Distribution)' ,'Fasten_Seat_Belt_Warning' ,'Gear_Shift_Reminder' ,'Number_of_Airbags' ,'Compression_Ratio' ,'Adjustable_Steering_Column' ,'Other_Specs' ,'Other_specs' ,'Parking_Assistance' ,'Key_Off_Reminder' ,'USB_Compatibility' ,'Android_Auto' ,'Apple_CarPlay' ,'Cigarette_Lighter' ,'Infotainment_Screen' ,'Multifunction_Steering_Wheel' ,'Average_Speed' ,'EBA_(Electronic_Brake_Assist)' ,'Seat_Height_Adjustment' ,'Navigation_System' ,'Second_Row_AC_Vents' ,'Tyre_Pressure_Monitoring_System' ,'Rear_Center_Armrest' ,'iPod_Compatibility' ,'ESP_(Electronic_Stability_Program)' ,'Cooled_Glove_Box' ,'Recommended_Tyre_Pressure' ,'Heated_Seats' ,'Turbocharger' ,'ISOFIX_(Child-Seat_Mount)' ,'Rain_Sensing_Wipers', 'Paddle_Shifters' ,'Leather_Wrapped_Steering' ,'Automatic_Headlamps' ,'Engine_Type', 'ASR_/_Traction_Control' ,'Cruise_Control' ,'USB_Ports' ,'Heads-Up_Display' ,'Welcome_Lights' ,'Battery' ,'Electric_Range'])
carInfoFull.reindex(columns=col_list).to_csv(r'/Users/Abhinav/Movies/DataSets/cars_ds_india_final_02_2022.csv',header=True)
                
'''
make_final = ''
model_final = ''
for word in string.lower().split():
    if word.lower() in make.lower(): 
        make_final = make_final + "" + word.title() + " "
for word in string.lower().split():
    if word.lower() not in make_final.lower(): 
        model_final = model_final + "" + word.title() + " "
'''    
'''
make = 'datsun'
print(make.title())
#'marutisuzuki'
'''
'''
make_model_variant = 'Ex-Showroom Price, Offers & Key Features of Datsun redi-GO D (Petrol)'
make_model = 'Specifications of Datsun redi-GO'
make_model_string = make_model.split("of ",1)[1]
make_model_variant_string = make_model_variant.rsplit(' ', 1)[0].split("of ",1)[1]
print(make_model_string)
print(make_model_variant_string)
'''
'''
make_final = ''
model_final = ''
variant_final = ''

for make_name in make_model_string.lower().split():
    if make_name.lower() in make.lower(): 
        make_final = make_final + "" + make_name.title() + " "

for model_name in make_model_string.lower().split():
    if model_name.lower() not in make.lower(): 
        model_final = model_final + "" + model_name.title() + " "
vf = set(make_model_variant_string.lower().split()) - set(make_model_string.lower().split())
for i in vf:
    variant_final = variant_final + "" + i.title() + " "
    '''