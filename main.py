from fastapi import FastAPI, Query
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = FastAPI()

# 英文星座 → 中文對照表
sign_map = {
    'Aries': '牡羊座',
    'Taurus': '金牛座',
    'Gemini': '雙子座',
    'Cancer': '巨蟹座',
    'Leo': '獅子座',
    'Virgo': '處女座',
    'Libra': '天秤座',
    'Scorpio': '天蠍座',
    'Sagittarius': '射手座',
    'Capricorn': '摩羯座',
    'Aquarius': '水瓶座',
    'Pisces': '雙魚座'
}

@app.get("/")
def root():
    return {"message": "Flatlib API is running!"}

@app.get("/chart")
def get_chart(
    date: str = Query(...),    # YYYY-MM-DD
    time: str = Query(...),    # HH:MM
    lat: str = Query(...),     # 緯度，可為 float 或 '25n02'
    lon: str = Query(...)      # 經度，可為 float 或 '121e31'
):
    try:
        dt = Datetime(date, time, '+08:00')

        def parse_coord(val: str, is_lat=True):
            if any(c.isalpha() for c in val):  # 已是 flatlib 格式
                return val.lower()
            else:
                val = float(val)
                deg = abs(int(val))
                minutes = int((abs(val) - deg) * 60)
                direction = (
                    'n' if is_lat and val >= 0 else
                    's' if is_lat and val < 0 else
                    'e' if not is_lat and val >= 0 else
                    'w'
                )
                return f"{deg}{direction}{minutes:02}"

        lat_str = parse_coord(lat, is_lat=True)
        lon_str = parse_coord(lon, is_lat=False)

        # ⚠️ 指定使用 placidus 宮位制
        pos = GeoPos(lat_str, lon_str)
        chart = Chart(dt, pos, hsys=const.HOUSES_PLACIDUS)

        star_list = [
            const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
            const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO
        ]

        planets = {}
        for obj in star_list:
            try:
                planet = chart.get(obj)
                planets[obj] = {
                    "星座": sign_map.get(planet.sign, planet.sign),
                    "宮位": planet.house  # 宮位號碼（1～12）
                }
            except Exception as inner:
                planets[obj] = {"error": str(inner)}

        return {
            "status": "success",
            "placidus": True,
            "tropical": True,
            "planets": planets
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
