import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import json

# Page configuration
st.set_page_config(
    page_title="Racing Lap Simulator",
    page_icon="🏎️",
    layout="wide"
)

# Constants
GRAVITY = 9.81
AIR_DENSITY = 1.225

class Car:
    def __init__(self, name, mass, power, drag_coef, downforce_coef, tire_grip, rolling_resistance, frontal_area, color, category):
        self.name = name
        self.mass = mass  # kg
        self.power = power  # kW
        self.drag_coef = drag_coef
        self.downforce_coef = downforce_coef
        self.tire_grip = tire_grip
        self.rolling_resistance = rolling_resistance
        self.frontal_area = frontal_area  # m²
        self.color = color
        self.category = category

class Track:
    def __init__(self, name, segments, country, length_km, coordinates=None):
        self.name = name
        self.segments = segments
        self.total_length = sum(seg['length'] for seg in segments)
        self.country = country
        self.length_km = length_km
        self.coordinates = coordinates or []

def create_car_database():
    """Create database of different car types with realistic specifications"""
    cars = {
        # F1 Teams (2023/2024 season)
        "Red Bull RB19": Car(
            name="Red Bull RB19",
            mass=798, power=760, drag_coef=0.85, downforce_coef=3.2, 
            tire_grip=1.9, rolling_resistance=0.015, frontal_area=1.5,
            color="#1E41FF", category="Formula 1"
        ),
        "Ferrari SF-23": Car(
            name="Ferrari SF-23",
            mass=798, power=755, drag_coef=0.88, downforce_coef=3.1,
            tire_grip=1.85, rolling_resistance=0.015, frontal_area=1.5,
            color="#DC143C", category="Formula 1"
        ),
        "Mercedes W14": Car(
            name="Mercedes W14",
            mass=798, power=750, drag_coef=0.92, downforce_coef=2.9,
            tire_grip=1.8, rolling_resistance=0.015, frontal_area=1.5,
            color="#00D2BE", category="Formula 1"
        ),
        "McLaren MCL60": Car(
            name="McLaren MCL60",
            mass=798, power=745, drag_coef=0.89, downforce_coef=3.0,
            tire_grip=1.82, rolling_resistance=0.015, frontal_area=1.5,
            color="#FF8700", category="Formula 1"
        ),
        "Aston Martin AMR23": Car(
            name="Aston Martin AMR23",
            mass=798, power=740, drag_coef=0.90, downforce_coef=2.95,
            tire_grip=1.78, rolling_resistance=0.015, frontal_area=1.5,
            color="#006F62", category="Formula 1"
        ),
        "Alpine A523": Car(
            name="Alpine A523",
            mass=798, power=735, drag_coef=0.93, downforce_coef=2.8,
            tire_grip=1.75, rolling_resistance=0.015, frontal_area=1.5,
            color="#0090FF", category="Formula 1"
        ),
        
        # GT3 Cars
        "Porsche 911 GT3 R": Car(
            name="Porsche 911 GT3 R",
            mass=1300, power=410, drag_coef=0.65, downforce_coef=1.8,
            tire_grip=1.4, rolling_resistance=0.018, frontal_area=2.0,
            color="#FFD700", category="GT3"
        ),
        "BMW M4 GT3": Car(
            name="BMW M4 GT3",
            mass=1320, power=415, drag_coef=0.68, downforce_coef=1.7,
            tire_grip=1.38, rolling_resistance=0.018, frontal_area=2.1,
            color="#0066CC", category="GT3"
        ),
        "Mercedes-AMG GT3": Car(
            name="Mercedes-AMG GT3",
            mass=1310, power=420, drag_coef=0.66, downforce_coef=1.75,
            tire_grip=1.42, rolling_resistance=0.018, frontal_area=2.0,
            color="#C0C0C0", category="GT3"
        ),
        "Ferrari 488 GT3": Car(
            name="Ferrari 488 GT3",
            mass=1315, power=425, drag_coef=0.64, downforce_coef=1.9,
            tire_grip=1.45, rolling_resistance=0.018, frontal_area=1.95,
            color="#DC143C", category="GT3"
        ),
        "Audi R8 LMS GT3": Car(
            name="Audi R8 LMS GT3",
            mass=1325, power=418, drag_coef=0.67, downforce_coef=1.72,
            tire_grip=1.40, rolling_resistance=0.018, frontal_area=2.05,
            color="#FF0000", category="GT3"
        ),
        
        # LMP1/Hypercar
        "Toyota GR010 Hybrid": Car(
            name="Toyota GR010 Hybrid",
            mass=1030, power=680, drag_coef=0.55, downforce_coef=2.5,
            tire_grip=1.65, rolling_resistance=0.016, frontal_area=1.8,
            color="#EB0A1E", category="LMP1/Hypercar"
        ),
        "Ferrari 499P": Car(
            name="Ferrari 499P",
            mass=1030, power=675, drag_coef=0.57, downforce_coef=2.4,
            tire_grip=1.62, rolling_resistance=0.016, frontal_area=1.8,
            color="#DC143C", category="LMP1/Hypercar"
        ),
        
        # Hypercars
        "Lamborghini Huracán": Car(
            name="Lamborghini Huracán",
            mass=1422, power=470, drag_coef=0.39, downforce_coef=0.3,
            tire_grip=1.2, rolling_resistance=0.012, frontal_area=2.1,
            color="#32CD32", category="Hypercar"
        ),
        "McLaren 720S": Car(
            name="McLaren 720S",
            mass=1468, power=530, drag_coef=0.32, downforce_coef=0.4,
            tire_grip=1.25, rolling_resistance=0.011, frontal_area=2.0,
            color="#FF8C00", category="Hypercar"
        ),
        "Ferrari F8 Tributo": Car(
            name="Ferrari F8 Tributo",
            mass=1435, power=530, drag_coef=0.34, downforce_coef=0.35,
            tire_grip=1.22, rolling_resistance=0.012, frontal_area=2.05,
            color="#B22222", category="Hypercar"
        ),
        "Porsche 911 Turbo S": Car(
            name="Porsche 911 Turbo S",
            mass=1640, power=478, drag_coef=0.35, downforce_coef=0.25,
            tire_grip=1.18, rolling_resistance=0.012, frontal_area=2.15,
            color="#FFFF00", category="Hypercar"
        ),
        
        # Sports Cars
        "BMW M3 Competition": Car(
            name="BMW M3 Competition",
            mass=1730, power=375, drag_coef=0.35, downforce_coef=0.1,
            tire_grip=1.1, rolling_resistance=0.014, frontal_area=2.3,
            color="#4169E1", category="Sports Car"
        ),
        "Audi RS6": Car(
            name="Audi RS6",
            mass=2040, power=441, drag_coef=0.32, downforce_coef=0.05,
            tire_grip=1.05, rolling_resistance=0.015, frontal_area=2.4,
            color="#800080", category="Sports Car"
        ),
        "Mercedes-AMG C63": Car(
            name="Mercedes-AMG C63",
            mass=1715, power=375, drag_coef=0.34, downforce_coef=0.08,
            tire_grip=1.08, rolling_resistance=0.014, frontal_area=2.25,
            color="#2F4F4F", category="Sports Car"
        )
    }
    
    return cars

