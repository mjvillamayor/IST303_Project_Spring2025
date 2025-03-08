from flask import Blueprint, request, jsonify
from api_integration import get_drug_interactions

main = Blueprint('main', __name__)

@main.route('/api/interactions', methods=['POST'])
def check_interactions():
    """
    API Endpoint to check for drug interactions.
    Accepts a JSON payload with a list of drug names.
    """
    data = request.get_json()

    # Validate request payload
    if not data or 'drug_names' not in data:
        return jsonify({"error": "Invalid request. Please provide a list of drug names."}), 400

    drug_names = data['drug_names']
    interaction_results = {}

    for drug in drug_names:
        interaction_results[drug] = get_drug_interactions(drug)

    return jsonify(interaction_results), 200
