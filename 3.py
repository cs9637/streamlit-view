import streamlit as st
import requests

# OpenWeatherMap API URL 및 API 키
AIR_QUALITY_API_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"
API_KEY = "04d2f3cc48621a3afcc039c743653ef2"  # 발급받은 OpenWeatherMap API 키를 입력하세요

def get_air_quality_status(pm10, pm25):
    # PM10 기준
    if pm10 <= 30:
        pm10_status = "좋음"
    elif pm10 <= 80:
        pm10_status = "보통"
    elif pm10 <= 150:
        pm10_status = "나쁨"
    else:
        pm10_status = "매우 나쁨"

    # PM2.5 기준
    if pm25 <= 15:
        pm25_status = "좋음"
    elif pm25 <= 35:
        pm25_status = "보통"
    elif pm25 <= 75:
        pm25_status = "나쁨"
    else:
        pm25_status = "매우 나쁨"

    return pm10_status, pm25_status

# 지역 이름으로 위도와 경도 가져오기
def get_coordinates(city_name, country_code="KR"):
    params = {
        "q": city_name,
        "limit": 1,  # 가장 일치하는 결과 1개만 반환
        "appid": API_KEY
    }
    response = requests.get(GEOCODING_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            return None, None
    else:
        return None, None

# Streamlit 웹 인터페이스
st.title("실시간 미세먼지/초미세먼지 정보")

# 사용자 입력
city_name = st.text_input("대한민국 지역 이름을 입력하세요 (예: Seoul): ")

if city_name:
    # 지역의 위도와 경도 가져오기
    latitude, longitude = get_coordinates(city_name)

    if latitude and longitude:
        # 대기질 데이터 요청
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": API_KEY
        }
        response = requests.get(AIR_QUALITY_API_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            components = data["list"][0]["components"]
            
            # 미세먼지(PM10) 및 초미세먼지(PM2.5) 농도
            pm10 = components["pm10"]
            pm25 = components["pm2_5"]

            # 대기질 상태 평가
            pm10_status, pm25_status = get_air_quality_status(pm10, pm25)

            # 결과 출력
            st.markdown(f"### 지역: {city_name}")
            st.markdown(f"- **미세먼지(PM10):** {pm10} µg/m³ ({pm10_status})")
            st.markdown(f"- **초미세먼지(PM2.5):** {pm25} µg/m³ ({pm25_status})")
        else:
            st.error("대기질 데이터를 가져오지 못했습니다. 다시 시도하세요.")
    else:
        st.error("입력한 지역을 찾을 수 없습니다. 다시 입력하세요.")