def create_tracks():
    """Create more realistic F1 track layouts with detailed coordinates"""
    tracks = {
        "Monza": Track(
            name="Monza",
            country="Italy",
            length_km=5.793,
            coordinates=[
                # Real GPS-inspired coordinates scaled for visualization
                (0, 0), (1100, 20), (1150, -10), (1200, -50), (1220, -30), (1300, 0),
                (2200, 50), (2250, 20), (2300, -20), (2320, -40), (2400, -20), (2500, 10),
                (2600, -30), (2650, -60), (2700, -40), (2800, -10), (2900, -40),
                (2950, -80), (3000, -120), (3100, -140), (3200, -120), (3300, -80),
                (3400, -40), (3500, -10), (3600, 20), (3700, 50), (3800, 30),
                (3850, 0), (3900, -30), (3950, -50), (4000, -30), (4100, 0),
                (4200, 40), (4300, 80), (4400, 100), (4500, 80), (4600, 40),
                (4700, 0), (4750, -40), (4800, -80), (4750, -120), (4700, -100),
                (4600, -80), (4500, -60), (4400, -40), (4300, -20), (4200, 0),
                (4100, 20), (4000, 40), (3900, 20), (3800, 0), (3700, -20),
                (3600, -40), (3500, -20), (3400, 0), (3300, 20), (3200, 40),
                (3100, 20), (3000, 0), (2900, -20), (2800, 0), (2700, 20),
                (2600, 40), (2500, 60), (2400, 40), (2300, 20), (2200, 0),
                (2100, -20), (2000, 0), (1900, 20), (1800, 0), (1700, -20),
                (1600, 0), (1500, 20), (1400, 0), (1300, -20), (1200, 0),
                (1100, 20), (1000, 0), (900, -20), (800, 0), (700, 20),
                (600, 0), (500, -20), (400, 0), (300, 20), (200, 0), (100, -20), (0, 0)
            ],
            segments=[
                {"type": "straight", "length": 1142, "name": "Main Straight", "drs": True},
                {"type": "corner", "length": 85, "radius": 85, "angle": 75, "name": "Turn 1 - Prima Variante"},
                {"type": "straight", "length": 175, "name": "Approach to T2"},
                {"type": "corner", "length": 95, "radius": 95, "angle": 65, "name": "Turn 2 - Prima Variante"},
                {"type": "straight", "length": 1090, "name": "Back Straight", "drs": True},
                {"type": "corner", "length": 120, "radius": 45, "angle": 85, "name": "Turn 3 - Seconda Variante"},
                {"type": "straight", "length": 55, "name": "Chicane Link"},
                {"type": "corner", "length": 130, "radius": 50, "angle": 75, "name": "Turn 4 - Seconda Variante"},
                {"type": "straight", "length": 290, "name": "Approach to Lesmo"},
                {"type": "corner", "length": 140, "radius": 65, "angle": 90, "name": "Turn 5 - Lesmo 1"},
                {"type": "straight", "length": 185, "name": "Between Lesmos"},
                {"type": "corner", "length": 155, "radius": 70, "angle": 85, "name": "Turn 6 - Lesmo 2"},
                {"type": "straight", "length": 320, "name": "Approach to Ascari"},
                {"type": "corner", "length": 110, "radius": 55, "angle": 70, "name": "Turn 7 - Ascari 1"},
                {"type": "corner", "length": 125, "radius": 45, "angle": 80, "name": "Turn 8 - Ascari 2"},
                {"type": "corner", "length": 95, "radius": 65, "angle": 60, "name": "Turn 9 - Ascari 3"},
                {"type": "straight", "length": 415, "name": "Approach to Parabolica"},
                {"type": "corner", "length": 320, "radius": 165, "angle": 180, "name": "Turn 10/11 - Parabolica"},
                {"type": "straight", "length": 580, "name": "Start/Finish Straight"}
            ]
        ),
        
        "Silverstone": Track(
            name="Silverstone",
            country="Great Britain",
            length_km=5.891,
            coordinates=[
                (0, 0), (200, 10), (400, 25), (600, 40), (800, 60), (1000, 80),
                (1200, 100), (1400, 120), (1600, 140), (1800, 160), (2000, 180),
                (2200, 200), (2400, 220), (2600, 240), (2800, 250), (3000, 260),
                (3200, 270), (3400, 280), (3600, 290), (3800, 295), (4000, 300),
                (4200, 295), (4400, 285), (4600, 270), (4800, 250), (5000, 225),
                (5200, 195), (5400, 160), (5600, 120), (5800, 75), (6000, 25),
                (6200, -25), (6400, -75), (6600, -125), (6800, -175), (7000, -225),
                (7200, -275), (7400, -320), (7600, -360), (7800, -395), (8000, -425),
                (8200, -450), (8400, -470), (8600, -485), (8800, -495), (9000, -500),
                (9200, -495), (9400, -485), (9600, -470), (9800, -450), (10000, -425),
                (10200, -395), (10400, -360), (10600, -320), (10800, -275), (11000, -225),
                (11200, -175), (11400, -125), (11600, -75), (11800, -25), (12000, 25),
                (12200, 75), (12400, 120), (12600, 160), (12800, 195), (13000, 225),
                (13200, 250), (13400, 270), (13600, 285), (13800, 295), (14000, 300),
                (14200, 295), (14400, 285), (14600, 270), (14800, 250), (15000, 225),
                (15200, 195), (15400, 160), (15600, 120), (15800, 75), (16000, 25),
                (16200, -25), (16400, -75), (16600, -125), (16800, -175), (17000, -200),
                (17200, -180), (17400, -150), (17600, -110), (17800, -60), (18000, 0),
                (18200, 60), (18400, 110), (18600, 150), (18800, 180), (19000, 200),
                (19200, 180), (19400, 150), (19600, 110), (19800, 60), (20000, 0),
                (20200, -60), (20400, -110), (20600, -150), (20800, -180), (21000, -200),
                (20800, -220), (20600, -200), (20400, -170), (20200, -130), (20000, -80),
                (19800, -20), (19600, 40), (19400, 90), (19200, 130), (19000, 160),
                (18800, 180), (18600, 190), (18400, 185), (18200, 170), (18000, 145),
                (17800, 110), (17600, 65), (17400, 10), (17200, -45), (17000, -90),
                (16800, -125), (16600, -150), (16400, -165), (16200, -170), (16000, -165),
                (15800, -150), (15600, -125), (15400, -90), (15200, -45), (15000, 10),
                (14800, 65), (14600, 110), (14400, 145), (14200, 170), (14000, 185),
                (13800, 190), (13600, 180), (13400, 160), (13200, 130), (13000, 90),
                (12800, 40), (12600, -20), (12400, -80), (12200, -130), (12000, -170),
                (11800, -200), (11600, -220), (11400, -230), (11200, -225), (11000, -210),
                (10800, -185), (10600, -150), (10400, -105), (10200, -50), (10000, 15),
                (9800, 80), (9600, 135), (9400, 180), (9200, 215), (9000, 240),
                (8800, 255), (8600, 260), (8400, 255), (8200, 240), (8000, 215),
                (7800, 180), (7600, 135), (7400, 80), (7200, 15), (7000, -50),
                (6800, -105), (6600, -150), (6400, -185), (6200, -210), (6000, -225),
                (5800, -230), (5600, -220), (5400, -200), (5200, -170), (5000, -130),
                (4800, -80), (4600, -20), (4400, 40), (4200, 90), (4000, 130),
                (3800, 160), (3600, 180), (3400, 190), (3200, 185), (3000, 170),
                (2800, 145), (2600, 110), (2400, 65), (2200, 10), (2000, -45),
                (1800, -90), (1600, -125), (1400, -150), (1200, -165), (1000, -170),
                (800, -165), (600, -150), (400, -125), (200, -90), (0, -45), (0, 0)
            ],
            segments=[
                {"type": "straight", "length": 265, "name": "Wellington Straight"},
                {"type": "corner", "length": 95, "radius": 150, "angle": 35, "name": "Turn 1 - Abbey"},
                {"type": "straight", "length": 180, "name": "National Straight"},
                {"type": "corner", "length": 110, "radius": 95, "angle": 65, "name": "Turn 2 - Farm Curve"},
                {"type": "straight", "length": 220, "name": "Approach to Village"},
                {"type": "corner", "length": 85, "radius": 40, "angle": 90, "name": "Turn 3 - Village"},
                {"type": "straight", "length": 155, "name": "The Loop Straight"},
                {"type": "corner", "length": 140, "radius": 120, "angle": 75, "name": "Turn 4 - The Loop"},
                {"type": "straight", "length": 95, "name": "Short Straight"},
                {"type": "corner", "length": 120, "radius": 85, "angle": 80, "name": "Turn 5 - Aintree"},
                {"type": "straight", "length": 310, "name": "Wellington Straight"},
                {"type": "corner", "length": 165, "radius": 180, "angle": 55, "name": "Turn 6 - Brooklands"},
                {"type": "straight", "length": 240, "name": "Luffield Straight"},
                {"type": "corner", "length": 145, "radius": 95, "angle": 75, "name": "Turn 7 - Luffield"},
                {"type": "straight", "length": 185, "name": "Woodcote Straight"},
                {"type": "corner", "length": 125, "radius": 110, "angle": 65, "name": "Turn 8 - Woodcote"},
                {"type": "straight", "length": 780, "name": "Copse Straight"},
                {"type": "corner", "length": 110, "radius": 125, "angle": 70, "name": "Turn 9 - Copse"},
                {"type": "straight", "length": 345, "name": "Maggotts Straight", "drs": True},
                {"type": "corner", "length": 135, "radius": 280, "angle": 45, "name": "Turn 10 - Maggotts"},
                {"type": "corner", "length": 125, "radius": 195, "angle": 55, "name": "Turn 11 - Becketts"},
                {"type": "corner", "length": 145, "radius": 75, "angle": 85, "name": "Turn 12 - Chapel"},
                {"type": "straight", "length": 910, "name": "Hangar Straight", "drs": True},
                {"type": "corner", "length": 155, "radius": 110, "angle": 75, "name": "Turn 13 - Stowe"},
                {"type": "straight", "length": 265, "name": "Vale Straight"},
                {"type": "corner", "length": 125, "radius": 85, "angle": 80, "name": "Turn 14 - Vale"},
                {"type": "corner", "length": 95, "radius": 65, "angle": 70, "name": "Turn 15 - Club"},
                {"type": "straight", "length": 518, "name": "Start/Finish Straight"}
            ]
        ),
        
        "Monaco": Track(
            name="Monaco",
            country="Monaco", 
            length_km=3.337,
            coordinates=[
                (0, 0), (50, 5), (100, 15), (145, 30), (180, 50), (200, 75),
                (210, 100), (205, 125), (185, 145), (155, 160), (120, 170),
                (80, 175), (40, 175), (0, 170), (-35, 160), (-65, 145),
                (-90, 125), (-110, 100), (-125, 75), (-135, 50), (-140, 25),
                (-140, 0), (-135, -25), (-125, -50), (-110, -75), (-90, -95),
                (-65, -110), (-35, -120), (0, -125), (40, -125), (80, -120),
                (120, -110), (155, -95), (185, -75), (205, -50), (210, -25),
                (200, 0), (180, 25), (145, 45), (100, 60), (50, 70), (0, 75),
                (-50, 75), (-95, 70), (-135, 60), (-170, 45), (-195, 25),
                (-210, 0), (-215, -25), (-210, -50), (-195, -75), (-170, -95),
                (-135, -110), (-95, -120), (-50, -125), (0, -125), (50, -120),
                (95, -110), (135, -95), (170, -75), (195, -50), (210, -25),
                (215, 0), (210, 25), (195, 50), (170, 70), (135, 85),
                (95, 95), (50, 100), (0, 100), (-50, 95), (-95, 85),
                (-135, 70), (-170, 50), (-195, 25), (-210, 0), (-215, -25),
                (-210, -50), (-195, -75), (-170, -95), (-135, -110), (-95, -120),
                (-50, -125), (0, -125), (50, -120), (95, -110), (135, -95),
                (170, -75), (195, -50), (210, -25), (215, 0), (210, 25),
                (195, 50), (170, 70), (135, 85), (95, 95), (50, 100),
                (0, 100), (-50, 95), (-95, 85), (-135, 70), (-170, 50),
                (-195, 25), (-210, 0)
            ],
            segments=[
                {"type": "straight", "length": 185, "name": "Start/Finish Straight"},
                {"type": "corner", "length": 95, "radius": 35, "angle": 85, "name": "Turn 1 - Sainte Devote"},
                {"type": "straight", "length": 245, "name": "Beau Rivage"},
                {"type": "corner", "length": 125, "radius": 65, "angle": 70, "name": "Turn 2 - Massenet"},
                {"type": "straight", "length": 85, "name": "Casino Straight"},
                {"type": "corner", "length": 155, "radius": 45, "angle": 95, "name": "Turn 3 - Casino"},
                {"type": "straight", "length": 115, "name": "Mirabeau Straight"},
                {"type": "corner", "length": 85, "radius": 55, "angle": 75, "name": "Turn 4 - Mirabeau"},
                {"type": "straight", "length": 65, "name": "Fairmont Straight"},
                {"type": "corner", "length": 125, "radius": 18, "angle": 180, "name": "Turn 5 - Grand Hotel Hairpin"},
                {"type": "straight", "length": 155, "name": "Portier Straight"},
                {"type": "corner", "length": 85, "radius": 45, "angle": 65, "name": "Turn 6 - Portier"},
                {"type": "straight", "length": 245, "name": "Tunnel Straight"},
                {"type": "corner", "length": 95, "radius": 85, "angle": 55, "name": "Turn 7 - Nouvelle Chicane"},
                {"type": "corner", "length": 75, "radius": 75, "angle": 45, "name": "Turn 8 - Nouvelle Chicane"},
                {"type": "straight", "length": 125, "name": "Tabac Straight"},
                {"type": "corner", "length": 115, "radius": 65, "angle": 80, "name": "Turn 9 - Tabac"},
                {"type": "straight", "length": 95, "name": "Swimming Pool Straight"},
                {"type": "corner", "length": 85, "radius": 25, "angle": 90, "name": "Turn 10 - Swimming Pool"},
                {"type": "corner", "length": 65, "radius": 30, "angle": 75, "name": "Turn 11 - Swimming Pool"},
                {"type": "corner", "length": 95, "radius": 35, "angle": 85, "name": "Turn 12 - Swimming Pool"},
                {"type": "straight", "length": 155, "name": "La Rascasse Straight"},
                {"type": "corner", "length": 125, "radius": 28, "angle": 110, "name": "Turn 13 - La Rascasse"},
                {"type": "straight", "length": 85, "name": "Anthony Noghes Straight"},
                {"type": "corner", "length": 155, "radius": 55, "angle": 95, "name": "Turn 14 - Anthony Noghes"},
                {"type": "straight", "length": 245, "name": "Final Straight"}
            ]
        ),
        
        "Spa-Francorchamps": Track(
            name="Spa-Francorchamps",
            country="Belgium",
            length_km=7.004,
            coordinates=[
                (0, 0), (300, 20), (600, 45), (900, 75), (1200, 110), (1500, 150),
                (1800, 195), (2100, 245), (2400, 300), (2700, 360), (3000, 425),
                (3300, 495), (3600, 570), (3900, 650), (4200, 735), (4500, 825),
                (4800, 920), (5100, 1020), (5400, 1125), (5700, 1235), (6000, 1350),
                (6300, 1470), (6600, 1595), (6900, 1725), (7200, 1860), (7500, 2000),
                (7800, 2145), (8100, 2295), (8400, 2450), (8700, 2610), (9000, 2775),
                (9300, 2945), (9600, 3120), (9900, 3300), (10200, 3485), (10500, 3675),
                (10800, 3870), (11100, 4070), (11400, 4275), (11700, 4485), (12000, 4700),
                (12300, 4920), (12600, 5145), (12900, 5375), (13200, 5610), (13500, 5850),
                (13800, 6095), (14100, 6345), (14400, 6600), (14700, 6860), (15000, 7125),
                (15300, 7395), (15600, 7670), (15900, 7950), (16200, 8235), (16500, 8525),
                (16800, 8820), (17100, 9120), (17400, 9425), (17700, 9735), (18000, 10050),
                (17700, 10365), (17400, 10675), (17100, 10980), (16800, 11280), (16500, 11575),
                (16200, 11865), (15900, 12150), (15600, 12430), (15300, 12705), (15000, 12975),
                (14700, 13240), (14400, 13500), (14100, 13755), (13800, 14005), (13500, 14250),
                (13200, 14490), (12900, 14725), (12600, 14955), (12300, 15180), (12000, 15400),
                (11700, 15615), (11400, 15825), (11100, 16030), (10800, 16230), (10500, 16425),
                (10200, 16615), (9900, 16800), (9600, 16980), (9300, 17155), (9000, 17325),
                (8700, 17490), (8400, 17650), (8100, 17805), (7800, 17955), (7500, 18100),
                (7200, 18240), (6900, 18375), (6600, 18505), (6300, 18630), (6000, 18750),
                (5700, 18865), (5400, 18975), (5100, 19080), (4800, 19180), (4500, 19275),
                (4200, 19365), (3900, 19450), (3600, 19530), (3300, 19605), (3000, 19675),
                (2700, 19740), (2400, 19800), (2100, 19855), (1800, 19905), (1500, 19950),
                (1200, 19990), (900, 20025), (600, 20055), (300, 20080), (0, 20100),
                (-300, 20080), (-600, 20055), (-900, 20025), (-1200, 19990), (-1500, 19950),
                (-1800, 19905), (-2100, 19855), (-2400, 19800), (-2700, 19740), (-3000, 19675),
                (-3300, 19605), (-3600, 19530), (-3900, 19450), (-4200, 19365), (-4500, 19275),
                (-4800, 19180), (-5100, 19080), (-5400, 18975), (-5700, 18865), (-6000, 18750),
                (-6300, 18630), (-6600, 18505), (-6900, 18375), (-7200, 18240), (-7500, 18100),
                (-7800, 17955), (-8100, 17805), (-8400, 17650), (-8700, 17490), (-9000, 17325),
                (-9300, 17155), (-9600, 16980), (-9900, 16800), (-10200, 16615), (-10500, 16425),
                (-10800, 16230), (-11100, 16030), (-11400, 15825), (-11700, 15615), (-12000, 15400),
                (-12300, 15180), (-12600, 14955), (-12900, 14725), (-13200, 14490), (-13500, 14250),
                (-13800, 14005), (-14100, 13755), (-14400, 13500), (-14700, 13240), (-15000, 12975),
                (-15300, 12705), (-15600, 12430), (-15900, 12150), (-16200, 11865), (-16500, 11575),
                (-16800, 11280), (-17100, 10980), (-17400, 10675), (-17700, 10365), (-18000, 10050),
                (-17700, 9735), (-17400, 9425), (-17100, 9120), (-16800, 8820), (-16500, 8525),
                (-16200, 8235), (-15900, 7950), (-15600, 7670), (-15300, 7395), (-15000, 7125),
                (-14700, 6860), (-14400, 6600), (-14100, 6345), (-13800, 6095), (-13500, 5850),
                (-13200, 5610), (-12900, 5375), (-12600, 5145), (-12300, 4920), (-12000, 4700),
                (-11700, 4485), (-11400, 4275), (-11100, 4070), (-10800, 3870), (-10500, 3675),
                (-10200, 3485), (-9900, 3300), (-9600, 3120), (-9300, 2945), (-9000, 2775),
                (-8700, 2610), (-8400, 2450), (-8100, 2295), (-7800, 2145), (-7500, 2000),
                (-7200, 1860), (-6900, 1725), (-6600, 1595), (-6300, 1470), (-6000, 1350),
                (-5700, 1235), (-5400, 1125), (-5100, 1020), (-4800, 920), (-4500, 825),
                (-4200, 735), (-3900, 650), (-3600, 570), (-3300, 495), (-3000, 425),
                (-2700, 360), (-2400, 300), (-2100, 245), (-1800, 195), (-1500, 150),
                (-1200, 110), (-900, 75), (-600, 45), (-300, 20), (0, 0)
            ],
            segments=[
                {"type": "straight", "length": 700, "name": "Start/Finish Straight"},
                {"type": "corner", "length": 120, "radius": 35, "angle": 90, "name": "Turn 1 - La Source"},
                {"type": "straight", "length": 180, "name": "Raidillon Approach"},
                {"type": "corner", "length": 85, "radius": 250, "angle": 35, "name": "Turn 2 - Eau Rouge"},
                {"type": "corner", "length": 140, "radius": 180, "angle": 45, "name": "Turn 3 - Raidillon"},
                {"type": "straight", "length": 1800, "name": "Kemmel Straight", "drs": True},
                {"type": "corner", "length": 160, "radius": 45, "angle": 110, "name": "Turn 4 - Les Combes"},
                {"type": "straight", "length": 280, "name": "Approach to Malmedy"},
                {"type": "corner", "length": 95, "radius": 65, "angle": 75, "name": "Turn 5 - Malmedy"},
                {"type": "straight", "length": 420, "name": "Sector 2 Straight"},
                {"type": "corner", "length": 125, "radius": 85, "angle": 80, "name": "Turn 6 - Rivage"},
                {"type": "straight", "length": 190, "name": "Approach to Pouhon"},
                {"type": "corner", "length": 180, "radius": 120, "angle": 95, "name": "Turn 7 - Pouhon"},
                {"type": "straight", "length": 320, "name": "Sector 2 Mid"},
                {"type": "corner", "length": 110, "radius": 75, "angle": 65, "name": "Turn 8 - Fagnes"},
                {"type": "straight", "length": 280, "name": "Approach to Stavelot"},
                {"type": "corner", "length": 95, "radius": 55, "angle": 85, "name": "Turn 9 - Stavelot"},
                {"type": "straight", "length": 150, "name": "Paul Frere Straight"},
                {"type": "corner", "length": 125, "radius": 95, "angle": 70, "name": "Turn 10 - Paul Frere"},
                {"type": "straight", "length": 480, "name": "Blanchimont Straight"},
                {"type": "corner", "length": 220, "radius": 350, "angle": 55, "name": "Turn 11 - Blanchimont"},
                {"type": "straight", "length": 370, "name": "Final Straight"},
                {"type": "corner", "length": 85, "radius": 25, "angle": 120, "name": "Turn 12 - Bus Stop Chicane"},
                {"type": "corner", "length": 65, "radius": 30, "angle": 100, "name": "Turn 13 - Bus Stop Exit"},
                {"type": "straight", "length": 285, "name": "Start/Finish Approach"}
            ]
        ),
        
        "Suzuka": Track(
            name="Suzuka",
            country="Japan",
            length_km=5.807,
            coordinates=[
                (0, 0), (250, 15), (500, 35), (750, 60), (1000, 90), (1250, 125),
                (1500, 165), (1750, 210), (2000, 260), (2250, 315), (2500, 375),
                (2750, 440), (3000, 510), (3250, 585), (3500, 665), (3750, 750),
                (4000, 840), (4250, 935), (4500, 1035), (4750, 1140), (5000, 1250),
                (5250, 1365), (5500, 1485), (5750, 1610), (6000, 1740), (6250, 1875),
                (6500, 2015), (6750, 2160), (7000, 2310), (7250, 2465), (7500, 2625),
                (7750, 2790), (8000, 2960), (8250, 3135), (8500, 3315), (8750, 3500),
                (9000, 3690), (9250, 3885), (9500, 4085), (9750, 4290), (10000, 4500),
                (10250, 4715), (10500, 4935), (10750, 5160), (11000, 5390), (11250, 5625),
                (11500, 5865), (11750, 6110), (12000, 6360), (12250, 6615), (12500, 6875),
                (12750, 7140), (13000, 7410), (13250, 7685), (13500, 7965), (13750, 8250),
                (14000, 8540), (14250, 8835), (14500, 9135), (14750, 9440), (15000, 9750),
                (14750, 10060), (14500, 10365), (14250, 10665), (14000, 10960), (13750, 11250),
                (13500, 11535), (13250, 11815), (13000, 12090), (12750, 12360), (12500, 12625),
                (12250, 12885), (12000, 13140), (11750, 13390), (11500, 13635), (11250, 13875),
                (11000, 14110), (10750, 14340), (10500, 14565), (10250, 14785), (10000, 15000),
                (9750, 15210), (9500, 15415), (9250, 15615), (9000, 15810), (8750, 16000),
                (8500, 16185), (8250, 16365), (8000, 16540), (7750, 16710), (7500, 16875),
                (7250, 17035), (7000, 17190), (6750, 17340), (6500, 17485), (6250, 17625),
                (6000, 17760), (5750, 17890), (5500, 18015), (5250, 18135), (5000, 18250),
                (4750, 18360), (4500, 18465), (4250, 18565), (4000, 18660), (3750, 18750),
                (3500, 18835), (3250, 18915), (3000, 18990), (2750, 19060), (2500, 19125),
                (2250, 19185), (2000, 19240), (1750, 19290), (1500, 19335), (1250, 19375),
                (1000, 19410), (750, 19440), (500, 19465), (250, 19485), (0, 19500),
                (-250, 19485), (-500, 19465), (-750, 19440), (-1000, 19410), (-1250, 19375),
                (-1500, 19335), (-1750, 19290), (-2000, 19240), (-2250, 19185), (-2500, 19125),
                (-2750, 19060), (-3000, 18990), (-3250, 18915), (-3500, 18835), (-3750, 18750),
                (-4000, 18660), (-4250, 18565), (-4500, 18465), (-4750, 18360), (-5000, 18250),
                (-5250, 18135), (-5500, 18015), (-5750, 17890), (-6000, 17760), (-6250, 17625),
                (-6500, 17485), (-6750, 17340), (-7000, 17190), (-7250, 17035), (-7500, 16875),
                (-7750, 16710), (-8000, 16540), (-8250, 16365), (-8500, 16185), (-8750, 16000),
                (-9000, 15810), (-9250, 15615), (-9500, 15415), (-9750, 15210), (-10000, 15000),
                (-10250, 14785), (-10500, 14565), (-10750, 14340), (-11000, 14110), (-11250, 13875),
                (-11500, 13635), (-11750, 13390), (-12000, 13140), (-12250, 12885), (-12500, 12625),
                (-12750, 12360), (-13000, 12090), (-13250, 11815), (-13500, 11535), (-13750, 11250),
                (-14000, 10960), (-14250, 10665), (-14500, 10365), (-14750, 10060), (-15000, 9750),
                (-14750, 9440), (-14500, 9135), (-14250, 8835), (-14000, 8540), (-13750, 8250),
                (-13500, 7965), (-13250, 7685), (-13000, 7410), (-12750, 7140), (-12500, 6875),
                (-12250, 6615), (-12000, 6360), (-11750, 6110), (-11500, 5865), (-11250, 5625),
                (-11000, 5390), (-10750, 5160), (-10500, 4935), (-10250, 4715), (-10000, 4500),
                (-9750, 4290), (-9500, 4085), (-9250, 3885), (-9000, 3690), (-8750, 3500),
                (-8500, 3315), (-8250, 3135), (-8000, 2960), (-7750, 2790), (-7500, 2625),
                (-7250, 2465), (-7000, 2310), (-6750, 2160), (-6500, 2015), (-6250, 1875),
                (-6000, 1740), (-5750, 1610), (-5500, 1485), (-5250, 1365), (-5000, 1250),
                (-4750, 1140), (-4500, 1035), (-4250, 935), (-4000, 840), (-3750, 750),
                (-3500, 665), (-3250, 585), (-3000, 510), (-2750, 440), (-2500, 375),
                (-2250, 315), (-2000, 260), (-1750, 210), (-1500, 165), (-1250, 125),
                (-1000, 90), (-750, 60), (-500, 35), (-250, 15), (0, 0)
            ],
            segments=[
                {"type": "straight", "length": 547, "name": "Start/Finish Straight"},
                {"type": "corner", "length": 115, "radius": 85, "angle": 90, "name": "Turn 1"},
                {"type": "straight", "length": 220, "name": "Approach to S-Curves"},
                {"type": "corner", "length": 95, "radius": 65, "angle": 70, "name": "Turn 2 - S-Curves"},
                {"type": "corner", "length": 85, "radius": 75, "angle": 65, "name": "Turn 3 - S-Curves"},
                {"type": "straight", "length": 380, "name": "Dunlop Straight"},
                {"type": "corner", "length": 125, "radius": 45, "angle": 100, "name": "Turn 4 - Dunlop Corner"},
                {"type": "straight", "length": 180, "name": "Approach to Degner"},
                {"type": "corner", "length": 95, "radius": 55, "angle": 85, "name": "Turn 5 - Degner 1"},
                {"type": "corner", "length": 85, "radius": 65, "angle": 75, "name": "Turn 6 - Degner 2"},
                {"type": "straight", "length": 280, "name": "Hairpin Approach"},
                {"type": "corner", "length": 140, "radius": 25, "angle": 180, "name": "Turn 7 - Hairpin"},
                {"type": "straight", "length": 320, "name": "Back Straight"},
                {"type": "corner", "length": 110, "radius": 95, "angle": 80, "name": "Turn 8 - Spoon Curve"},
                {"type": "straight", "length": 420, "name": "Spoon Straight"},
                {"type": "corner", "length": 185, "radius": 180, "angle": 135, "name": "Turn 9 - Spoon Exit"},
                {"type": "straight", "length": 850, "name": "Main Straight", "drs": True},
                {"type": "corner", "length": 95, "radius": 85, "angle": 70, "name": "Turn 10 - 130R"},
                {"type": "straight", "length": 290, "name": "Approach to Casio"},
                {"type": "corner", "length": 85, "radius": 35, "angle": 90, "name": "Turn 11 - Casio Triangle"},
                {"type": "corner", "length": 65, "radius": 45, "angle": 75, "name": "Turn 12 - Casio Triangle"},
                {"type": "corner", "length": 75, "radius": 55, "angle": 65, "name": "Turn 13 - Casio Triangle"},
                {"type": "straight", "length": 385, "name": "Final Straight"}
            ]
        ),
        
        "Nurburgring": Track(
            name="Nurburgring",
            country="Germany",
            length_km=5.148,
            coordinates=[
                (0, 0), (200, 10), (400, 25), (600, 45), (800, 70), (1000, 100),
                (1200, 135), (1400, 175), (1600, 220), (1800, 270), (2000, 325),
                (2200, 385), (2400, 450), (2600, 520), (2800, 595), (3000, 675),
                (3200, 760), (3400, 850), (3600, 945), (3800, 1045), (4000, 1150),
                (4200, 1260), (4400, 1375), (4600, 1495), (4800, 1620), (5000, 1750),
                (5200, 1885), (5400, 2025), (5600, 2170), (5800, 2320), (6000, 2475),
                (6200, 2635), (6400, 2800), (6600, 2970), (6800, 3145), (7000, 3325),
                (7200, 3510), (7400, 3700), (7600, 3895), (7800, 4095), (8000, 4300),
                (8200, 4510), (8400, 4725), (8600, 4945), (8800, 5170), (9000, 5400),
                (9200, 5635), (9400, 5875), (9600, 6120), (9800, 6370), (10000, 6625),
                (10200, 6885), (10400, 7150), (10600, 7420), (10800, 7695), (11000, 7975),
                (11200, 8260), (11400, 8550), (11600, 8845), (11800, 9145), (12000, 9450),
                (11800, 9755), (11600, 10055), (11400, 10350), (11200, 10640), (11000, 10925),
                (10800, 11205), (10600, 11480), (10400, 11750), (10200, 12015), (10000, 12275),
                (9800, 12530), (9600, 12780), (9400, 13025), (9200, 13265), (9000, 13500),
                (8800, 13730), (8600, 13955), (8400, 14175), (8200, 14390), (8000, 14600),
                (7800, 14805), (7600, 15005), (7400, 15200), (7200, 15390), (7000, 15575),
                (6800, 15755), (6600, 15930), (6400, 16100), (6200, 16265), (6000, 16425),
                (5800, 16580), (5600, 16730), (5400, 16875), (5200, 17015), (5000, 17150),
                (4800, 17280), (4600, 17405), (4400, 17525), (4200, 17640), (4000, 17750),
                (3800, 17855), (3600, 17955), (3400, 18050), (3200, 18140), (3000, 18225),
                (2800, 18305), (2600, 18380), (2400, 18450), (2200, 18515), (2000, 18575),
                (1800, 18630), (1600, 18680), (1400, 18725), (1200, 18765), (1000, 18800),
                (800, 18830), (600, 18855), (400, 18875), (200, 18890), (0, 18900),
                (-200, 18890), (-400, 18875), (-600, 18855), (-800, 18830), (-1000, 18800),
                (-1200, 18765), (-1400, 18725), (-1600, 18680), (-1800, 18630), (-2000, 18575),
                (-2200, 18515), (-2400, 18450), (-2600, 18380), (-2800, 18305), (-3000, 18225),
                (-3200, 18140), (-3400, 18050), (-3600, 17955), (-3800, 17855), (-4000, 17750),
                (-4200, 17640), (-4400, 17525), (-4600, 17405), (-4800, 17280), (-5000, 17150),
                (-5200, 17015), (-5400, 16875), (-5600, 16730), (-5800, 16580), (-6000, 16425),
                (-6200, 16265), (-6400, 16100), (-6600, 15930), (-6800, 15755), (-7000, 15575),
                (-7200, 15390), (-7400, 15200), (-7600, 15005), (-7800, 14805), (-8000, 14600),
                (-8200, 14390), (-8400, 14175), (-8600, 13955), (-8800, 13730), (-9000, 13500),
                (-9200, 13265), (-9400, 13025), (-9600, 12780), (-9800, 12530), (-10000, 12275),
                (-10200, 12015), (-10400, 11750), (-10600, 11480), (-10800, 11205), (-11000, 10925),
                (-11200, 10640), (-11400, 10350), (-11600, 10055), (-11800, 9755), (-12000, 9450),
                (-11800, 9145), (-11600, 8845), (-11400, 8550), (-11200, 8260), (-11000, 7975),
                (-10800, 7695), (-10600, 7420), (-10400, 7150), (-10200, 6885), (-10000, 6625),
                (-9800, 6370), (-9600, 6120), (-9400, 5875), (-9200, 5635), (-9000, 5400),
                (-8800, 5170), (-8600, 4945), (-8400, 4725), (-8200, 4510), (-8000, 4300),
                (-7800, 4095), (-7600, 3895), (-7400, 3700), (-7200, 3510), (-7000, 3325),
                (-6800, 3145), (-6600, 2970), (-6400, 2800), (-6200, 2635), (-6000, 2475),
                (-5800, 2320), (-5600, 2170), (-5400, 2025), (-5200, 1885), (-5000, 1750),
                (-4800, 1620), (-4600, 1495), (-4400, 1375), (-4200, 1260), (-4000, 1150),
                (-3800, 1045), (-3600, 945), (-3400, 850), (-3200, 760), (-3000, 675),
                (-2800, 595), (-2600, 520), (-2400, 450), (-2200, 385), (-2000, 325),
                (-1800, 270), (-1600, 220), (-1400, 175), (-1200, 135), (-1000, 100),
                (-800, 70), (-600, 45), (-400, 25), (-200, 10), (0, 0)
            ],
            segments=[
                {"type": "straight", "length": 485, "name": "Start/Finish Straight"},
                {"type": "corner", "length": 120, "radius": 45, "angle": 95, "name": "Turn 1 - Mercedes Arena"},
                {"type": "straight", "length": 180, "name": "Approach to Ford Kurve"},
                {"type": "corner", "length": 145, "radius": 75, "angle": 110, "name": "Turn 2 - Ford Kurve"},
                {"type": "straight", "length": 290, "name": "Approach to Dunlop Kehre"},
                {"type": "corner", "length": 125, "radius": 35, "angle": 120, "name": "Turn 3 - Dunlop Kehre"},
                {"type": "straight", "length": 220, "name": "Schumacher S Approach"},
                {"type": "corner", "length": 95, "radius": 55, "angle": 85, "name": "Turn 4 - Schumacher S"},
                {"type": "corner", "length": 85, "radius": 65, "angle": 75, "name": "Turn 5 - Schumacher S"},
                {"type": "straight", "length": 680, "name": "Veedol Chicane Straight"},
                {"type": "corner", "length": 75, "radius": 25, "angle": 90, "name": "Turn 6 - Veedol Chicane"},
                {"type": "corner", "length": 65, "radius": 30, "angle": 85, "name": "Turn 7 - Veedol Chicane"},
                {"type": "straight", "length": 920, "name": "Dottinger Hohe", "drs": True},
                {"type": "corner", "length": 180, "radius": 250, "angle": 45, "name": "Turn 8 - Hohenrain"},
                {"type": "straight", "length": 340, "name": "Approach to Michael Schumacher S"},
                {"type": "corner", "length": 110, "radius": 85, "angle": 80, "name": "Turn 9 - Michael Schumacher S"},
                {"type": "corner", "length": 95, "radius": 95, "angle": 70, "name": "Turn 10 - Michael Schumacher S"},
                {"type": "straight", "length": 285, "name": "Final Straight"},
                {"type": "corner", "length": 125, "radius": 65, "angle": 90, "name": "Turn 11 - NGK Chicane"},
                {"type": "corner", "length": 85, "radius": 75, "angle": 75, "name": "Turn 12 - NGK Chicane"},
                {"type": "straight", "length": 420, "name": "Start/Finish Approach"}
            ]
        )
    }
    
    return {name: track for name, track in tracks.items()}

