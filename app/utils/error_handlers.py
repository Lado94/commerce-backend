from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(400)
    def handle_400(e):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Internal server error"}), 500
