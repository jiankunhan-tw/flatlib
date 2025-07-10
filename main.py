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
    date: str = Query(...),     # YYYY-MM-DD
    time: str = Query(...),     # HH:MM
    lat: str = Query(...),      # 經緯度現在改為字串型別
    lon: str = Query(...)
):
    try:
        dt = Datetime(date, time, '+08:00')

        # 判斷是否是純 float，如果是就轉為 flatlib 格式
        def parse_coord(val: str, is_lat=True):
            if any(c.isalpha() for c in val):
                # 已是 flatlib 格式（如 25n02）
                return val.lower()
            else:
                # 是小數格式，要轉成 flatlib 格式
                val = float(val)
                deg = abs(int(val))
                minutes = int(abs(val - deg) * 60)
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

        planets = {}
        for obj in star_list:
            planet = chart.get(obj)
            planets[obj] = {
                "sign": planet.sign,
                "lon": planet.lon,
                "lat": planet.lat,
                "house": getattr(planet, 'house', None)
            }

        return {
            "status": "success",
            "placidus": True,
            "tropical": True,
            "planets": planets
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
