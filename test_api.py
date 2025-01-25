import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

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

@app.route('/check-interaction', methods=['POST'])
def check_interaction():
    """
    Endpoint to check for interactions between two drugs using OpenFDA.
    """
    data = request.get_json()
    drug1 = data.get("drug1")
    drug2 = data.get("drug2")

    if not drug1 or not drug2:
        return jsonify({"error": "Both drug1 and drug2 are required"}), 400

    interactions = get_adverse_events(drug1, drug2)
    if "error" in interactions:
        return jsonify({"error": interactions["error"]}), 500

    return jsonify({"drug1": drug1, "drug2": drug2, "interactions": interactions}), 200

if __name__ == "__main__":
    app.run(debug=True)
