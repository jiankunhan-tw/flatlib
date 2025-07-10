from fastapi import FastAPI, Query
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = FastAPI()

@app.get("/chart")
def get_chart(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    time: str = Query(..., description="Time in HH:MM format"),
    tz: str = Query("+08:00", description="Timezone offset"),
    lat: float = Query(..., description="Latitude as float"),
    lon: float = Query(..., description="Longitude as float")
):
    try:
        # ✅ 正確轉換為 float，不做 int()
        dt = Datetime(date, time, tz)
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos)

        body_data = {}
        for body in const.LIST_OBJECTS:
            obj = chart.get(body)
            body_data[body] = {
                "sign": obj.sign,
                "lon": obj.lon,
                "lat": obj.lat,
                "speed": obj.speed,
                "house": obj.house
            }

        return {"status": "ok", "chart": body_data}

    except Exception as e:
        return {"status": "error", "message": str(e)}
