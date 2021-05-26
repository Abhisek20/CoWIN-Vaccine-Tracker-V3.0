#!/usr/bin/env python
# coding: utf-8
'''
File: Covid Vaccine Tacker v3.0
Dev.: Abhisek Ghosh
Date: 26/05/2021
Email: abhisekg9516@gmail.com
'''

# In[2]:


import requests
import json
import pandas as pd
from playsound import playsound
from datetime import datetime
import time
import webbrowser


# In[12]:


t1 = datetime.now()


# In[13]:


t2 = datetime.now()


# In[8]:


config_data = open('config.json')
config_data = json.load(config_data)


# In[15]:


version = config_data['version_name']
app_type = config_data["app_type"]
vaccine_limit = int(config_data["vaccine_lim"])


# In[18]:


print("Covid Vaccine Tracker Console Version-{}".format(version), "\n")
date = input('\nEnter Date(DD/MM/YYYY format only) => ')
date = int(date.replace('/', ''))
dist_code = input("\nEnter District code => ")
age = int(input('\nEnter age => '))


# In[15]:


URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(
    dist_code, date)
header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
        }


# # Manual

# In[10]:


if app_type == "manual":
    res = requests.get(URL, headers=header)
    response_json = res.json()
    response_df = pd.DataFrame(dict(response_json)['sessions'])
    filter_df = response_df[(response_df.min_age_limit == age) & (response_df.available_capacity > vaccine_limit)]

    from tkinter import *

    if filter_df.shape[0] > 0:
        root = Tk()
        root.title('CoWIN Vaccine Tracker')
        root.geometry('1000x800')
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=Y)
        mylist = Listbox(root, yscrollcommand=scrollbar.set, width = 150)
        print("\n\n\t\t\t ***Vaccine centre/s found*** ")
        for m in range(0,2):
            playsound('Alarm.mp3')
        webbrowser.open("https://selfregistration.cowin.gov.in/", new=1)
        for i in range(filter_df.shape[0]):
            Data = "Centre Name : {}, Address : {}, Pin :{}, Total dose :{}, Vaccine Type :{}".format(
                filter_df.name.iloc[i], filter_df.address.iloc[i],
                filter_df.pincode.iloc[i], filter_df.available_capacity.iloc[i],
                filter_df.vaccine.iloc[i])
            mylist.insert(END, Data)

        mylist.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=mylist.yview)
        mainloop()


# # Automated

# In[ ]:


elif app_type == "auto":
    while True:
        response = requests.get(URL, headers=header)
        if response.ok:
            response_json = response.json()
            response_df = pd.DataFrame(dict(response_json)['sessions'])
            filter_df = response_df[(response_df.min_age_limit == age)
                                    & (response_df.available_capacity > vaccine_limit)]
            from tkinter import *

            if filter_df.shape[0] > 0:
                root = Tk()
                root.title('CoWIN Vaccine Tracker')
                root.geometry('1000x800')
                scrollbar = Scrollbar(root)
                scrollbar.pack(side=RIGHT, fill=Y)
                mylist = Listbox(root, yscrollcommand=scrollbar.set, width=150)
                for m in range(0, 2):
                    playsound('Alarm.mp3')
                webbrowser.open("https://selfregistration.cowin.gov.in/", new=1)
                for i in range(filter_df.shape[0]):
                    Data = "Centre Name : {}, Address : {}, Pin :{}, Total dose :{}, Vaccine Type :{}".format(
                        filter_df.name.iloc[i], filter_df.address.iloc[i],
                        filter_df.pincode.iloc[i],
                        filter_df.available_capacity.iloc[i],
                        filter_df.vaccine.iloc[i])
                    mylist.insert(END, Data)

                mylist.pack(side=LEFT, fill=BOTH)
                scrollbar.config(command=mylist.yview)
                mainloop()
        time.sleep(300)  # every 5 mins check