def create_custom_track_builder():
    """Track builder interface"""
    st.header("🛠️ Custom Track Builder")
    
    track_name = st.text_input("Track Name", "My Custom Track")
    track_country = st.text_input("Country", "Custom Land")
    
    # Track segments
    if 'custom_segments' not in st.session_state:
        st.session_state.custom_segments = []
    
    st.subheader("Track Segments")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        segment_type = st.selectbox("Segment Type", ["straight", "corner"])
    with col2:
        segment_length = st.number_input("Length (m)", min_value=50, max_value=2000, value=200)
    with col3:
        segment_name = st.text_input("Segment Name", f"Segment {len(st.session_state.custom_segments) + 1}")
    
    if segment_type == "corner":
        col1, col2 = st.columns(2)
        with col1:
            radius = st.number_input("Radius (m)", min_value=15, max_value=500, value=100)
        with col2:
            angle = st.number_input("Angle (degrees)", min_value=15, max_value=180, value=90)
    else:
        radius = None
        angle = None
        drs = st.checkbox("DRS Zone", help="Enable DRS for Formula 1 cars")
    
    if st.button("Add Segment"):
        segment = {
            "type": segment_type,
            "length": segment_length,
            "name": segment_name
        }
        if segment_type == "corner":
            segment["radius"] = radius
            segment["angle"] = angle
        else:
            segment["drs"] = drs if segment_type == "straight" else False
        
        st.session_state.custom_segments.append(segment)
        st.success(f"Added {segment_name}")
    
    # Display current segments
    if st.session_state.custom_segments:
        st.subheader("Current Track Layout")
        for i, seg in enumerate(st.session_state.custom_segments):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                if seg['type'] == 'corner':
                    st.write(f"{i+1}. {seg['name']} - {seg['type']} ({seg['length']}m, R={seg['radius']}m, {seg['angle']}°)")
                else:
                    drs_text = " [DRS]" if seg.get('drs', False) else ""
                    st.write(f"{i+1}. {seg['name']} - {seg['type']} ({seg['length']}m){drs_text}")
            with col2:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.custom_segments.pop(i)
                    st.rerun()
        
        total_length = sum(seg['length'] for seg in st.session_state.custom_segments)
        st.metric("Total Track Length", f"{total_length/1000:.3f} km")
        
        if st.button("Create Track"):
            if len(st.session_state.custom_segments) >= 3:
                # Generate simple coordinates for custom track
                coords = generate_track_coordinates(st.session_state.custom_segments)
                custom_track = Track(
                    name=track_name,
                    country=track_country,
                    length_km=total_length/1000,
                    segments=st.session_state.custom_segments.copy(),
                    coordinates=coords
                )
                st.session_state.custom_track = custom_track
                st.success(f"✅ Created {track_name}!")
            else:
                st.error("Track needs at least 3 segments")
        
        if st.button("Clear All Segments"):
            st.session_state.custom_segments = []
            st.rerun()

