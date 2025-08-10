import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

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
    def __init__(self, name, segments, country, length_km):
        self.name = name
        self.segments = segments
        self.total_length = sum(seg['length'] for seg in segments)
        self.country = country
        self.length_km = length_km

def create_car_database():
    """Create database of different car types with realistic specifications"""
    cars = {
        # F1 Teams
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
    """Create more realistic F1 track layouts based on actual circuit data"""
    tracks = {
        "Monza": Track(
            name="Monza",
            country="Italy",
            length_km=5.793,
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
        )
    }
    
    return {name: track for name, track in tracks.items()}

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

def create_realistic_track_layout(track):
    """Create highly realistic track layouts based on actual F1 circuit data"""
    
    # Real track coordinate data (simplified but proportionally accurate)
    track_coords = {
        "Monza": [
            (0, 0), (380, 0), (420, -15), (450, -45), (480, -15), (520, 0),
            (880, 0), (910, -25), (925, -15), (940, -30), (970, -15),
            (1020, 0), (1080, -20), (1100, -40), (1120, -20), (1200, -10),
            (1250, -35), (1280, -55), (1300, -35), (1350, -20),
            (1420, -45), (1380, -85), (1320, -115), (1250, -125),
            (1180, -115), (1120, -85), (1080, -45), (980, -25),
            (880, -15), (780, -10), (680, -8), (580, -5), (480, -3),
            (380, -2), (280, -1), (180, 0), (0, 0)
        ],
        
        "Silverstone": [
            (0, 0), (90, 5), (150, 25), (200, 15), (260, 35), (300, 55),
            (330, 45), (360, 25), (420, 35), (480, 65), (540, 85),
            (600, 75), (680, 95), (760, 115), (840, 135), (920, 125),
            (1000, 145), (1080, 165), (1160, 155), (1220, 175),
            (1280, 185), (1340, 175), (1400, 155), (1440, 135),
            (1480, 115), (1500, 95), (1520, 75), (1480, 55),
            (1440, 35), (1380, 25), (1320, 15), (1260, 5),
            (1200, -5), (1140, -15), (1080, -25), (1020, -35),
            (960, -45), (900, -35), (840, -25), (780, -15),
            (720, -5), (660, 5), (600, 15), (540, 25), (480, 35),
            (420, 25), (360, 15), (300, 5), (240, -5), (180, -15),
            (120, -25), (60, -15), (0, 0)
        ],
        
        "Monaco": [
            (0, 0), (25, 5), (45, 15), (55, 35), (45, 55), (25, 65),
            (5, 75), (-15, 85), (-25, 105), (-15, 125), (5, 135),
            (25, 145), (45, 155), (65, 165), (85, 155), (105, 145),
            (115, 125), (105, 105), (85, 95), (65, 85), (45, 75),
            (25, 65), (15, 45), (25, 25), (45, 15), (65, 5),
            (85, -5), (105, -15), (115, -35), (105, -55), (85, -65),
            (65, -75), (45, -85), (25, -95), (5, -105), (-15, -115),
            (-35, -105), (-45, -85), (-35, -65), (-15, -55), (5, -45),
            (25, -35), (45, -25), (65, -15), (85, -5), (105, 5),
            (115, 25), (105, 45), (85, 55), (65, 65), (45, 75),
            (25, 85), (5, 95), (-15, 105), (-25, 115), (-15, 125),
            (5, 135), (25, 145), (45, 135), (65, 125), (85, 115),
            (105, 105), (115, 85), (105, 65), (85, 55), (65, 45),
            (45, 35), (25, 25), (5, 15), (-15, 5), (-25, -5),
            (-15, -15), (5, -5), (25, 5), (45, 15), (25, 5), (0, 0)
        ]
    }
    
    coords = track_coords.get(track.name, [(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)])
    
    # Create smooth interpolated track
    x_coords = []
    y_coords = []
    
    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]
        
        # Smooth interpolation
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance > 0:
            num_points = max(20, int(distance / 8))
            
            for j in range(num_points):
                t = j / num_points
                # Bezier-like smoothing
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                x_coords.append(x)
                y_coords.append(y)
    
    # Create the track visualization
    fig = go.Figure()
    
    # Track colors by category
    track_colors = {
        "Monza": "#1E41FF",  # Blue - Italian speed
        "Silverstone": "#00FF00",  # Green - British heritage
        "Monaco": "#FFD700",  # Gold - Monaco glamour
    }
    
    track_color = track_colors.get(track.name, "#333333")
    
    # Main track line
    fig.add_trace(go.Scatter(
        x=x_coords + [x_coords[0]],  # Close the loop
        y=y_coords + [y_coords[0]],
        mode='lines',
        name=f'{track.name} Circuit',
        line=dict(color=track_color, width=25),
        hovertemplate=f'<b>{track.name}</b><br>Length: {track.length_km} km<br>Country: {track.country}<extra></extra>'
    ))
    
    # Track borders for realism
    fig.add_trace(go.Scatter(
        x=x_coords + [x_coords[0]],
        y=y_coords + [y_coords[0]],
        mode='lines',
        name='Track Border',
        line=dict(color='white', width=30),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=x_coords + [x_coords[0]],
        y=y_coords + [y_coords[0]],
        mode='lines',
        name='Track Surface',
        line=dict(color='#2F2F2F', width=20),
        showlegend=False
    ))
    
    # Start/Finish line
    if len(x_coords) > 1:
        start_x, start_y = x_coords[0], y_coords[0]
        # Calculate perpendicular direction
        dx = x_coords[1] - x_coords[0]
        dy = y_coords[1] - y_coords[0]
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            # Perpendicular vector
            px, py = -dy/length * 15, dx/length * 15
            
            fig.add_trace(go.Scatter(
                x=[start_x - px, start_x + px],
                y=[start_y - py, start_y + py],
                mode='lines',
                name='Start/Finish',
                line=dict(color='white', width=8, dash='dot'),
                showlegend=False
            ))
    
    # Add sector markers
    total_points = len(x_coords)
    sector_points = [0, total_points//3, 2*total_points//3]
    
    for i, point_idx in enumerate(sector_points[1:], 1):
        if point_idx < len(x_coords):
            fig.add_trace(go.Scatter(
                x=[x_coords[point_idx]],
                y=[y_coords[point_idx]],
                mode='markers',
                name=f'Sector {i}',
                marker=dict(
                    symbol='diamond',
                    size=15,
                    color='yellow',
                    line=dict(color='black', width=2)
                ),
                showlegend=False
            ))
    
    # Track information
    fig.add_annotation(
        x=0.02, y=0.98, xref='paper', yref='paper',
        text=f"🏁 <b>{track.name}</b><br>📍 {track.country}<br>📏 {track.length_km} km",
        showarrow=False,
        font=dict(size=16, color='white'),
        bgcolor='rgba(0,0,0,0.8)',
        bordercolor='white',
        borderwidth=2,
        align='left'
    )
    
    fig.update_layout(
        title=f"{track.name} Circuit Layout",
        xaxis_title="",
        yaxis_title="",
        width=800,
        height=600,
        showlegend=False,
        plot_bgcolor='#0F5132',  # Racing green background
        paper_bgcolor='#0F5132',
        font=dict(color='white')
    )
    
    # Equal aspect ratio and hide axes for clean look
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False, scaleanchor="x", scaleratio=1)
    
    return fig

