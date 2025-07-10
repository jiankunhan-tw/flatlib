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
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    time: str = Query(..., description="Time in HH:MM format"),
    lat: str = Query(..., description="Latitude like '24n58'"),
    lon: str = Query(..., description="Longitude like '121e26'")
):
    try:
        dt = Datetime(date, time, '+08:00')
        pos = GeoPos(lat.lower(), lon.lower())

        # ✅ 用默認設定，不使用 const.PLACIDUS、ZODIAC_TROPICAL 避免錯誤
        chart = Chart(dt, pos)

        planets = {}
        for obj in const.LIST_OBJECTS:
            planet = chart.get(obj)
            planets[obj] = {
                "sign": planet.sign,
                "lon": planet.lon,
                "lat": planet.lat,
                "house": planet.house
            }

        return {"status": "success", "planets": planets}

    except Exception as e:
        return {"status": "error", "message": str(e)}
