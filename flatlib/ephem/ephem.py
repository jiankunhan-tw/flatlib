from fastapi import FastAPI, Query
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib.ephem import ephem  # ✅ 正確引用 flatlib 的 ephem 模組

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Flatlib API is running!"}


@app.get("/chart")
def get_chart(
    date: str = Query(...),    # YYYY-MM-DD
    time: str = Query(...),    # HH:MM
    lat: float = Query(...),
    lon: float = Query(...)
):
    try:
        dt = Datetime(date, time, '+08:00')

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
        lon_str = decimal_to_dms_str(lon, is_lat=False)

        pos = GeoPos(lat_str, lon_str)
        chart = Chart(dt, pos)

        star_list = [
            const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
            const.JUPITER, const.SATURN
        ]

        # 內行星用 chart 拿
        planets = {}
        for obj in star_list:
            planet = chart.get(obj)
            planets[obj] = {
                "sign": planet.sign,
                "lon": planet.lon,
                "lat": planet.lat,
                "house": getattr(planet, 'house', None)
            }

        # 外行星：Uranus, Neptune, Pluto（用 ephem.getObject）
        for outer in ['Uranus', 'Neptune', 'Pluto']:
            try:
                planet = ephem.getObject(outer, dt, pos)
                planets[outer] = {
                    "sign": planet.sign,
                    "lon": planet.lon,
                    "lat": planet.lat,
                    "house": None  # 外行星無 house
                }
            except Exception as e:
                planets[outer] = {"error": str(e)}

        return {
            "status": "success",
            "placidus": True,
            "tropical": True,
            "planets": planets
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
