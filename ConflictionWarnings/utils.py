import requests

OPENFDA_API_URL = "https://api.fda.gov/drug/event.json"

def get_adverse_events(drug1, drug2):
    """
    Query the OpenFDA API for adverse event reports involving two drugs.
    """
    try:
        query = f'"{drug1}" AND "{drug2}"'
        response = requests.get(
            OPENFDA_API_URL,
            params={"search": f"patient.drug.medicinalproduct:{query}", "limit": 5}
        )
        if response.status_code == 200:
            data = response.json()
            results = []
            for event in data.get("results", []):
                results.append({
                    "reaction": event.get("patient", {}).get("reaction", [{}])[0].get("reactionmeddrapt", "N/A"),
                    "description": event.get("safetyreportid", "No description available"),
                })
            return results
        else:
            return {"error": f"OpenFDA API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
