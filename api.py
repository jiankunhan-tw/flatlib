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
        dt = Datetime(f"{date}", f"{time}", tz)
        pos = GeoPos(float(lat), float(lon))  # ✅ 強制轉 float

        chart = Chart(dt, pos)

        # 回傳所有行星資訊
        body_data = {}
        for body in const.LIST_OBJECTS:
            obj = chart.get(body)
            body_data[body] = {
                "sign": obj.sign,
                "lon": obj.lon,
                "lat": obj.lat,
                "speed": obj.speed
            }

        # 回傳所有宮位資訊
        house_data = {}
        for i in range(1, 13):
            house = chart.houses.get(f"H{i}")
            house_data[f"H{i}"] = {
                "sign": house.sign,
                "lon": house.lon
            }

        return {
            "status": "success",
            "datetime": str(dt),
            "location": str(pos),
            "bodies": body_data,
            "houses": house_data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
