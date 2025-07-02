from fastapi import FastAPI
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import TROPICAL, PLACIDUS

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Flatlib API is running!"}

@app.get("/chart")
def get_chart(date: str, time: str, lat: float, lon: float):
    dt = Datetime(date, time, '+08:00')
    pos = GeoPos(str(lat), str(lon))
    chart = Chart(dt, pos, hsys=PLACIDUS, IDs=TROPICAL)
    planets = {obj.id: chart[obj.id].sign for obj in chart.objects}
    return {"planets": planets}
