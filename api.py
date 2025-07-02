from fastapi import FastAPI
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

app = FastAPI()

@app.get("/chart")
def get_chart():
    date = Datetime('2022-07-01', '12:00', '+00:00')
    pos = GeoPos('40n42', '74w00')
    chart = Chart(date, pos)
    return {"sun": str(chart.get("SUN"))}
