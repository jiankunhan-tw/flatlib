from fastapi import FastAPI, Query
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.const import ALL_BODIES, HOUSES

app = FastAPI()

# 經緯度格式轉換工具：例如 24.98 -> 24n59
def decimal_to_geo_string(value: float, direction: str) -> str:
    deg = int(abs(value))
    minutes = int(round((abs(value) - deg) * 60))
    return f"{deg}{direction}{minutes:02d}"

@app.get("/chart")
def get_full_chart(
    lat: float = Query(...),
    lon: float = Query(...),
    date: str = Query('1995-04-04'),
    time: str = Query('11:30'),
    tz: str = Query('+08:00')
):
    # 經緯度處理
    lat_dir = 'n' if lat >= 0 else 's'
    lon_dir = 'e' if lon >= 0 else 'w'
    lat_str = decimal_to_geo_string(lat, lat_dir)
    lon_str = decimal_to_geo_string(lon, lon_dir)

    # 命盤基本資料
    dt = Datetime(date, time, tz)
    pos = GeoPos(lat_str, lon_str)
    chart = Chart(dt, pos)

    # 所有星體位置
    bodies = {
        body: {
            "sign": chart.get(body).sign,
            "lon": chart.get(body).lon,
            "lat": chart.get(body).lat,
            "speed": chart.get(body).speed
        } for body in ALL_BODIES
    }

    # 所有宮位位置（含主星與起始度數）
    houses = {
        house: {
            "sign": chart.houses.get(house).sign,
            "lon": chart.houses.get(house).lon
        } for house in HOUSES
    }

    return {
        "datetime": str(dt),
        "location": str(pos),
        "bodies": bodies,
        "houses": houses
    }
