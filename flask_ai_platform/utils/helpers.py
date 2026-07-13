def format_response(success, message, data=None):
    """
    Standardize the JSON response format for all API endpoints.
    """
    response = {
        'success': success,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return response

def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg', 'webp'}):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
