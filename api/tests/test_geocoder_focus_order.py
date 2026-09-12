import json
from unittest.mock import patch
from utils.geo import geocoder
class R:
 def __init__(self,p): self.p=p
 def __enter__(self): return self
 def __exit__(self,*a): return False
 def read(self): return json.dumps(self.p).encode()
def f(label,lat,lon,country="France"):
 return {"properties":{"label":label,"country":country},"geometry":{"coordinates":[lon,lat]}}
def test_focus_reorders_homonyms_by_distance(monkeypatch):
 monkeypatch.setattr("utils.geo._ors_api_key",lambda:"key")
 payload={"features":[f("Vinca, Tanzania",-8.1,35.2,"Tanzania"),f("Vinça, Pyrénées-Orientales, France",42.6456,2.5285)]}
 with patch("utils.geo.urllib.request.urlopen",return_value=R(payload)):
  places=geocoder("Vinça",focus_lat=42.6711,focus_lon=2.6203)
 assert places[0]["pays"]=="France"
 assert places[0]["latitude"]==42.6456
def test_no_focus_keeps_provider_order(monkeypatch):
 monkeypatch.setattr("utils.geo._ors_api_key",lambda:"key")
 payload={"features":[f("A",0,0),f("B",1,1)]}
 with patch("utils.geo.urllib.request.urlopen",return_value=R(payload)):
  places=geocoder("test")
 assert [p["nom"] for p in places]==["A","B"]
