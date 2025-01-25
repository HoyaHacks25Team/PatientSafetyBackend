from flask import Blueprint, request, jsonify
from ConflictionWarnings.utils import get_adverse_events

blueprint = Blueprint('confliction_warnings', __name__)

@blueprint.route('/check', methods=['POST'])
def check_interaction():
    """
    Endpoint to check for interactions between two drugs.
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
