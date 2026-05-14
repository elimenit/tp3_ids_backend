from flask import jsonify

def error_response(message: str, description: str, status_code: int = 400):
    """ Response de Error;\n
    devuelve una response con el status code pasado como argumento.
    """

    return jsonify(
        {"mensaje": message, "description": description}
    ), status_code