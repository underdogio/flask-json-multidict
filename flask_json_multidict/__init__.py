# Load in our dependencies
from werkzeug.datastructures import MultiDict


# Define our library
def get_json_multidict(request):
    """Extract MultiDict from `request.get_json` to produce similar MultiDict to `request.form`"""
    # Extract our JSON
    body = request.get_json()

    # Iterate over the values
    multi_dict_items = []
    for key in body:
        # If the item is a list (e.g. `['hello', 'world']`, iterate its values
        value = body[key]
        if isinstance(value, list):
            for subvalue in value:
                # If the subvalue is a primitive, save it (e.g. `key -> 'hello'`)
                # DEV: We ignore non-primitives for consistency with what `application/x-www-form-urlencoded` accepts
                if not isinstance(subvalue, list) and not isinstance(subvalue, dict):
                    multi_dict_items.append((key, subvalue))
        # If we have a dictionary, ignore it
        # DEV: We ignore non-primitives for consistency with what `application/x-www-form-urlencoded` accepts
        elif isinstance(value, dict):
            pass
        # Otherwise, save the key/value pair
        else:
            multi_dict_items.append((key, value))

    # Return our generated multidict
    return MultiDict(multi_dict_items)
