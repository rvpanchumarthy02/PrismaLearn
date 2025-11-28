from flask import jsonify

def error_response(message, status_code):
    return jsonify({"error": message, "success": False}), status_code

def success_response(data, message="Success", status_code=200):
    return jsonify({"data": data, "message": message, "success": True}), status_code