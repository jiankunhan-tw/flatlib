from fastapi import FastAPI, Query
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import HOUSES_PLACIDUS, ZODIAC_TROPICAL

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
        chart = Chart(dt, pos, hsys=HOUSES_PLACIDUS, IDs=ZODIAC_TROPICAL)

        planets = {obj.id: chart[obj.id].sign for obj in chart.objects}
        return {"status": "success", "planets": planets}
    except Exception as e:
        return {"status": "error", "message": str(e)}
