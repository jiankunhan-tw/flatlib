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
    lat: float = Query(...),   # 緯度，例如 24.968371
    lon: float = Query(...)    # 經度，例如 121.438034
):
    try:
        dt = Datetime(date, time, '+08:00')

        # 將經緯度從 float 轉為 flatlib 格式（例如 25n02、121e31）
        def decimal_to_dms_str(value, is_lat=True):
            degrees = abs(int(value))
            minutes = int(abs(value - int(value)) * 60)
            direction = (
                'n' if is_lat and value >= 0 else
                's' if is_lat and value < 0 else
                'e' if not is_lat and value >= 0 else
                'w'
            )
            return f"{degrees}{direction}{minutes:02}"

        lat_str = decimal_to_dms_str(lat, is_lat=True)
        lon_str = decimal_to_dms_str(float(lon), is_lat=False)

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
