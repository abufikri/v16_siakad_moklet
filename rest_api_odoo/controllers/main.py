# -*- coding: utf-8 -*-
import json
import logging
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class RestApi(http.Controller):
    """Controller to handle API requests and generate responses."""

    def auth_api_key(self, api_key):
        """Authenticate API key."""
        if not api_key:
            return Response(json.dumps({'status': 'error', 'message': 'No API key provided'}), content_type='application/json')
        
        user_id = request.env['res.users'].search([('api_key', '=', api_key)], limit=1)
        if user_id:
            return True
        return Response(json.dumps({'status': 'error', 'message': 'Invalid API key'}), content_type='application/json')

    def get_request_data(self):
        """Utility to extract and parse request data."""
        try:
            return json.loads(request.httprequest.data)
        except json.JSONDecodeError:
            return Response(json.dumps({'status': 'error', 'message': 'Invalid JSON Data'}), content_type='application/json')

    def generate_response(self, method, model, rec_id):
        """Generate the response based on HTTP method and parameters."""
        option = request.env['connection.api'].search([('model_id', '=', model)], limit=1)
        if not option:
            return Response(json.dumps({'status': 'error', 'message': 'No Record Created for the model'}), content_type='application/json')

        model_name = option.model_id.model
        fields = []
        data = self.get_request_data() if method != 'DELETE' else {}

        if data and 'fields' in data:
            fields = data['fields']

        if method == 'GET':
            return self.handle_get(option, model_name, rec_id, fields)
        elif method == 'POST':
            return self.handle_post(option, model_name, fields, data)
        elif method == 'PUT':
            return self.handle_put(option, model_name, rec_id, fields, data)
        elif method == 'DELETE':
            return self.handle_delete(option, model_name, rec_id)
        else:
            return Response(json.dumps({'status': 'error', 'message': 'Invalid Method'}), content_type='application/json')

    def handle_get(self, option, model_name, rec_id, fields):
        """Handle GET requests."""
        if not option.is_get:
            return Response(json.dumps({'status': 'error', 'message': 'Method Not Allowed'}), content_type='application/json')

        domain = [('id', '=', rec_id)] if rec_id else []
        records = request.env[str(model_name)].search_read(domain=domain, fields=fields)
        return request.make_response(json.dumps({'records': records}))

    def handle_post(self, option, model_name, fields, data):
        """Handle POST requests."""
        if not option.is_post:
            return Response(json.dumps({'status': 'error', 'message': 'Method Not Allowed'}), content_type='application/json')

        try:
            new_resource = request.env[str(model_name)].create(data['values'])
            partner_records = request.env[str(model_name)].search_read(
                domain=[('id', '=', new_resource.id)],
                fields=fields
            )
            return request.make_response(json.dumps({'New resource': partner_records}))
        except KeyError:
            return Response(json.dumps({'status': 'error', 'message': 'Invalid JSON Data'}), content_type='application/json')

    def handle_put(self, option, model_name, rec_id, fields, data):
        """Handle PUT requests."""
        if not option.is_put:
            return Response(json.dumps({'status': 'error', 'message': 'Method Not Allowed'}), content_type='application/json')

        if rec_id == 0:
            return Response(json.dumps({'status': 'error', 'message': 'No ID Provided'}), content_type='application/json')

        resource = request.env[str(model_name)].browse(rec_id)
        if not resource.exists():
            return Response(json.dumps({'status': 'error', 'message': 'Resource not found'}), content_type='application/json')

        try:
            resource.write(data['values'])
            updated_resource = request.env[str(model_name)].search_read(
                domain=[('id', '=', resource.id)],
                fields=fields
            )
            return request.make_response(json.dumps({'Updated resource': updated_resource}))
        except KeyError:
            return Response(json.dumps({'status': 'error', 'message': 'Invalid JSON Data'}), content_type='application/json')

    def handle_delete(self, option, model_name, rec_id):
        """Handle DELETE requests."""
        if not option.is_delete:
            return Response(json.dumps({'status': 'error', 'message': 'Method Not Allowed'}), content_type='application/json')

        if rec_id == 0:
            return Response(json.dumps({'status': 'error', 'message': 'No ID Provided'}), content_type='application/json')

        resource = request.env[str(model_name)].browse(rec_id)
        if not resource.exists():
            return Response(json.dumps({'status': 'error', 'message': 'Resource not found'}), content_type='application/json')

        records = request.env[str(model_name)].search_read(
            domain=[('id', '=', resource.id)],
            fields=['id', 'display_name']
        )
        resource.unlink()
        return request.make_response(json.dumps({"Resource deleted": records}))

    @http.route(['/send_request'], type='http', auth='none', methods=['GET', 'POST', 'PUT', 'DELETE'], csrf=False)
    def fetch_data(self, **kw):
        """Handle incoming requests, authenticate API key, and generate response."""
        api_key = request.httprequest.headers.get('api-key')
        auth_api = self.auth_api_key(api_key)

        if auth_api is not True:
            return auth_api

        model = kw.get('model')
        rec_id = int(kw.get('Id', 0))
        username = request.httprequest.headers.get('login')
        password = request.httprequest.headers.get('password')
        request.session.authenticate(request.session.db, username, password)

        model_id = request.env['ir.model'].search([('model', '=', model)], limit=1)
        if not model_id:
            return Response(json.dumps({'status': 'error', 'message': 'Invalid model or module not installed'}), content_type='application/json')

        return self.generate_response(request.httprequest.method, model_id.id, rec_id)

    @http.route(['/odoo_connect'], type="http", auth="none", csrf=False, methods=['GET'])
    def odoo_connect(self, **kw):
        """Generate API key for authenticated user."""
        try:
            username = request.httprequest.headers.get('login')
            password = request.httprequest.headers.get('password')
            db = request.httprequest.headers.get('db')
            request.session.update(http.get_default_session(), db=db)
            auth = request.session.authenticate(request.session.db, username, password)
            api_key = request.env.user.generate_api(username)
            user = request.env['res.users'].browse(auth)
            return request.make_response(json.dumps({"Status": "auth successful", "User": user.name, "api-key": api_key}))
        except:
            return Response(json.dumps({'status': 'error', 'message': 'Wrong login credentials'}), content_type='application/json')
