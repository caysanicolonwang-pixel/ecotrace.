import streamlit as st
import requests
from datetime import datetime
from streamlit_geolocation import streamlit_geolocation
def pollutant_bar(name, value, limit, description):
    pct = min(value / limit * 100, 100)
    if pct < 33:
        color = "#3E9E5A"
    elif pct < 66:
        color = "#E0B33C"
    else:
        color = "#E15C4F"
    st.markdown(f"""
    <div style='margin-bottom:6px;'>
      <b>{name}</b> <span style='float:right;'>{value} µg/m³</span>
    </div>
    <div style='background:#EDEDED; height:8px; border-radius:4px; overflow:hidden;'>
      <div style='background:{color}; width:{pct}%; height:100%;'></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(description)
def aqi_ring(aqi, category, color, city, pm25, timestamp):
    pct = min(aqi / 300, 1.0)
    circumference = 2 * 3.14159 * 70
    filled = circumference * pct
    st.markdown(f"""<div style='display:flex; align-items:center; gap:40px;'>
<svg width="180" height="180" viewBox="0 0 180 180">
<circle cx="90" cy="90" r="70" fill="none" stroke="#EDF0F2" stroke-width="14"/>
<circle cx="90" cy="90" r="70" fill="none" stroke="{color}" stroke-width="14"
stroke-linecap="round" stroke-dasharray="{filled} {circumference}"
transform="rotate(-90 90 90)"/>
<text x="90" y="92" text-anchor="middle" font-size="46" fill="#2C3338">{aqi}</text>
<text x="90" y="115" text-anchor="middle" font-size="11" fill="#8A9299" letter-spacing="2">US AQI</text>
</svg>
<div>
<div style='color:#8A9299; font-size:13px; letter-spacing:2px;'>{city.upper()}</div>
<div style='color:{color}; font-size:30px; margin:6px 0 12px 0;'>{category}</div>
<div style='color:#5C6866;'>Fine particles are at {pm25} µg/m³ right now. As of {timestamp}.</div>
</div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:left; padding:20px 0 30px 0;'>
  <h1 style='font-family:Poppins, sans-serif; font-size:44px; font-weight:600; margin:0; line-height:1.2;'>
    Understand your air. Enjoy your outdoors.
  </h1>
  <p style='font-family:Poppins, sans-serif; font-size:19px; color:#5C6866; margin:14px 0 0 0; line-height:1.5;'>
    Live air quality for every US state, personalized for your health and your outdoor plans.
  </p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600;700&display=swap');
html, body, .stApp, .stApp * { font-family: Georgia, serif !important; }
.stButton button p { white-space: pre-line !important; text-align: center; }
.wordmark { font-family: Outfit, sans-serif !important; }
div[role="radiogroup"] { background:#F0F2F5; border-radius:999px; padding:4px; display:inline-flex !important; flex-direction:row !important; gap:0; width:auto !important; }
div[role="radiogroup"] > label { border-radius:999px; padding:6px 20px !important; margin:0 !important; cursor:pointer; display:flex !important; align-items:center; }
div[role="radiogroup"] > label p { color:#8A9299 !important; margin:0 !important; }
div[role="radiogroup"] > label:has(input:checked) { background:#1A1D21; }
div[role="radiogroup"] > label:has(input:checked) p { color:#FFFFFF !important; }
</style>
""", unsafe_allow_html=True)
cities = {
    "Alabama": ["Birmingham", "Montgomery", "Mobile", "Huntsville","Tuscaloosa"],
    "Alaska": ["Anchorage", "Fairbanks", "Juneau","Badger","North Lakes"],
    "Arizona": ["Phoenix", "Tucson", "Mesa", "Flagstaff","Gilbert"],
    "Arkansas": ["Little Rock", "Fayetteville", "Fort Smith","Springdale","Jonesboro"],
    "California": ["Los Angeles", "San Francisco", "San Diego", "Sacramento","San Jose"],
    "Colorado": ["Denver", "Aurora", "Colorado Springs","Fort Collins","Lakewood"],
    "Connecticut": ["Bridgeport","New Haven","Stamford","Hartford","Waterbury"],
    "Delaware": ["Wilmington","Dover","Newark","Middletown","Bear"],
    "Florida":["Jacksonville","Miami","Tampa","Orlando","Cape Coral"],
    "Georgia":["Atlanta","Augusta","Columbus","Savannah","Athens"],
    "Hawaii":["Honolulu","East Honolulu","Hilo","Pearl City","Waipahu"],
    "Idaho":["Boise","Meridian","Nampa","Caldwell","Idaho Falls"],
    "Illinois":["Chicago","Naperville","Joliet","Rockford","Elgin"],
    "Indiana":["Indianapolis","Fort Wayne","Evansville","Carmel","Fishers"],
    "Iowa":["Des Moines","Cedar Rapids","Davenport","Sioux City","Ankeny"],
    "Kansas":["Wichita","Overland Park","Kansas City","Olathe","Topeka"],
    "Kentucky":["Louisville","Lexington","Bowling Green","Owensboro","Covington"],
    "Louisiana":["New Orleans","Baton Rouge","Shreveport","Metairie","Lafayette"],
    "Maine":["Portland","Lewiston","Bangor","South Portland","Auburn"],
    "Maryland":["Baltimore","Columbia","Frederick","Germantown","Waldorf"],
    "Massachusetts":["Boston","Worcester","Springfield","Cambridge","Lowell"],
    "Michigan":["Detroit","Grand Rapids","Warren","Sterling Heights","Ann Arbor"],
    "Minnesota":["Minneapolis","Woodbury","Bloomington","Duluth","Brooklyn Park"],
    "Mississippi":["Jackson","Gulfport","Southaven","Biloxi","Hattiesburg"],
    "Missouri":["Kansas City","Saint Louis","Springfield","Independence","Lee's Summit"],
    "Montana":["Billings","Missoula","Great Falls","Bozeman","Helena"],
    "Nebraska":["Omaha","Lincoln","Bellevue","Grand Island","Kearney"],
    "Nevada":["Las Vegas","Henderson","North Las Vegas","Reno","Sparks"],
    "New Hampshire":["Manchester","Nashua","Concord","Derry","Salem",],
    "New Jersey":["Newark","Jersey City","Paterson","Lakewood","Elizabeth"],
    "New Mexico":["Albuquerque","Las Cruces","Rio Rancho","Santa Fe","Roswell"],
    "New York":["New York City","Buffalo","Yonkers","Rochester","Syracuse"],
    "North Carolina":["Charlotte","Raleigh","Greensboro","Durham","Winston-Salem"],
    "North Dakota":["Fargo","Bismarck","Grand Forks","Minot","West Fargo"],
    "Ohio":["Columbus","Cleveland","Cincinnati","Toledo","Akron"],
    "Oklahoma":["Oklahoma City","Tulsa","Norman","Broken Arrow","Edmond"],
    "Oregon":["Portland","Salem","Eugene","Hillsboro","Gresham"],
    "Pennsylvania":["Philadelphia","Pittsburgh","Allentown","Reading","Erie"],
    "Rhode Island":["Providence","Cranston","Warwick","Pawtucket","East Providence"],
    "South Carolina":["Charleston","North Charleston","Mount Pleasant","Rock Hill","Greenville"],
    "South Dakota":["Sioux Falls","Rapid City","Aberdeen","Brookings","Watertown"],
    "Tennessee":["Nashville","Memphis","Knoxville","Chattanooga","Clarksville"],
    "Texas":["Houston","San Antonio","Dallas","Fort Worth","Austin"],
    "Utah":["Salt Lake City","West Valley City","West Jordan","Provo","Saint George"],
    "Vermont":["Burlington","South Burlington","Colchester","Rutland","Bennington"],
    "Virginia":["Virginia Beach","Chesapeake","Arlington","Richmond","Norfolk"],
    "Washington":["Seattle","Tacoma","Spokane","Vancouver","Bellevue"],
    "West Virginia":["Huntington","Morgantown","Parkersburg","Wheeling","Martinsburg"],
    "Wisconsin":["Milwaukee","Madison","Green Bay","Kenosha","Racine"],
    "Wyoming":["Cheyenne","Casper","Gillette","Laramie","Rock Springs"],
}
spacer, toggle_col = st.columns([2, 1])
with toggle_col:
    section = st.radio("", ["Air", "Swim"], horizontal=True, label_visibility="collapsed")
swim_areas = {
    "Hammonasset Beach State Park": {"town": "Madison", "type": "Shoreline", "status": "OPEN", "coords": (41.2612, -72.5453)},
    "Rocky Neck State Park (West Beach)": {"town": "Niantic", "type": "Shoreline", "status": "CLOSED", "coords": (41.3037, -72.2456)},
    "Sherwood Island State Park": {"town": "Westport", "type": "Shoreline", "status": "OPEN", "coords": (41.1181, -73.3298)},
    "Silver Sands State Park": {"town": "Milford", "type": "Shoreline", "status": "OPEN", "coords": (41.1901, -73.0640)},
"Black Rock State Park": {"town": "Watertown", "type": "Lake", "status": "OPEN"},
    "Burr Pond State Park": {"town": "Torrington", "type": "Lake", "status": "OPEN"},
    "Chatfield Hollow State Park": {"town": "Killingworth", "type": "Lake", "status": "OPEN"},
    "Cockaponset State Forest (Pattaconk)": {"town": "Chester", "type": "Lake", "status": "OPEN"},
    "Day Pond State Park": {"town": "Colchester", "type": "Lake", "status": "OPEN"},
    "Gardner Lake State Park": {"town": "Salem", "type": "Lake", "status": "OPEN"},
    "Gay City State Park": {"town": "Hebron", "type": "Lake", "status": "OPEN"},
    "Hopeville Pond State Park": {"town": "Griswold", "type": "Lake", "status": "OPEN"},
    "Indian Well State Park": {"town": "Shelton", "type": "Lake", "status": "OPEN"},
    "Lake Waramaug State Park": {"town": "Kent", "type": "Lake", "status": "OPEN"},
    "Mount Tom State Park": {"town": "Litchfield", "type": "Lake", "status": "OPEN"},
    "Pachaug State Forest (Green Falls Pond)": {"town": "Voluntown", "type": "Lake", "status": "OPEN"},
    "Quaddick State Park": {"town": "Thompson", "type": "Lake", "status": "OPEN"},
    "Squantz Pond State Park": {"town": "New Fairfield", "type": "Lake", "status": "OPEN"},
    "Stratton Brook State Park": {"town": "Simsbury", "type": "Lake", "status": "OPEN"},
    "Wadsworth Falls State Park": {"town": "Middlefield", "type": "Lake", "status": "OPEN"},
    "Wharton Brook State Park": {"town": "Wallingford", "type": "Lake", "status": "OPEN"},
}

SAMPLE_DATE = "September 4, 2026"
if section == "Air":
    tab1, tab2, tab3 = st.tabs(["Plan", "Learn", "About"])
    with tab2:
        st.markdown("#### How air changes through the day:")

        hour_labels = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM",
                       "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM",
                       "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"]

        time_label = st.select_slider("Time of day", options=hour_labels, value="12 PM")
        time_of_day = hour_labels.index(time_label)

        if time_of_day < 6:
            st.write("At night, the air near the ground can become trapped under warmer air. This is called a temperature inversion. When this happens, pollution from cars, fires, and other sources can stay close to the ground instead of spreading out. Ozone is also usually low at night. Without sunlight, new ozone cannot form. But there is another reason ozone can disappear quickly. Nitrogen oxide (NO) from cars can react with ozone and use it up. This reaction is called ozone titration.")
            st.info("**What this means for you**: The best time to go outside depends on the pollutants in your area. Low ozone at night does not always mean the overall air is clean.")
        elif time_of_day < 10:
            st.write("Morning traffic can send more nitrogen dioxide (NO₂) and tiny particles into the air. If a temperature inversion is still happening, these pollutants can become trapped near the ground. As the sun warms the ground, the air usually begins to mix more. This can help spread out some pollution, but traffic emissions may still make the air less clean.")
            st.info ("**What this means for you**: This is why your cleanest hour is rarely at 8 AM, even though the air may feel fresh.")
        elif time_of_day < 16:
            st.write("Sunlight changes the air in an important way. It helps chemicals from cars, factories, and other sources react and form ground-level ozone. Ozone is not usually released directly. It is made in the air through chemical reactions involving nitrogen oxides and other chemicals called VOCs. This process is called photochemical smog. Ozone often reaches its highest levels in the afternoon, especially on hot, sunny days.")
            st.info("**What this means for you**: This is why the app may suggest waiting until evening on hot, sunny days if ozone is the main problem.")
        elif time_of_day < 20:
            st.write("Traffic becomes heavier again during the evening. This can raise nitrogen dioxide and particle pollution. At the same time, the sun is getting lower, so less new ozone is being formed. Ozone can also be used up by fresh pollution from traffic. This means two pollutants can move in opposite directions: NO₂ can rise while ozone falls.")
            st.info("**What this means for you**: An evening hour can be better for ozone but worse for traffic-related pollution. This app looks at all the pollutants together instead of assuming one time is always best.")
        else:
            st.write("After sunset, ozone levels usually continue to drop because there is no sunlight to keep forming it. The air can also begin to settle closer to the ground. During colder months, wood smoke and other particles can build up when there is little wind. The exact pattern depends on the weather, location, and sources of pollution nearby.")
            st.info("**What this means for you**: A low ozone reading at night does not automatically mean the air is clean. Your best time to go outside depends on which pollutants are present and how the weather is moving them.")
        with tab3:
            st.subheader("Where the numbers come from")
            st.write("""
        Air quality readings come from Open-Meteo's air quality API, which provides hourly
        forecasts for any location. Breathing rates by activity come from the EPA Exposure
        Factors Handbook. The daily reference intake is derived from the WHO 24-hour PM2.5
        guideline of 15 µg/m³ multiplied by a typical adult's daily air intake of about
        16 cubic metres, giving roughly 240 micrograms per day.
        """)

            st.subheader("How exposure is calculated")
            st.write("""
        Most air quality apps report the concentration of pollution in the air. That describes
        the air, not the person breathing it. How much pollution actually reaches your lungs
        depends on how hard you are breathing and for how long.
    
        The calculation works in three steps. Your breathing rate in litres per minute is
        converted to cubic metres per hour. That is multiplied by your session length to get
        the total volume of air you move through your lungs. That volume is multiplied by the
        PM2.5 concentration to get micrograms inhaled.
        """)

            st.subheader("Limitations")
            st.write("""
        Forecast data is an estimate and gets less reliable further ahead. The dose calculation
        uses PM2.5 only, though other pollutants matter too. Breathing rates vary between
        individuals. This is a planning tool for informational purposes, not a medical
        measurement or diagnosis.
        """)

    with tab1:
        use_location = st.toggle("Use my location")

        if use_location:
            coords = streamlit_geolocation()
            if coords and coords.get("latitude"):
                lat = coords["latitude"]
                lon = coords["longitude"]
                location = None
            else:
                st.info("Click the location button above to allow access!")
                st.stop()
        else:
            state_col, city_col = st.columns(2)
            with state_col:
                state = st.selectbox("State:", ["None selected"] + list(cities.keys()))
            with city_col:
                if state == "None selected":
                    city = st.selectbox("City", ["None selected"])
                else:
                    city = st.selectbox("City", ["None selected"] + cities[state])

            custom = st.text_input("Don't see your city? Search here:", placeholder="e.g. Los Angeles, California")

            if custom:
                location = custom
            elif city != "None selected":
                location = f"{city}, {state}"
            else:
                st.info("Pick a state and city above, or search for your city.")
                st.stop()

        if location is not None:
            g = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&country_code=US")

            geo = g.json()
            if "results" not in geo:
                st.error(f"Couldn't find a city called '{location}'. Check the spelling and try again.")
                st.stop()
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]
            found_name = geo["results"][0]["name"]
            found_state = geo["results"][0].get("admin1", "")
            location = f"{found_name}, {found_state}" if found_state else found_name
        if location is None:
            rev = requests.get(
                f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json",
                headers={"User-Agent": "BeaCTive-air-quality-app"}
            )
            addr = rev.json().get("address", {})
            town = addr.get("city") or addr.get("town") or addr.get("village") or "Your location"
            state_name = addr.get("state", "")
            location = f"{town}, {state_name}" if state_name else town

        r = requests.get(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5,pm10,ozone,nitrogen_dioxide,sulphur_dioxide,carbon_monoxide,us_aqi,us_aqi_pm2_5,us_aqi_pm10,us_aqi_ozone,us_aqi_nitrogen_dioxide,us_aqi_sulphur_dioxide,us_aqi_carbon_monoxide&hourly=pm2_5,us_aqi&timezone=auto")
        data = r.json()
        sub_aqi = {
            "PM2.5": data["current"]["us_aqi_pm2_5"],
            "PM10": data["current"]["us_aqi_pm10"],
            "Ozone": data["current"]["us_aqi_ozone"],
            "NO₂": data["current"]["us_aqi_nitrogen_dioxide"],
            "SO₂": data["current"]["us_aqi_sulphur_dioxide"],
            "CO": data["current"]["us_aqi_carbon_monoxide"],
        }
        driver = max(sub_aqi, key=sub_aqi.get)
        st.write("Driver:", driver, sub_aqi[driver])

        aqi = data["current"]["us_aqi"]

        if aqi <= 50:
            category = "Good"
        elif aqi <= 100:
            category = "Moderate"
        elif aqi <= 150:
            category = "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            category = "Unhealthy"
        elif aqi <= 300:
            category = "Very Unhealthy"
        else:
            category = "Hazardous"
        category_colors = {
            "Good": "#3E9E5A",
            "Moderate": "#E0A03C",
            "Unhealthy for Sensitive Groups": "#DA7434",
            "Unhealthy": "#C8452F",
            "Very Unhealthy": "#8E4585",
            "Hazardous": "#7A2230"
        }
        color = category_colors[category]
        now_label = datetime.now().strftime("%a %I %p").replace(" 0", " ")
        aqi_ring(aqi, category, color, location, data["current"]["pm2_5"], now_label)

        st.subheader("Pollutant breakdown")

        p1, p2, p3 = st.columns(3)
        with p1:
            pollutant_bar("PM2.5", data["current"]["pm2_5"], 35, "Fine soot & smoke — reaches deep into lungs")
        with p2:
            pollutant_bar("PM10", data["current"]["pm10"], 154, "Dust, pollen, road grit")
        with p3:
            pollutant_bar("Ozone", data["current"]["ozone"], 140, "Peaks on hot sunny afternoons")

        p4, p5, p6 = st.columns(3)
        with p4:
            pollutant_bar("NO₂", data["current"]["nitrogen_dioxide"], 100, "Traffic exhaust — worst near busy roads")
        with p5:
            pollutant_bar("SO₂", data["current"]["sulphur_dioxide"], 75, "Industrial burning")
        with p6:
            pollutant_bar("CO", data["current"]["carbon_monoxide"], 4000, "Combustion gas")

        st.divider()

        st.divider()
        hours = st.slider("How long will you be outside?", 0.5, 10.0, 1.0, 0.5, format="%.1f hr")

        if "activity" not in st.session_state:
            st.session_state.activity = "Walking"
        st.subheader("Your Activity")
        activity = st.session_state.activity

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚶\nWalking", type="primary" if activity == "Walking" else "secondary", use_container_width=True):
                st.session_state.activity = "Walking"
                st.rerun()
        with col2:
            if st.button("🏃\nRunning", type="primary" if activity == "Running" else "secondary", use_container_width=True):
                st.session_state.activity = "Running"
                st.rerun()
        with col3:
            if st.button("🚴\nCycling", type="primary" if activity == "Cycling" else "secondary", use_container_width=True):
                st.session_state.activity = "Cycling"
                st.rerun()

        col4, col5, col6 = st.columns(3)
        with col4:
            if st.button("🥾\nHiking", type="primary" if activity == "Hiking" else "secondary", use_container_width=True):
                st.session_state.activity = "Hiking"
                st.rerun()
        with col5:
            if st.button("🌱\nGardening", type="primary" if activity == "Gardening" else "secondary", use_container_width=True):
                st.session_state.activity = "Gardening"
                st.rerun()
        with col6:
            if st.button("⚽\nTeam sports", type="primary" if activity == "Team sports" else "secondary", use_container_width=True):
                st.session_state.activity = "Team sports"
                st.rerun()

        activity = st.session_state.activity
        sensitivity = st.selectbox("Any health conditions?", ["None", "Asthma", "Heart condition", "Child", "Over 65"])
        breathing_rates = {
            "Walking": 15,
            "Running": 45,
            "Cycling": 32,
            "Hiking": 28,
            "Gardening": 20,
            "Team sports": 38
        }
        rate = breathing_rates[activity]
        st.write("Breathing rate:", rate, "L/min")
        rate_m3 = rate * 60/1000
        st.write("Cubic metres per hour:", rate_m3)
        air_breathed = rate_m3 * hours
        st.write("Air breathed:", air_breathed, "cubic metres")
        pm25 = data["current"]["pm2_5"]
        dose = pm25 * air_breathed
        st.write("PM2.5 inhaled:", dose, "micrograms")
        percent = dose / 240 * 100
        st.write("That's", round(percent), "% of a full day's safe limit")

        sensitive = sensitivity != "None"

        if sensitive:
            aqi_level = 0 if aqi < 101 else (1 if aqi < 151 else 2)
        else:
            aqi_level = 0 if aqi < 151 else (1 if aqi < 201 else 2)

        if percent < 75:
            dose_level = 0
        elif percent < 150:
            dose_level = 1
        else:
            dose_level = 2

        level = max(aqi_level, dose_level)

        key_pollutants = {
            "None": ["PM2.5", "PM10", "Ozone", "NO₂", "SO₂", "CO"],
            "Asthma": ["Ozone", "PM2.5", "NO₂", "SO₂"],
            "Child": ["Ozone", "PM2.5", "NO₂", "SO₂"],
            "Over 65": ["Ozone", "PM2.5", "NO₂", "SO₂"],
            "Heart condition": ["PM2.5", "PM10", "CO"],
        }

        matters = driver in key_pollutants[sensitivity]

        if matters and sensitivity != "None":
            driver_note = f"{driver} is what's driving the air quality number today, and that's one of the pollutants that matters most for {sensitivity.lower()}."
        else:
            driver_note = f"{driver} is what's driving the air quality number today."

        if level == 0:
            st.success(f"#### Go ahead\n\n{driver_note} At {activity.lower()} for {hours} hours you'd take in about {round(dose)} micrograms of fine particulate — roughly {round(percent)}% of a day's reference intake.")
        elif level == 1:
            st.warning(f"#### Consider adjusting\n\n{driver_note} This session comes to about {round(percent)}% of a day's reference intake at an AQI of {aqi}. A shorter outing or a cleaner hour would cut it meaningfully.")
        else:
            st.error(f"#### Take it easy today\n\n{driver_note} This session comes to about {round(percent)}% of a day's reference intake at an AQI of {aqi}. Consider indoors, or wait for cleaner air.")

        now_hour = datetime.now().hour
        end_hour = min(now_hour + 24, len(data["hourly"]["us_aqi"]))

        st.subheader("Next 24 hours")
        chart_col, best_col = st.columns([2, 1])

        with chart_col:
            next24 = data["hourly"]["us_aqi"][now_hour:end_hour]
            st.line_chart(next24, height=250)

        with best_col:
            st.write("**Cleanest hours ahead:**")
            upcoming = []
            for i in range(now_hour, end_hour):
                upcoming.append((data["hourly"]["us_aqi"][i], data["hourly"]["time"][i]))
            upcoming.sort()
            chosen = []
            for aqi_value, time_string in upcoming:
                when = datetime.fromisoformat(time_string)
                if all(abs((when - c).total_seconds()) >= 10800 for c in chosen):
                    chosen.append(when)
                    label = when.strftime("%a %I%p").replace(" 0", " ")
                    st.write(f"{label} — AQI {aqi_value}")
                if len(chosen) == 3:
                    break
else:
    st.subheader("Connecticut swimming areas")

    kind = st.radio("", ["Shoreline", "Lake"], horizontal=True, label_visibility="collapsed")

    matching = [n for n in swim_areas if swim_areas[n]["type"] == kind]
    spot = st.selectbox("Swimming area", matching)
    info = swim_areas[spot]

    st.caption(f"{info['town']}, Connecticut")

    if kind == "Shoreline":
        blat, blon = info["coords"]
        m = requests.get(f"https://marine-api.open-meteo.com/v1/marine?latitude={blat}&longitude={blon}&current=sea_surface_temperature,wave_height&timezone=auto")
        marine = m.json()

        temp_c = marine["current"]["sea_surface_temperature"]
        waves = marine["current"]["wave_height"]
        temp_f = temp_c * 9 / 5 + 32

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Water temperature", f"{round(temp_f)}°F")
        with c2:
            st.metric("Wave height", f"{waves} m")

        w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={blat}&longitude={blon}&hourly=precipitation&past_days=2&timezone=auto")
        rain_data = w.json()["hourly"]["precipitation"]
        recent_rain = sum(rain_data[:48])

        if recent_rain > 12:
            st.warning(f"**{recent_rain:.0f} mm of rain in the last 48 hours.** Heavy rain washes bacteria into the water, so conditions right now may be worse than the last test suggests.")

    if info["status"] == "OPEN":
        st.success("**Open** — bacteria levels were within safe limits at the last test.")
    else:
        st.error("**Closed** — bacteria levels exceeded safe limits at the last test.")

    st.caption(f"Tested by CT DEEP on {SAMPLE_DATE}. Testing runs weekly from Memorial Day to Labor Day.")

    with st.expander("What is being tested?"):
        st.markdown("""
**What is Enterococcus?**

Enterococcus is a type of bacteria that lives in the intestines of people and animals. Finding it in water can be a sign that other harmful germs may be present too.

**Why test for it?**

There are too many possible harmful germs to test for one by one. Enterococcus gives scientists a quick and practical way to check whether water may have been contaminated.

**Why test weekly?**

Testing requires growing the bacteria in a lab, which takes about 24 hours. This means there is no instant test, so water is usually tested on a regular schedule.

**What causes spikes?**

Heavy rain can wash sewage, animal waste, and other pollution into the water. Sewage overflows and other sources can also cause Enterococcus levels to rise.
""")