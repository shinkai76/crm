#encoding=utf-8

import json
import requests


# headers = {"Token": "YzkgMnwxOjB8MTA6MTUzOTc0MDI0NXw0OnVzZXJ8NDpNakF6fDFiZWZmOTczN2Q4N2ZlMmM3MmNhNzQ2ZWY5MDdiNTFkOGNiNDFjYmQwYTI1N2FkMTg3OTZlMzE1ODI0MjE5ZWI="}
# params = {"url": "http://s05.c8erp.com:6320", "set_of_book": "c9", "user_name": "admin"}
# r = requests.get("http://192.168.2.196:8940/api/access_token", headers=headers, params=params)
# print r.text

headers = {"Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMjAzIiwidXJsIjoiaHR0cDovL3MwNS5jOGVycC5jb206NjMyMCIsImFjY2Vzc19sZXZlbCI6MTUsInRva2VuIjoiWXprZ01ud3hPakI4TVRBNk1UVXpPVGMwTURJME5YdzBPblZ6WlhKOE5EcE5ha0Y2ZkRGaVpXWm1PVGN6TjJRNE4yWmxNbU0zTW1OaE56UTJaV1k1TURkaU5URmtPR05pTkRGalltUXdZVEkxTjJGa01UZzNPVFpsTXpFMU9ESTBNakU1WldJPSIsInNldF9vZl9ib29rIjoiYzkiLCJ1c2VyX25hbWUiOiJhZG1pbiJ9.vz9PZfmrpUEkXsl0IRbpeoTDEnZAsh1PoxCryvis1Ek"}

params = {"page": 1, "per_page": 20, "category": "10730677", "start_date": "2018-9-15", "end_date": "2018-10-15", "time_type": "created_at"}

r = requests.get("http://192.168.2.196:8940/api/orders?action=get_orders", headers=headers, params=params)
print r.text

# r = requests.delete("http://192.168.2.196:8940/api/orders/3", headers=headers)
# print r.text

# r = requests.get("http://192.168.2.196:8940/api/orders/3?action=import", headers=headers)
# print r.text

# r = requests.get("http://192.168.2.196:8940/api/orders/3?action=init_order", headers=headers)
# print r.text

# r = requests.get("http://192.168.2.196:8940/api/orders/64?action=complete_download", headers=headers)
# print r.text