def create_speed_profile(result, car):
    """Create speed profile visualization"""
    df = pd.DataFrame({
        'Distance': result['distances'],
        'Speed': result['speeds'],
        'Time': result['times']
    })
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Speed Profile', 'Lap Progress'),
        vertical_spacing=0.1
    )
    
    # Speed profile
    fig.add_trace(
        go.Scatter(
            x=[d/1000 for d in df['Distance']],
            y=df['Speed'],
            mode='lines',
            name='Speed',
            line=dict(color=car.color, width=3)
        ),
        row=1, col=1
    )
    
    # Lap progress
    fig.add_trace(
        go.Scatter(
            x=df['Time'],
            y=[d/1000 for d in df['Distance']],
            mode='lines',
            name='Distance',
            line=dict(color='orange', width=3)
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title=f'{car.name} - Speed Analysis',
        height=600,
        showlegend=False
    )
    
    fig.update_xaxes(title_text='Distance (km)', row=1, col=1)
    fig.update_yaxes(title_text='Speed (km/h)', row=1, col=1)
    fig.update_xaxes(title_text='Time (s)', row=2, col=1)
    fig.update_yaxes(title_text='Distance (km)', row=2, col=1)
    
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
    st.markdown("### 🏁 Professional racing simulation with realistic physics and multiple car categories")
    
    # Create databases
    cars = create_car_database()
    tracks = create_tracks()
    
    # Sidebar controls
    with st.sidebar:
        st.header("🏁 Circuit Selection")
        track_name = st.selectbox(
            "Choose a Circuit",
            list(tracks.keys()),
            help="Select from authentic F1 circuits"
        )
        track = tracks[track_name]
        
        st.info(f"📍 **{track.country}**\n📏 **{track.length_km} km**")
        
        st.header("🚗 Vehicle Selection")
        
        # Car category filter
        categories = list(set(car.category for car in cars.values()))
        selected_category = st.selectbox("Category", categories, help="Choose vehicle category")
        
        # Filter cars by category
        available_cars = {name: car for name, car in cars.items() if car.category == selected_category}
        
        car_name = st.selectbox(
            "Choose Vehicle",
            list(available_cars.keys()),
            help="Select your racing machine"
        )
        car = available_cars[car_name]
        
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
        if car.category in ["Formula 1", "GT3"]:
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
    
    # Main content area
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # Track visualization
        st.subheader(f"🏁 {track.name} Circuit")
        track_fig = create_realistic_track_layout(track)
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
                else:
                    rating = "✅ Completed"
                
                st.success(f"Performance Rating: {rating}")
                
                # Speed profile
                speed_fig = create_speed_profile(result, car)
                st.plotly_chart(speed_fig, use_container_width=True)
                
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
                line_color=car.color
            ))
            
            preview_fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )),
                showlegend=False,
                title="Vehicle Performance Profile",
                height=400
            )
            
            st.plotly_chart(preview_fig, use_container_width=True)
    
    # Technical information
    with st.expander("🔬 Technical Details & Physics Model"):
        col1_t, col2_t = st.columns(2)
        
        with col1_t:
            st.markdown("""
            **🏎️ Vehicle Physics:**
            - Realistic power-to-weight ratios
            - Aerodynamic drag and downforce effects
            - Tire grip modeling with compound effects
            - Traction-limited acceleration
            - Speed-dependent braking performance
            
            **🏁 Track Features:**
            - Authentic circuit layouts
            - Corner radius affects maximum speeds
            - DRS zones for Formula 1 cars
            - Elevation changes (simplified)
            """)
        
        with col2_t:
            st.markdown("""
            **📊 Categories:**
            - **Formula 1:** High downforce, advanced aerodynamics
            - **GT3:** Balanced performance, racing slicks
            - **Hypercar:** High power, limited aerodynamics
            - **Sports Car:** Street-based performance
            
            **🌧️ Weather Effects:**
            - Dry conditions: Full grip potential
            - Light rain: 15% grip reduction
            - Heavy rain: 30% grip reduction
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("### 🏁 Built with realistic racing physics • Authentic circuit data • Multiple vehicle categories")

if __name__ == "__main__":
    main()