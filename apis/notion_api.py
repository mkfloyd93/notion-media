import requests

def notion_request(method, url, headers, payload=None):
    """Helper for making Notion API requests."""
    try:
        if payload:
            response = requests.request(method, url, headers=headers, json=payload)
        else:
            response = requests.request(method, url, headers=headers)

        # Raise exception for HTTP errors
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err} | Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception: {req_err}")
    return None


# --- API Functions ---
def read_database(database_id, headers, query_payload):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    return notion_request("POST", url, headers, query_payload)


def create_page(headers, new_page_data):
    url = "https://api.notion.com/v1/pages"
    return notion_request("POST", url, headers, new_page_data)


def update_page(page_id, headers, update_data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    return notion_request("PATCH", url, headers, update_data)