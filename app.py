import requests
from flask import Flask, request, jsonify
from config import DevelopmentConfig

# Initialisation de Flask avec config
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

@app.route('/verify_address', methods=['GET'])
def verify_address():
    """Vérifie si une adresse est valide en Europe via Google Address Validation API"""

    address = request.args.get('address')
    if not address:
        return jsonify({"error": "Paramètre 'address' requis"}), 400

    # Corps de la requête
    payload = {
        "address": {"addressLines": [address]},
        "enableUspsCass": False  # USPS désactivé pour l'Europe
    }
    params = {"key": app.config["GOOGLE_API_KEY"]}

    try:
        response = requests.post(app.config["API_URL"], json=payload, params=params)
        data = response.json()

        # Affichage pour le debug
        print(f"Réponse API : {data}")

        # Vérifier si l'API a retourné un verdict
        verdict = data.get("result", {}).get("verdict", {})
        address_complete = verdict.get("addressComplete", False)

        # Vérifier si une adresse formatée est renvoyée
        formatted_address = data.get("result", {}).get("address", {}).get("formattedAddress", None)

        # Construire la réponse
        return jsonify({
            "valid": address_complete,
            "formatted_address": formatted_address,
            "verdict": verdict  # Ajout des détails pour analyse
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Erreur de connexion à l'API", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"])
