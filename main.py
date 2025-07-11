from fastapi import FastAPI, Query
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Flatlib API is running!"}

@app.get("/chart")
def get_chart(
    date: str = Query(...),    # YYYY-MM-DD
    time: str = Query(...),    # HH:MM
    lat: str = Query(...),     # 緯度
    lon: str = Query(...)      # 經度
):
    try:
        dt = Datetime(date, time, '+08:00')

        def parse_coord(val: str, is_lat=True):
            if any(c.isalpha() for c in val):
                return val.lower()
            else:
                val = float(val)
                deg = abs(int(val))
                minutes = int((abs(val) - deg) * 60)
                direction = (
                    'n' if is_lat and val >= 0 else
                    's' if is_lat and val < 0 else
                    'e' if not is_lat and val >= 0 else
                    'w'
                )
                return f"{deg}{direction}{minutes:02}"

        lat_str = parse_coord(lat, is_lat=True)
        lon_str = parse_coord(lon, is_lat=False)

        pos = GeoPos(lat_str, lon_str)
        chart = Chart(dt, pos)

        star_list = [
            const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
            const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO
        ]

        planet_names = {
            const.SUN: "太陽", const.MOON: "月亮", const.MERCURY: "水星", const.VENUS: "金星",
            const.MARS: "火星", const.JUPITER: "木星", const.SATURN: "土星",
            const.URANUS: "天王星", const.NEPTUNE: "海王星", const.PLUTO: "冥王星"
        }

        planets = {}
        for obj in star_list:
            try:
                planet = chart.get(obj)
                house = chart.houseOf(planet)  # ✅ 宮位
                planets[obj] = {
                    "zh": planet_names.get(obj, obj),
                    "sign": planet.sign,
                    "lon": planet.lon,
                    "lat": planet.lat,
                    "house": house
                }
            except Exception as inner:
                planets[obj] = {"error": str(inner)}

        return {
            "status": "success",
            "placidus": True,
            "tropical": True,
            "planets": planets
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
