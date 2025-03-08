import requests

def get_drug_interactions(drug_name):
    """
    Fetches drug interaction data from openFDA API.
    """
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}&limit=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract interactions if available
        results = data.get("results", [])
        if results and "drug_interactions" in results[0]:
            return results[0]["drug_interactions"]
        else:
            return {"message": "No interaction data found for this drug."}
    
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error: {req_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}
