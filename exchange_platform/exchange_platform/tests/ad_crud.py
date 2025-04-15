import httpx

# 🔐 Подставь сюда свой токен
TOKEN = 'f321aaac6b9c41e5f429c1d3ce8000c435ac83bc'

# 🌐 URL твоего API
BASE_URL = 'http://localhost:8000/api/v1/ads/'

# Заголовки для авторизации
HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}


def create_ad():
    data = {
        "title": "iPhone 13 Pro",
        "description": "Новый, без царапин",
        "category": "Electronics",
        "condition": "New"
    }
    response = httpx.post(BASE_URL, headers=HEADERS, json=data)
    print("CREATE:", response.status_code, response.json())
    return response.json().get('id')


def list_ads():
    response = httpx.get(BASE_URL, headers=HEADERS)
    print("LIST:", response.status_code, response.json())


def retrieve_ad(ad_id):
    response = httpx.get(f"{BASE_URL}{ad_id}/", headers=HEADERS)
    print("RETRIEVE:", response.status_code, response.json())


def update_ad(ad_id):
    updated_data = {
        "title": "iPhone 13 Pro Max",
        "description": "Как новый, торг уместен",
        "category": "Electronics",
        "condition": "Like New"
    }
    response = httpx.put(f"{BASE_URL}{ad_id}/", headers=HEADERS, json=updated_data)
    print("UPDATE:", response.status_code, response.json())


def delete_ad(ad_id):
    response = httpx.delete(f"{BASE_URL}{ad_id}/", headers=HEADERS)
    print("DELETE:", response.status_code)

"""
аутпут экзамл

CREATE: 201 {'id': 13, 'user': 1, 'title': 'iPhone 13 Pro', 'description': 'Новый, без царапин', 'image': None, 'category': 'Electronics', 'condition': 'New', 'created_at': '2025-04-14T11:46:04.615921Z', 'is_archived': False}
LIST: 200 [{'id': 13, 'user': 1, 'title': 'iPhone 13 Pro', 'description': 'Новый, без царапин', 'image': None, 'category': 'Electronics', 'condition': 'New', 'created_at': '2025-04-14T11:46:04.615921Z', 'is_archived': False}]
RETRIEVE: 200 {'id': 13, 'user': 1, 'title': 'iPhone 13 Pro', 'description': 'Новый, без царапин', 'image': None, 'category': 'Electronics', 'condition': 'New', 'created_at': '2025-04-14T11:46:04.615921Z', 'is_archived': False}
UPDATE: 200 {'id': 13, 'user': 1, 'title': 'iPhone 13 Pro Max', 'description': 'Как новый, торг уместен', 'image': None, 'category': 'Electronics', 'condition': 'Like New', 'created_at': '2025-04-14T11:46:04.615921Z', 'is_archived': False}
RETRIEVE: 200 {'id': 13, 'user': 1, 'title': 'iPhone 13 Pro Max', 'description': 'Как новый, торг уместен', 'image': None, 'category': 'Electronics', 'condition': 'Like New', 'created_at': '2025-04-14T11:46:04.615921Z', 'is_archived': False}
DELETE: 204
LIST: 200 []

"""

if __name__ == "__main__":
    ad_id = create_ad()
    if ad_id:
        list_ads()
        retrieve_ad(ad_id)
        update_ad(ad_id)
        retrieve_ad(ad_id)
        delete_ad(ad_id)
        list_ads()