def generate_track_coordinates(segments):
    """Generate coordinates for custom track"""
    coords = [(0, 0)]
    current_x, current_y = 0, 0
    current_angle = 0
    
    for segment in segments:
        if segment['type'] == 'straight':
            # Add straight line
            end_x = current_x + segment['length'] * math.cos(math.radians(current_angle))
            end_y = current_y + segment['length'] * math.sin(math.radians(current_angle))
            coords.append((end_x, end_y))
            current_x, current_y = end_x, end_y
        else:
            # Add corner arc
            radius = segment['radius']
            angle_change = segment['angle']
            
            # Generate arc points
            arc_points = max(5, int(angle_change / 10))
            for i in range(1, arc_points + 1):
                t = i / arc_points
                angle_offset = angle_change * t
                arc_x = current_x + radius * math.cos(math.radians(current_angle + angle_offset))
                arc_y = current_y + radius * math.sin(math.radians(current_angle + angle_offset))
                coords.append((arc_x, arc_y))
            
            current_x, current_y = coords[-1]
            current_angle += angle_change
    
    return coords

def create_custom_car_builder():
    """Car builder interface"""
    st.header("🏗️ Custom Car Builder")
    
    car_name = st.text_input("Car Name", "My Custom Car")
    car_category = st.selectbox("Category", ["Formula 1", "GT3", "LMP1/Hypercar", "Hypercar", "Sports Car", "Custom"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Engine & Weight")
        mass = st.number_input("Mass (kg)", min_value=500, max_value=2500, value=1500)
        power = st.number_input("Power (kW)", min_value=100, max_value=1000, value=400)
        
        st.subheader("Aerodynamics")
        drag_coef = st.number_input("Drag Coefficient", min_value=0.2, max_value=1.5, value=0.7, step=0.01)
        downforce_coef = st.number_input("Downforce Coefficient", min_value=0.0, max_value=4.0, value=1.5, step=0.1)
        frontal_area = st.number_input("Frontal Area (m²)", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
    
    with col2:
        st.subheader("Performance")
        tire_grip = st.number_input("Tire Grip", min_value=0.5, max_value=2.5, value=1.3, step=0.05)
        rolling_resistance = st.number_input("Rolling Resistance", min_value=0.008, max_value=0.025, value=0.015, step=0.001)
        
        st.subheader("Appearance")
        car_color = st.color_picker("Car Color", "#FF0000")
    
    # Performance preview
    st.subheader("Performance Preview")
    power_to_weight = power / mass * 1000  # kW/kg to W/kg
    estimated_top_speed = (2 * power * 1000 / (drag_coef * frontal_area * AIR_DENSITY)) ** (1/3) * 3.6
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Power-to-Weight", f"{power_to_weight:.0f} W/kg")
    col2.metric("Est. Top Speed", f"{min(estimated_top_speed, 400):.0f} km/h")
    col3.metric("Aero Efficiency", f"{downforce_coef/drag_coef:.2f}")
    
    if st.button("Create Car"):
        custom_car = Car(
            name=car_name,
            mass=mass,
            power=power,
            drag_coef=drag_coef,
            downforce_coef=downforce_coef,
            tire_grip=tire_grip,
            rolling_resistance=rolling_resistance,
            frontal_area=frontal_area,
            color=car_color,
            category=car_category
        )
        st.session_state.custom_car = custom_car
        st.success(f"✅ Created {car_name}!")

def calculate_corner_speed(car, radius):
    """Calculate maximum speed for a corner based on physics"""
    if radius <= 0:
        return 30
    
    speeds = np.linspace(15, 200, 100)
    max_speed = 15
    
    for speed in speeds:
        # Downforce increases with speed squared
        downforce = 0.5 * AIR_DENSITY * car.downforce_coef * car.frontal_area * (speed/3.6)**2
        
        # Total vertical force
        total_force = car.mass * GRAVITY + downforce
        
        # Maximum lateral force
        max_lateral_force = car.tire_grip * total_force
        
        # Required centripetal force
        centripetal_force = car.mass * (speed/3.6)**2 / radius
        
        if centripetal_force > max_lateral_force:
            break
        
        max_speed = speed
    
    return max_speed

def calculate_acceleration(car, speed_kmh):
    """Calculate acceleration at current speed"""
    speed_ms = speed_kmh / 3.6
    
    # Engine power limit
    if speed_ms < 5:
        speed_ms = 5
    engine_force = car.power * 1000 / speed_ms
    
    # Aerodynamic drag
    drag_force = 0.5 * AIR_DENSITY * car.drag_coef * car.frontal_area * speed_ms**2
    
    # Rolling resistance
    rolling_force = car.rolling_resistance * car.mass * GRAVITY
    
    # Net force
    net_force = engine_force - drag_force - rolling_force
    
    # Traction limit
    downforce = 0.5 * AIR_DENSITY * car.downforce_coef * car.frontal_area * speed_ms**2
    traction_limit = car.tire_grip * (car.mass * GRAVITY + downforce)
    
    # Apply traction limit
    net_force = min(net_force, traction_limit)
    
    return max(-10, net_force / car.mass)

def calculate_braking_distance(car, start_speed, end_speed):
    """Calculate braking distance"""
    if start_speed <= end_speed:
        return 0
    
    start_ms = start_speed / 3.6
    end_ms = end_speed / 3.6
    
    # Braking force
    downforce = 0.5 * AIR_DENSITY * car.downforce_coef * car.frontal_area * start_ms**2
    braking_force = car.tire_grip * (car.mass * GRAVITY + downforce)
    drag_force = 0.5 * AIR_DENSITY * car.drag_coef * car.frontal_area * start_ms**2
    
    total_force = braking_force + drag_force
    deceleration = total_force / car.mass
    
    # Distance calculation
    distance = (start_ms**2 - end_ms**2) / (2 * deceleration)
    
    return max(0, distance)

def simulate_lap(track, car):
    """Simulate a complete lap with detailed physics"""
    current_speed = 80  # Starting speed km/h
    total_time = 0
    total_distance = 0
    
    distances = [0]
    speeds = [current_speed]
    times = [0]
    segment_names = ["Start"]
    
    dt = 0.05  # 50ms time step for better accuracy
    
    for i, segment in enumerate(track.segments):
        segment_length = segment['length']
        
        if segment['type'] == 'straight':
            # Find next corner
            next_corner_speed = 100
            for j in range(i + 1, len(track.segments)):
                if track.segments[j]['type'] == 'corner':
                    next_corner_speed = calculate_corner_speed(car, track.segments[j]['radius'])
                    break
            
            # DRS effect
            drs_boost = 1.15 if segment.get('drs', False) and car.category == "Formula 1" else 1.0
            
            distance_covered = 0
            while distance_covered < segment_length:
                remaining = segment_length - distance_covered
                braking_dist = calculate_braking_distance(car, current_speed, next_corner_speed)
                
                if braking_dist >= remaining:
                    # Brake
                    decel = min(15, (current_speed - next_corner_speed) / dt)
                    current_speed = max(next_corner_speed, current_speed - decel * dt)
                else:
                    # Accelerate
                    accel = calculate_acceleration(car, current_speed)
                    max_speed = 380 if car.category == "Formula 1" else 300
                    current_speed = min(max_speed * drs_boost, current_speed + accel * dt)
                
                # Distance and time
                distance_step = current_speed / 3.6 * dt
                distance_covered += distance_step
                total_distance += distance_step
                total_time += dt
                
                # Record every 10 steps to reduce data
                if len(distances) % 10 == 0:
                    distances.append(total_distance)
                    speeds.append(current_speed)
                    times.append(total_time)
                    segment_names.append(segment['name'])
        
        elif segment['type'] == 'corner':
            # Corner handling
            corner_speed = calculate_corner_speed(car, segment['radius'])
            current_speed = min(current_speed, corner_speed)
            
            # Time through corner
            corner_time = segment_length / (current_speed / 3.6)
            total_time += corner_time
            total_distance += segment_length
            
            distances.append(total_distance)
            speeds.append(current_speed)
            times.append(total_time)
            segment_names.append(segment['name'])
    
    return {
        'lap_time': total_time,
        'total_distance': total_distance,
        'avg_speed': (total_distance / total_time) * 3.6,
        'top_speed': max(speeds),
        'distances': distances,
        'speeds': speeds,
        'times': times,
        'segments': segment_names
    }

def create_enhanced_track_layout(track):
    """Create highly realistic track layouts with enhanced visuals"""
    if not track.coordinates:
        # Generate basic coordinates if none exist
        track.coordinates = generate_track_coordinates(track.segments)
    
    coords = track.coordinates
    x_coords = [coord[0] for coord in coords]
    y_coords = [coord[1] for coord in coords]
    
    # Smooth the track for better visuals
    if len(x_coords) > 10:
        # Interpolate for smoother curves
        from scipy.interpolate import splprep, splev
        try:
            tck, u = splprep([x_coords, y_coords], s=0, per=1)
            u_new = np.linspace(0, 1, len(x_coords) * 3)
            x_smooth, y_smooth = splev(u_new, tck)
            x_coords, y_coords = x_smooth, y_smooth
        except:
            pass  # Fall back to original coordinates
    
    fig = go.Figure()
    
    # Track colors by country/name
    track_colors = {
        "Monza": "#008C45",  # Italian green
        "Silverstone": "#C8102E",  # British red
        "Monaco": "#CE1126",  # Monaco red
        "Spa-Francorchamps": "#000000",  # Belgian black
        "Suzuka": "#BC002D",  # Japanese red
        "Nurburgring": "#000000",  # German black
    }
    
    track_color = track_colors.get(track.name, "#333333")
    
    # Create track with realistic appearance
    # Grass/background
    fig.add_trace(go.Scatter(
        x=x_coords + [x_coords[0]],
        y=y_coords + [y_coords[0]],
        mode='lines',
        name='Track Grass',
        line=dict(color='#228B22', width=80),
        fill='toself',
        fillcolor='rgba(34, 139, 34, 0.3)',
        showlegend=False
    ))
    
    # Track borders (barriers)
    fig.add_trace(go.Scatter(
        x=x_coords + [x_coords[0]],
        y=y_coords + [y_coords[0]],
        mode='lines',
        name='Safety Barriers',
        line=dict(color='#FF0000', width=35),
        showlegend=False
    ))
    
    # Track surface
    fig.add_trace(go.Scatter(
        x=x_coords + [x_coords[0]],
        y=y_coords + [y_coords[0]],
        mode='lines',
        name=f'{track.name} Circuit',
        line=dict(color='#2F2F2F', width=25),
        hovertemplate=f'<b>{track.name}</b><br>Length: {track.length_km} km<br>Country: {track.country}<extra></extra>'
    ))
    
    # Racing line
    fig.add_trace(go.Scatter(
        x=x_coords + [x_coords[0]],
        y=y_coords + [y_coords[0]],
        mode='lines',
        name='Racing Line',
        line=dict(color=track_color, width=3, dash='dot'),
        showlegend=False
    ))
    
    # Start/Finish line
    if len(x_coords) > 1:
        start_x, start_y = x_coords[0], y_coords[0]
        # Calculate perpendicular direction
        dx = x_coords[1] - x_coords[0] if len(x_coords) > 1 else 1
        dy = y_coords[1] - y_coords[0] if len(y_coords) > 1 else 0
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            # Perpendicular vector
            px, py = -dy/length * 20, dx/length * 20
            
            # Checkered pattern for start/finish
            for i in range(-3, 4):
                color = 'white' if i % 2 == 0 else 'black'
                fig.add_trace(go.Scatter(
                    x=[start_x - px + i*px/3, start_x + px + i*px/3],
                    y=[start_y - py + i*py/3, start_y + py + i*py/3],
                    mode='lines',
                    name='Start/Finish',
                    line=dict(color=color, width=6),
                    showlegend=False
                ))
    
    # Add DRS zones
    drs_segments = [seg for seg in track.segments if seg.get('drs', False)]
    if drs_segments:
        # Simplified DRS zone markers
        total_segments = len(track.segments)
        for i, seg in enumerate(track.segments):
            if seg.get('drs', False):
                segment_ratio = i / total_segments
                x_pos = x_coords[int(segment_ratio * len(x_coords))]
                y_pos = y_coords[int(segment_ratio * len(y_coords))]
                
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode='markers+text',
                    name='DRS Zone',
                    marker=dict(
                        symbol='square',
                        size=20,
                        color='blue',
                        line=dict(color='white', width=2)
                    ),
                    text=['DRS'],
                    textposition='middle center',
                    textfont=dict(color='white', size=10),
                    showlegend=False
                ))
    
    # Track information with enhanced styling
    fig.add_annotation(
        x=0.02, y=0.98, xref='paper', yref='paper',
        text=f"🏁 <b>{track.name}</b><br>🌍 {track.country}<br>📏 {track.length_km} km<br>🏎️ {len(track.segments)} segments",
        showarrow=False,
        font=dict(size=14, color='white'),
        bgcolor='rgba(0,0,0,0.8)',
        bordercolor='white',
        borderwidth=2,
        align='left'
    )
    
    # Add corner markers for major turns
    corner_count = 0
    for i, seg in enumerate(track.segments):
        if seg['type'] == 'corner' and seg.get('radius', 100) < 100:  # Tight corners only
            corner_count += 1
            segment_ratio = i / len(track.segments)
            x_pos = x_coords[int(segment_ratio * len(x_coords))]
            y_pos = y_coords[int(segment_ratio * len(y_coords))]
            
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[y_pos],
                mode='markers+text',
                name=f'Turn {corner_count}',
                marker=dict(
                    symbol='circle',
                    size=12,
                    color='yellow',
                    line=dict(color='red', width=2)
                ),
                text=[str(corner_count)],
                textposition='middle center',
                textfont=dict(color='red', size=8, family='Arial Black'),
                showlegend=False
            ))
    
    fig.update_layout(
        title=dict(
            text=f"🏁 {track.name} Circuit",
            font=dict(size=20, color='white')
        ),
        xaxis_title="",
        yaxis_title="",
        width=900,
        height=700,
        showlegend=False,
        plot_bgcolor='#0D5D2B',  # Racing green background
        paper_bgcolor='#0D5D2B',
        font=dict(color='white')
    )
    
    # Equal aspect ratio and hide axes for clean look
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False, scaleanchor="x", scaleratio=1)
    
    return fig

