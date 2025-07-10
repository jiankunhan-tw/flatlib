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
    date: str = Query(...),
    time: str = Query(...),
    lat: str = Query(...),
    lon: str = Query(...)
):
    try:
        dt = Datetime(date, time, '+08:00')
        pos = GeoPos(lat.lower(), lon.lower())
        chart = Chart(dt, pos)

        planets = {}
        classical_planets = [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN]

        for obj in classical_planets:
            planet = chart.get(obj)
            planets[obj] = {
                "sign": planet.sign,
                "lon": planet.lon,
                "lat": planet.lat,
                "house": getattr(planet, 'house', None)
            }

        return {"status": "success", "planets": planets}

    except Exception as e:
        return {"status": "error", "message": str(e)}
