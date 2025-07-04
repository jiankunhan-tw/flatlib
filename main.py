from fastapi import FastAPI
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const  # ✅ 用新版 flatlib 的方式

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Flatlib API is running!"}

@app.get("/chart")
def get_chart(date: str, time: str, lat: float, lon: float):
    try:
        dt = Datetime(date, time, '+08:00')
        pos = GeoPos(str(lat), str(lon))
        chart = Chart(dt, pos, hsys=const.PLACIDUS, IDs=const.TROPICAL)  # ✅ 用 const.PLACIDUS 等
        planets = {obj.id: chart[obj.id].sign for obj in chart.objects}
        return {"status": "success", "planets": planets}
    except Exception as e:
        return {"status": "error", "message": str(e)}
