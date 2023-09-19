
import requests
import json

url = "https://json.freeastrologyapi.com/planets"

payload = json.dumps({
  "year": 2022,
  "month": 8,
  "date": 11,
  "hours": 6,
  "minutes": 0,
  "seconds": 0,
  "latitude": 17.38333,
  "longitude": 78.4666,
  "timezone": 5.5,
  "settings": {
    "observation_point": "topocentric",
    "ayanamsha": "lahiri"
  }
})
headers = {
  'Content-Type': 'application/json',
  'x-api-key': 'FlY7SWUJ1I7C7mEOou7ch4VynTFpFU9h4JRmKXsh'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
