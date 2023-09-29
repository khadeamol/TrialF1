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


year, gp, session = 2023, 'Monaco', 'R'
quali = f1.get_session(year, gp, session)

quali.load()

def calcDelta(quali, driver_1, driver_2):
    laps_driver_1 = quali.laps.pick_driver(driver_1)
    laps_driver_2 = quali.laps.pick_driver(driver_2)
    fastest_driver_1 = laps_driver_1.pick_fastest()
    fastest_driver_2 = laps_driver_2.pick_fastest()

    telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
    telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

    team_driver_1 = fastest_driver_1['Team']
    team_driver_2 = fastest_driver_2['Team']

    from fastf1 import utils

    delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1,\
                                                    fastest_driver_2)
    return [delta_time, ref_tel]

def timeDeltaViz(quali, delta_time, ref_tel, driver_1, driver_2):
    plot_size = [14,3]
    plt.rcParams['figure.figsize'] = plot_size
    plot_ratios = [1]
    fix, ax = plt.subplots(1, gridspec_kw = {'height_ratios': plot_ratios})
    plot_title = f"{quali.event.year} {quali.event.EventName} - {quali.name} - {driver_1} VS {driver_2}"
    ax.title.set_text(plot_title)
    ax.plot(ref_tel['Distance'], delta_time)
    ax.axhline(0)
    ax.set(ylabel = f"Gap to {driver_2}(s)")
    plt.savefig("plt1.png")
    return plt

# setCanvas(quali, driver_1, driver_2)
# timeDelta(delta_time, driver_1, driver_2)