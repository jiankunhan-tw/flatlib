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
    date: str = Query(...),      # YYYY-MM-DD
    time: str = Query(...),      # HH:MM
    lat: str = Query(...),       # e.g. 25n02
    lon: str = Query(...)        # e.g. 121e31
):
    try:
        dt = Datetime(date, time, '+08:00')
        pos = GeoPos(lat.lower(), lon.lower())
        chart = Chart(dt, pos)

        # 定義完整星體清單（包含外行星）
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
