from flask import Flask, flash, request, url_for, redirect, render_template, jsonify
import pandas as pd
import pickle, json
import numpy as np
from json2html import *
import jsonpickle
import os

import fastf1 as f1
from matplotlib import pyplot as plt
from fastf1 import plotting
from fastf1.ergast import Ergast 

import time

os.system("driverViz.py")
from driverViz import timeDeltaViz, calcDelta

app = Flask(__name__)
config = {
    "DEBUG": True
}
app.config.from_mapping(config)

@app.route('/')
def home():
    print("We are home now.")
    return render_template("yearSelection.html")
    
@app.route('/yearSelection', methods = ['POST'])
def raceResults():
    if request.method == "POST":

        f1.Cache.enable_cache("cache")
        
        
        yearSel = request.form.get("year")
        raceSel = request.form.get("race")
        sessionType = request.form.get("sessionType")
        
        
        eventObj = f1.get_event(int(yearSel), raceSel)
        eventName = eventObj.OfficialEventName
        
        sessionObj = f1.get_session(int(yearSel), str(eventName), sessionType)
        sessionObj.load(telemetry = False)
        sessionResults = sessionObj.results
        
        
        resultDF = pd.DataFrame(sessionResults)

        driverList = pd.DataFrame(resultDF['FullName'], columns = ["FullName"])


        qualiColList = ['FullName','TeamName',
        'Position', 'Q1', 'Q2', 'Q3', 'Time']
        
        raceColList = ['FullName', 'TeamName',
        'Position', 'ClassifiedPosition', 'Time', 'Status', 'Points']
        

        ################################################################################

        # vizCreate(sessionObj, 'VER', 'PER')
        ################################################################################
        if sessionType == 'Q':
            resultDF = resultDF[qualiColList]
            resultDF = resultDF.rename(columns = {'FullName': 'Full Name', 'TeamName': 'Team Name', 'ClassifiedPosition': 'Classified Position'})
            sessionTypeFull = 'Qualifying'
        
        elif sessionType == 'R':
            resultDF = resultDF[raceColList]
            resultDF = resultDF.rename(columns = {'FullName': 'Full Name', 'TeamName': 'Team Name', 'ClassifiedPosition': 'Classified Position'})
            sessionTypeFull = 'Race'

        return render_template("raceResults.html", data1 = driverList, eventName = eventName,raceResults = resultDF.to_html(), yearSel = yearSel, raceSel = "xx", sessionType = sessionTypeFull)

def driverFocus(resultDF):
    colList = ['FullName', 'DriverNumber']
    driverList = resultDF[colList]
    
    return createListHTML(driverList)

def createListHTML(refDF):
    st = ""
    for i in range(len(refDF)):
        st = st + "<option value = '" + refDF['FullName'][i] + "'>" + refDF['FullName'][i] + "</option"
    print(st)
    return st

def vizCreate(quali, driver_1, driver_2):
    delta_time = calcDelta(quali, driver_1, driver_2)[0]
    ref_tel = calcDelta(quali, driver_1, driver_2)[1]
    x = timeDeltaViz(quali, delta_time, ref_tel, driver_1, driver_2)
    return x


#  <option value ='Bahrain Grand Prix'>Bahrain Grand Prix</option>



    