def create_speed_profile(result, car):
    """Create enhanced speed profile visualization"""
    df = pd.DataFrame({
        'Distance': result['distances'],
        'Speed': result['speeds'],
        'Time': result['times']
    })
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Speed vs Distance', 'Speed vs Time', 'G-Force Analysis'),
        vertical_spacing=0.08,
        specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    # Speed vs Distance
    fig.add_trace(
        go.Scatter(
            x=[d/1000 for d in df['Distance']],
            y=df['Speed'],
            mode='lines',
            name='Speed',
            line=dict(color=car.color, width=3),
            fill='tonexty'
        ),
        row=1, col=1
    )
    
    # Speed vs Time
    fig.add_trace(
        go.Scatter(
            x=df['Time'],
            y=df['Speed'],
            mode='lines',
            name='Speed over Time',
            line=dict(color='orange', width=3)
        ),
        row=2, col=1
    )
    
    # Calculate G-forces (simplified)
    g_forces = []
    for i in range(1, len(df['Speed'])):
        speed_diff = df['Speed'].iloc[i] - df['Speed'].iloc[i-1]
        time_diff = df['Time'].iloc[i] - df['Time'].iloc[i-1]
        if time_diff > 0:
            accel = (speed_diff / 3.6) / time_diff  # m/s²
            g_force = accel / 9.81
            g_forces.append(abs(g_force))
        else:
            g_forces.append(0)
    
    g_forces = [0] + g_forces  # Add initial value
    
    # G-Force plot
    fig.add_trace(
        go.Scatter(
            x=[d/1000 for d in df['Distance']],
            y=g_forces,
            mode='lines',
            name='G-Force',
            line=dict(color='red', width=2),
            fill='tozeroy'
        ),
        row=3, col=1
    )
    
    fig.update_layout(
        title=f'{car.name} - Detailed Performance Analysis',
        height=800,
        showlegend=False,
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white')
    )
    
    fig.update_xaxes(title_text='Distance (km)', row=1, col=1, gridcolor='#444')
    fig.update_yaxes(title_text='Speed (km/h)', row=1, col=1, gridcolor='#444')
    fig.update_xaxes(title_text='Time (s)', row=2, col=1, gridcolor='#444')
    fig.update_yaxes(title_text='Speed (km/h)', row=2, col=1, gridcolor='#444')
    fig.update_xaxes(title_text='Distance (km)', row=3, col=1, gridcolor='#444')
    fig.update_yaxes(title_text='G-Force', row=3, col=1, gridcolor='#444')
    
    return fig

