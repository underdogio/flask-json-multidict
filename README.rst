flask-json-multidict
====================

.. image:: https://travis-ci.org/underdogio/flask-json-multidict.png?branch=master
   :target: https://travis-ci.org/underdogio/flask-json-multidict
   :alt: Build Status

Convert Flask's `request.get_json`_ dict into a `MultiDict`_ like `request.form`_

This was written to maintain a consistent API for interacting with both ``request.form`` and ``request.get_json()``. This allows use to leverage ``.get`` with type coercion and ``.getlist``.

.. _`request.get_json`: http://flask.pocoo.org/docs/0.10/api/#flask.Request.get_json
.. _`MultiDict`: http://werkzeug.pocoo.org/docs/0.10/datastructures/#werkzeug.datastructures.MultiDict
.. _`request.form`: http://flask.pocoo.org/docs/0.10/api/#flask.Request.form

Getting Started
---------------
Install the module with: ``pip install flask_json_multidict``

.. code:: python

    # Load in our dependencies
    from flask import Flask, request, jsonify
    from flask_json_multidict import get_json_multidict

    # Start an application
    app = Flask(__name__)

    def resolve_request_body():
        """Before every request, resolve `request.body` from either `request.form` or `request.get_json()`"""
        request.body = request.form
        if request.headers['content-type'] == 'application/json':
            request.body = get_json_multidict(request)
    app.before_request(resolve_request_body)

    @app.route('/', methods=['POST'])
    def root():
        """Reply with POST data as we see it"""
        body = request.body
        return jsonify({key: body[key] for key in body})
        # We can also leverage `request.body.getlist` as we do with `request.form`


    if __name__ == '__main__':
        app.run()

    # $ curl http://localhost:5000/ -X POST --data 'hello=world'
    # {"hello": "world"}
    # $ curl http://localhost:5000/ -X POST -H 'Content-Type: application/json' --data '{"hello": "world"}
    # {"hello": "world"}

Documentation
-------------
``flask-json-multidict`` can be imported via ``flask_json_multidict``.

flask_json_multidict.get_json_multidict(request)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``get_json_multidict`` walks over the ``json`` provided by ``request.get_json()`` and returns a `MultiDict`_.

- request ``object`` - Current ``request`` being handled by Flask

**Returns:**

- body ``object`` - MultiDict with ``json`` information
    - If there were any dictionaries or nested lists, then these will be ignored as parameters
        - This is for consistency with how ``request.form`` behaves

.. code:: python

    # Assume we receive `{"colors": ["red", "blue"]}`
    body = get_json_multidict(request)
    body.getlist('colors')  # ['red', 'blue']

    # Assume we receive `{"hello": "world"}`
    body = get_json_multidict(request)
    body.['hello']  # 'world'
    body.get('hello')  # 'world'

    # Assume we receive `{"foo": {"bar": "baz"}}`
    # This is the silent ignore of bad parameters
    body = get_json_multidict(request)
    body.get('foo')  # None

Contributing
------------
In lieu of a formal styleguide, take care to maintain the existing coding style. Add unit tests for any new or changed functionality. Test via ``nosetests``.

License
-------
Copyright (c) 2015 Underdog.io

Licensed under the MIT license.
