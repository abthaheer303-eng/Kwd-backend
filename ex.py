import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import os
import random, time


app = FastAPI()

# ALLOW STREAMLIT CALL TO  API

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

API_KEY = os.getenv("Exchange API_KEY", "1010d89bb4ecae457459e4d4")





@app.get("/predict")
def predict():
    
    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        res =  requests.get(url, timeout=10).json()
        data = res['conversion_rates']
        
        kwd_per_usd = data['KWD']
        
        base = {
            "USD": round(1 / kwd_per_usd, 2),
            "EUR": round(data['EUR'] / kwd_per_usd, 2),
            "GBP": round(data['GBP'] / kwd_per_usd, 2),
            "INR": round(data['INR'] / kwd_per_usd, 2),
            "JPY": round(data['JPY'] / kwd_per_usd, 2),
        }
        live ={
            "USD": round(base["USD"] + random.uniform(-0.008, 0.008), 2),
            "EUR": round(base["EUR"] + random.uniform(-0.008, 0.008), 2),
            "GBP": round(base["GBP"] + random.uniform(-0.008, 0.008), 2),
            "INR": round(base["INR"] + random.uniform(-0.15, 0.15), 2),
            "JPY": round(base["JPY"] + random.uniform(-0.6, 0.6), 2),
        }
        return{"live_forex_rates_vs_USD": live, "source": "real-api+live-tick", "time": time.time()}
    except Exception as e:
        print("API failed, using fallback:", e)
        return {
        "live_forex_rates_vs_USD": {
            "USD":3.25,
            "EUR": round(2.99 + random.uniform(-0.05, 0.05), 2),
            "GBP": round(2.56 + random.uniform(-0.05, 0.05), 2),
            "INR": round(310.42 + random.uniform(-0.7, 0.7), 2),
        },
        "source": "fallback-random"
    }
        
@app.get("/")
def home():
    return {"status": "live api running"}

        

    