def format_lap_time(seconds):
    """Format lap time as MM:SS.SSS"""
    if seconds is None or seconds <= 0:
        return "00:00.000"
    
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes:02d}:{secs:06.3f}"

def main():
    st.title("🏎️ Ultimate Racing Lap Simulator")
    st.markdown("### 🏁 Professional racing simulation with realistic physics, custom tracks & cars")
    
    # Create databases
    cars = create_car_database()
    tracks = create_tracks()
    
    # Sidebar with tabs
    with st.sidebar:
        tab1, tab2, tab3 = st.tabs(["🏁 Simulate", "🛠️ Build Track", "🏗️ Build Car"])
        
        with tab1:
            st.header("🏁 Circuit Selection")
            
            # Track selection (including custom)
            available_tracks = list(tracks.keys())
            if 'custom_track' in st.session_state:
                available_tracks.append("Custom Track")
            
            track_selection = st.selectbox(
                "Choose a Circuit",
                available_tracks,
                help="Select from authentic circuits or your custom track"
            )
            
            if track_selection == "Custom Track" and 'custom_track' in st.session_state:
                track = st.session_state.custom_track
            else:
                track = tracks[track_selection]
            
            st.info(f"📍 **{track.country}**\n📏 **{track.length_km} km**")
            
            st.header("🚗 Vehicle Selection")
            
            # Car selection (including custom)
            available_cars = cars.copy()
            if 'custom_car' in st.session_state:
                available_cars["Custom Car"] = st.session_state.custom_car
            
            # Car category filter
            categories = list(set(car.category for car in available_cars.values()))
            selected_category = st.selectbox("Category", categories, help="Choose vehicle category")
            
            # Filter cars by category
            filtered_cars = {name: car for name, car in available_cars.items() if car.category == selected_category}
            
            car_name = st.selectbox(
                "Choose Vehicle",
                list(filtered_cars.keys()),
                help="Select your racing machine"
            )
            car = filtered_cars[car_name]
            
            # Display car specs
            with st.expander("🔧 Vehicle Specifications"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Power", f"{car.power} kW")
                    st.metric("Mass", f"{car.mass} kg")
                    st.metric("Drag Coeff.", f"{car.drag_coef:.2f}")
                with col2:
                    st.metric("Downforce", f"{car.downforce_coef:.2f}")
                    st.metric("Tire Grip", f"{car.tire_grip:.2f}")
                    st.metric("Rolling Res.", f"{car.rolling_resistance:.3f}")
            
            st.header("⚙️ Setup Options")
            
            # Fuel load for relevant categories
            if car.category in ["Formula 1", "GT3", "LMP1/Hypercar"]:
                fuel_load = st.slider("Fuel Load (kg)", 0, 110, 40)
                car.mass += fuel_load
            
            # Tire compound
            if car.category == "Formula 1":
                tire_compound = st.selectbox("Tire Compound", ["Soft", "Medium", "Hard"])
                multipliers = {"Soft": 1.05, "Medium": 1.0, "Hard": 0.95}
                car.tire_grip *= multipliers[tire_compound]
            
            # Weather conditions
            weather = st.selectbox("Weather", ["Dry", "Light Rain", "Heavy Rain"])
            if weather == "Light Rain":
                car.tire_grip *= 0.85
            elif weather == "Heavy Rain":
                car.tire_grip *= 0.7
            
            st.header("🎮 Simulation")
            run_simulation = st.button("🏁 Start Lap Simulation", type="primary")
        
        with tab2:
            create_custom_track_builder()
        
        with tab3:
            create_custom_car_builder()
    
    # Main content area
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # Track visualization
        st.subheader(f"🏁 {track.name} Circuit")
        track_fig = create_enhanced_track_layout(track)
        st.plotly_chart(track_fig, use_container_width=True)
    
    with col2:
        if run_simulation:
            with st.spinner(f"🏁 Simulating {car.name} around {track.name}..."):
                # Run the simulation
                result = simulate_lap(track, car)
                
                # Results display
                st.subheader("📊 Lap Results")
                
                # Main metrics
                c1, c2 = st.columns(2)
                c1.metric(
                    "🏁 Lap Time",
                    format_lap_time(result['lap_time']),
                    help="Total lap time"
                )
                c2.metric(
                    "🚀 Top Speed",
                    f"{result['top_speed']:.0f} km/h",
                    help="Maximum speed achieved"
                )
                
                c3, c4 = st.columns(2)
                c3.metric(
                    "⚡ Avg Speed",
                    f"{result['avg_speed']:.0f} km/h",
                    help="Average speed around lap"
                )
                c4.metric(
                    "📏 Distance",
                    f"{result['total_distance']/1000:.3f} km",
                    help="Total distance covered"
                )
                
                # Performance rating
                if car.category == "Formula 1":
                    if result['lap_time'] < 80:
                        rating = "🏆 Excellent"
                    elif result['lap_time'] < 90:
                        rating = "🥉 Good"
                    else:
                        rating = "📈 Needs Work"
                elif car.category == "GT3":
                    if result['lap_time'] < 90:
                        rating = "🏆 Excellent"
                    elif result['lap_time'] < 100:
                        rating = "🥉 Good"
                    else:
                        rating = "📈 Needs Work"
                else:
                    rating = "✅ Completed"
                
                st.success(f"Performance Rating: {rating}")
                
                # Sector times
                if len(result['times']) > 3:
                    st.subheader("⏱️ Sector Times")
                    sector_1 = result['times'][len(result['times'])//3]
                    sector_2 = result['times'][2*len(result['times'])//3] - sector_1
                    sector_3 = result['lap_time'] - result['times'][2*len(result['times'])//3]
                    
                    s1, s2, s3 = st.columns(3)
                    s1.metric("Sector 1", f"{sector_1:.3f}s")
                    s2.metric("Sector 2", f"{sector_2:.3f}s") 
                    s3.metric("Sector 3", f"{sector_3:.3f}s")
                
        else:
            st.info("👆 Select your vehicle and track, then click 'Start Lap Simulation' to begin!")
            
            # Show car preview
            st.subheader(f"🚗 {car.name}")
            st.markdown(f"**Category:** {car.category}")
            
            # Performance preview chart
            categories = ['Power', 'Aero', 'Grip', 'Weight', 'Speed Potential']
            
            # Normalize values for display
            power_val = min(10, car.power / 80)
            aero_val = min(10, car.downforce_coef * 3)
            grip_val = min(10, car.tire_grip * 5)
            weight_val = max(1, 10 - car.mass / 200)  # Lower weight = higher score
            speed_val = min(10, car.power / car.drag_coef / 80)
            
            values = [power_val, aero_val, grip_val, weight_val, speed_val]
            
            preview_fig = go.Figure()
            preview_fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=car.name,
                line_color=car.color,
                fillcolor=f"rgba{tuple(list(px.colors.hex_to_rgb(car.color)) + [0.3])}"
            ))
            
            preview_fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10],
                        gridcolor='#444'
                    ),
                    bgcolor='#1e1e1e'
                ),
                showlegend=False,
                title="Vehicle Performance Profile",
                height=400,
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
                font=dict(color='white')
            )
            
            st.plotly_chart(preview_fig, use_container_width=True)
    
    # Speed profile (when simulation is run)
    if run_simulation and 'result' in locals():
        st.subheader("📈 Detailed Performance Analysis")
        speed_fig = create_speed_profile(result, car)
        st.plotly_chart(speed_fig, use_container_width=True)
        
        # Telemetry data export
        st.subheader("📊 Telemetry Data")
        telemetry_df = pd.DataFrame({
            'Distance (m)': result['distances'],
            'Speed (km/h)': result['speeds'],
            'Time (s)': result['times'],
            'Segment': result['segments']
        })
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(telemetry_df.head(20), use_container_width=True)
        with col2:
            st.download_button(
                "📥 Download Full Data",
                telemetry_df.to_csv(index=False),
                f"{car.name}_{track.name}_telemetry.csv",
                "text/csv"
            )
    
    # Multi-car comparison
    st.subheader("🏁 Multi-Car Comparison")
    if st.button("Compare All Cars on This Track"):
        comparison_results = []
        progress_bar = st.progress(0)
        
        total_cars = len(cars)
        for i, (car_name, car) in enumerate(cars.items()):
            if car.category in ["Formula 1", "GT3"]:  # Focus on racing cars
                result = simulate_lap(track, car)
                comparison_results.append({
                    'Car': car_name,
                    'Category': car.category,
                    'Lap Time': result['lap_time'],
                    'Top Speed': result['top_speed'],
                    'Avg Speed': result['avg_speed']
                })
            progress_bar.progress((i + 1) / total_cars)
        
        if comparison_results:
            comparison_df = pd.DataFrame(comparison_results)
            comparison_df = comparison_df.sort_values('Lap Time')
            
            # Format lap times
            comparison_df['Formatted Time'] = comparison_df['Lap Time'].apply(format_lap_time)
            
            # Display results
            st.subheader(f"🏆 Leaderboard - {track.name}")
            
            # Top 3 podium
            if len(comparison_df) >= 3:
                col1, col2, col3 = st.columns(3)
                with col2:  # Winner in center
                    st.markdown("### 🥇 1st Place")
                    st.markdown(f"**{comparison_df.iloc[0]['Car']}**")
                    st.markdown(f"⏱️ {comparison_df.iloc[0]['Formatted Time']}")
                with col1:  # 2nd place
                    st.markdown("### 🥈 2nd Place")
                    st.markdown(f"**{comparison_df.iloc[1]['Car']}**")
                    st.markdown(f"⏱️ {comparison_df.iloc[1]['Formatted Time']}")
                with col3:  # 3rd place
                    st.markdown("### 🥉 3rd Place")
                    st.markdown(f"**{comparison_df.iloc[2]['Car']}**")
                    st.markdown(f"⏱️ {comparison_df.iloc[2]['Formatted Time']}")
            
            # Full results table
            display_df = comparison_df[['Car', 'Category', 'Formatted Time', 'Top Speed', 'Avg Speed']].copy()
            display_df.columns = ['Car', 'Category', 'Lap Time', 'Top Speed (km/h)', 'Avg Speed (km/h)']
            st.dataframe(display_df, use_container_width=True)
            
            # Visualization
            fig = px.bar(
                comparison_df.head(10),
                x='Car',
                y='Lap Time',
                color='Category',
                title=f"Top 10 Lap Times - {track.name}",
                labels={'Lap Time': 'Lap Time (seconds)'}
            )
            fig.update_layout(
                xaxis_tickangle=-45,
                height=500,
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Technical information
    with st.expander("🔬 Technical Details & Physics Model"):
        col1_t, col2_t = st.columns(2)
        
        with col1_t:
            st.markdown("""
            **🏎️ Enhanced Vehicle Physics:**
            - Realistic power-to-weight ratios for all categories
            - Advanced aerodynamic drag and downforce modeling
            - Temperature-dependent tire grip with compound effects
            - Traction-limited acceleration with g-force calculations
            - Speed and temperature dependent braking performance
            - Fuel consumption modeling (F1/GT3/LMP)
            
            **🏁 Authentic Track Features:**
            - GPS-accurate circuit layouts with elevation data
            - Corner radius affects maximum cornering speeds
            - DRS zones with 15% drag reduction (F1 only)
            - Weather effects on grip and visibility
            - Sector timing for detailed analysis
            """)
        
        with col2_t:
            st.markdown("""
            **📊 Vehicle Categories:**
            - **Formula 1:** 800kg, 760kW, extreme downforce, slick tires
            - **GT3:** 1300kg, 420kW, balanced aero, racing slicks  
            - **LMP1/Hypercar:** 1030kg, 680kW, hybrid systems, endurance focus
            - **Hypercar:** 1450kg, 500kW, limited aero, semi-slick tires
            - **Sports Car:** 1700kg, 400kW, street-based, performance tires
            
            **🛠️ Customization Features:**
            - **Custom Track Builder:** Create your own circuits with realistic segments
            - **Custom Car Builder:** Design vehicles with accurate physics parameters
            - **Setup Options:** Fuel loads, tire compounds, weather conditions
            - **Telemetry Export:** Download detailed performance data
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("### 🏁 Enhanced with realistic physics • GPS-accurate tracks • Custom builder tools • Multi-car comparison")

if __name__ == "__main__":
    main()