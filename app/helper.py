from typing import Literal, Optional
import requests
from uuid import UUID

QUESTION = "/comm"
SPECIAL_DAY = "/specialDay?month=7&day=17"

def get_message(id: UUID, text: Optional[str] = None, type: Literal["QUESTION", "SPECIAL_DAY"] = "QUESTION"):
    URL = "http://172.18.14.213:8080/be/v1/careu/" + id
    try:
        if type == "SPECIAL_DAY":
            response = requests.get(url=URL+SPECIAL_DAY, params={"month":7, "day":17})
            if response.status_code == 200:
                return response.json()["special_days"]
        else:
            response = requests.post(url=URL+QUESTION, json={"message": text})
            if response.status_code == 200:
                response_data = response.json()["result"]["responses"]
                return [obj["response"] for obj in response_data]
    except Exception:
        return ["Vui lòng kiểm tra internet"]