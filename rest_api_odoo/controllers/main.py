# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import json
import logging
from odoo import http
from odoo.http import request
from odoo.http import Response

_logger = logging.getLogger(__name__)


class RestApi(http.Controller):
    """This is a controller which is used to generate responses based on the
    api requests"""

    def auth_api_key(self, api_key):
        """This function is used to authenticate the api-key when sending a
        request"""

        user_id = request.env['res.users'].search([('api_key', '=', api_key)])
        if api_key is not None and user_id:
            response = True
            return response
        elif not user_id:
            response = {'status': 'error', 'message': 'Invalid API key'}
            return Response(json.dumps(response), content_type='application/json')

        else:
            response = {'status': 'error', 'message': 'No API key provided'}
            return Response(json.dumps(response), content_type='application/json')



    def generate_response(self, method, model, rec_id):
        """This function is used to generate the response based on the type
        of request and the parameters given"""
        option = request.env['connection.api'].search(
            [('model_id', '=', model)], limit=1)
        model_name = option.model_id.model

        if method != 'DELETE':
            data = json.loads(request.httprequest.data)
        else:
            data = {}
        fields = []
        if data:
            for field in data['fields']:
                fields.append(field)
        if not fields and method != 'DELETE':
            response = {'status': 'error', 'message': 'No fields selected for the model'}
            return Response(json.dumps(response), content_type='application/json')
        
        if not option:
            response = {'status': 'error', 'message': 'No Record Created for the model'}
            return Response(json.dumps(response), content_type='application/json')
        try:
            if method == 'GET':
                fields = []
                for field in data['fields']:
                    fields.append(field)
                if not option.is_get:
                    response = {'status': 'error', 'message': 'Method Not Allowed'}
                    return Response(json.dumps(response), content_type='application/json')
                else:
                    datas = []
                    if rec_id != 0:
                        partner_records = request.env[
                            str(model_name)].search_read(
                            domain=[('id', '=', rec_id)],
                            fields=fields
                        )
                        data = json.dumps({
                            'records': partner_records
                        })
                        datas.append(data)
                        return request.make_response(data=datas)
                    else:
                        partner_records = request.env[
                            str(model_name)].search_read(
                            domain=[],
                            fields=fields
                        )
                        data = json.dumps({
                            'records': partner_records
                        })
                        datas.append(data)
                        return request.make_response(data=datas)
        except:
            response = {'status': 'error', 'message': 'Invalid JSON Data'}
            return Response(json.dumps(response), content_type='application/json')
        if method == 'POST':
            if not option.is_post:
                response = {'status': 'error', 'message': 'Method Not Allowed'}
                return Response(json.dumps(response), content_type='application/json')
            else:
                try:
                    data = json.loads(request.httprequest.data)
                    datas = []
                    new_resource = request.env[str(model_name)].create(
                        data['values'])
                    partner_records = request.env[
                        str(model_name)].search_read(
                        domain=[('id', '=', new_resource.id)],
                        fields=fields
                    )
                    new_data = json.dumps({'New resource': partner_records, })
                    datas.append(new_data)
                    return request.make_response(data=datas)
                except:
                    response = {'status': 'error', 'message': 'Invalid Json Data'}
                    return Response(json.dumps(response), content_type='application/json')
        if method == 'PUT':
            if not option.is_put:
                response = {'status': 'error', 'message': 'Method Not Allowed'}
                return Response(json.dumps(response), content_type='application/json')
            else:
                if rec_id == 0:
                    response = {'status': 'error', 'message': 'No ID Provided'}
                    return Response(json.dumps(response), content_type='application/json')

                else:
                    resource = request.env[str(model_name)].browse(
                        int(rec_id))
                    if not resource.exists():
                        response = {'status': 'error', 'message': 'Resource not found'}
                        return Response(json.dumps(response), content_type='application/json')
                    else:
                        try:
                            datas = []
                            data = json.loads(request.httprequest.data)
                            resource.write(data['values'])
                            partner_records = request.env[
                                str(model_name)].search_read(
                                domain=[('id', '=', resource.id)],
                                fields=fields
                            )
                            new_data = json.dumps(
                                {'Updated resource': partner_records,
                                 })
                            datas.append(new_data)
                            return request.make_response(data=datas)

                        except:
                            response = {'status': 'error', 'message': 'Invalid JSON Data'}
                            return Response(json.dumps(response), content_type='application/json')
        if method == 'DELETE':
            if not option.is_delete:
                response = {'status': 'error', 'message': 'Method Not Allowed'}
                return Response(json.dumps(response), content_type='application/json')

            else:
                if rec_id == 0:
                    response = {'status': 'error', 'message': 'No ID Provided'}
                    return Response(json.dumps(response), content_type='application/json')
                else:
                    resource = request.env[str(model_name)].browse(
                        int(rec_id))
                    if not resource.exists():
                        response = {'status': 'error', 'message': 'Resource not found'}
                        return Response(json.dumps(response), content_type='application/json')
                    else:

                        records = request.env[
                            str(model_name)].search_read(
                            domain=[('id', '=', resource.id)],
                            fields=['id', 'display_name']
                        )
                        remove = json.dumps(
                            {"Resource deleted": records,
                             })
                        resource.unlink()
                        return request.make_response(data=remove)

    @http.route(['/send_request'], type='http',
                auth='none',
                methods=['GET', 'POST', 'PUT', 'DELETE'], csrf=False)
    def fetch_data(self, **kw):
        """This controller will be called when sending a request to the
        specified url, and it will authenticate the api-key and then will
        generate the result"""

        http_method = request.httprequest.method
        api_key = request.httprequest.headers.get('api-key')
        auth_api = self.auth_api_key(api_key)
        model = kw.get('model')
        username = request.httprequest.headers.get('login')
        password = request.httprequest.headers.get('password')
        request.session.authenticate(request.session.db, username,
                                     password)
        model_id = request.env['ir.model'].search(
            [('model', '=', model)])
        if not model_id:
            response = {'status': 'error', 'message': 'Invalid model, check spelling or maybe the related module is not installed'}
            return Response(json.dumps(response), content_type='application/json')

        if auth_api == True:
            if not kw.get('Id'):
                rec_id = 0
            else:
                rec_id = int(kw.get('Id'))
            result = self.generate_response(http_method, model_id.id, rec_id)
            return result
        else:
            return auth_api

    @http.route(['/odoo_connect'], type="http", auth="none", csrf=False,
                methods=['GET'])
    def odoo_connect(self, **kw):
        """This is the controller which initializes the api transaction by
        generating the api-key for specific user and database"""

        username = request.httprequest.headers.get('login')
        password = request.httprequest.headers.get('password')
        db = request.httprequest.headers.get('db')
        try:
            request.session.update(http.get_default_session(), db=db)
            auth = request.session.authenticate(request.session.db, username,
                                                password)
            user = request.env['res.users'].browse(auth)
            api_key = request.env.user.generate_api(username)
            datas = json.dumps({"Status": "auth successful",
                                "User": user.name,
                                "api-key": api_key})
            return request.make_response(data=datas)
        except:
            response = {'status': 'error', 'message': 'wrong login credentials'}
            return Response(json.dumps(response), content_type='application/json')
