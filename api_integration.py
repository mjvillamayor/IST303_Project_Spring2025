import requests

def get_drug_interactions(drug_name):
    """Fetch drug interactions from OpenFDA API"""
    API_URL = f"https://api.fda.gov/drug/label.json?search={drug_name}&limit=1"

    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data from OpenFDA"}
    except Exception as e:
        return {"error": str(e)}
