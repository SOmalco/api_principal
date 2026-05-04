from flask import Flask, jsonify, request
from api_principal.controller import controller

app = Flask(__name__)

@app.route('/partners', methods=['POST'])
def create_partner_endpoint():
    try:
        if request.is_json:
            body = request.get_json()
            return controller.create_partner(body)
        return jsonify({"error": "Invalid JSON format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/partners/<string:partner_id>/quotes', methods=['POST'])
def calculate_quote_endpoint(partner_id):
    """
    Expected body:
        {
        age: integer [0-99],
        sex: string ['m/M', 'f/F', 'n/N']
        }
    expected response:
        {
        id: uuid,
        age: integer [0-99],
        sex: string ['m/M', 'f/F', 'n/N'],
        price: string,
        expire_at: Date ("yyyy-mm-dd")
        }
    """
    try:
        if request.is_json:
            body = request.get_json()
            return controller.calculate_quote(body)
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/partners/<partner_id>/policies', methods=['POST'])
def create_policy_endpoint(partner_id):
    """"
    Expected body:
        {
        quotation_id: uuid,
        name: string,
        sex: string ['m/M', 'f/F', 'n/N'],
        date_of_birth: Date ("yyyy-mm-dd")
        }
    expected response:
        200
        {
        id: uuid,
        quotation_id: uuid,
        name: string,
        sex: string ['m/M', 'f/F', 'n/N'],
        date_of_birth: Date ("yyyy-mm-dd")
        }
    """
    try:
        if request.is_json:
            body = request.get_json()
            return controller.create_policy(body)

        return jsonify({"error": "Invalid JSON format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/partners/<partner_id>/policies/<policy_id>', methods=['GET'])
def get_policy_by_id_endpoint(partner_id: str,
                              policy_id: str):
    """"

    expected response:
        {
        "date_of_birth": Date ("yyyy-mm-dd"),
        "id": uuid,
        "name": str,
        "quotation_id": uuid,
        "sex": string ['m/M', 'f/F', 'n/N']
    }
    """
    try:
        return controller.get_policy(policy_id)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def start_server():
    app.run(debug=True)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
