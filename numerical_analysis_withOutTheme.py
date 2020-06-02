import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import numpy as np
import pandas as pd
import tkinter as tk
import requests
import json
import datetime

r = tk.Tk()
r.geometry("1200x600")
r.configure(bg="#464646")  
figure2 = plt.Figure(figsize=(12,6), dpi=100)
ax2 = figure2.add_subplot(111)
figure2.patch.set_facecolor('#464646')

 

def get_country():
    
    country_name = e1.get()
    #print(country_name)
    request = requests.get("https://pomber.github.io/covid19/timeseries.json").text
    data = json.loads(request)
    
    covid_date = []
    covid_cases = []
    covid_deaths = []
    covid_recovered = []
    
    if country_name == "us":
        country_name = country_name.upper()
    else :
        country_name = country_name.capitalize()
    
    for cases_data in data[country_name]:
        date = cases_data["date"]
        cases = cases_data["confirmed"]
        deaths = cases_data["deaths"]
        recovered = cases_data["recovered"]
        
        covid_date.append(date)
        covid_cases.append(cases)
        covid_deaths.append(deaths)
        covid_recovered.append(recovered)
                
        df=pd.DataFrame({'date': covid_date,'cases': covid_cases, 'deaths': covid_deaths, 'recovered': covid_recovered})#, 'recovered': covid_recovered 
        ax2.plot(covid_date,covid_cases)
        ax2.fill_between(covid_date , covid_cases, covid_deaths, facecolor="pink",color='pink') # Transparency of the fill
        ax2.fill_between(covid_date , covid_deaths,covid_recovered, facecolor="#58cced",color='#58cced') # Transparency of the fill
        ax2.fill_between(covid_date , covid_deaths,0, facecolor="coral",color='coral') # Transparency of the fill
        
        df2=pd.DataFrame({'country': country_name,'dates': covid_date,'cases': covid_cases,'deaths': covid_deaths})
        df2.to_excel(country_name+".xlsx",sheet_name='sheet1',index=False)
        
    var = tk.StringVar()
    label = tk.Message( r, textvariable=var ,width=200,bg="#464646",fg="#9199a1")
    
    var.set("\nCOVID-19 Graphical Representation\ntotal cases in "+country_name+" : "+str(cases)+"\ntotal deaths : "+str(deaths)+"\ntotal recovered : "+str(recovered))
    label.pack()
        
      
        
    rightframe = tk.Frame(r)
    rightframe.pack(side = "left")
    
    line2 = FigureCanvasTkAgg(figure2, rightframe)
    line2.get_tk_widget().pack()
    df.plot(kind='line',ax=ax2,rot=90)
    
    ax2.set_title("\nCOVID-19 Graphical Representation", loc='center', fontsize=16, fontweight=0, color='#9199a1')
    
   
    
    
frame = tk.Frame(r)
frame.pack()
bottomframe = tk.Frame(r)
bottomframe.pack(side = "left")
e1 = tk.Entry(frame)
e1.grid(row=0, column=0)
search = tk.Button(frame, text='search', width=10, command=get_country)
search.grid(row=0, column=2)

r.mainloop()