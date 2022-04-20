from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception,content_disposition
import base64

class Binary(http.Controller):

    @http.route('/web/binary/download_document', type='http', auth="public")
    @serialize_exception
    def download_document(self, model, id, filename=None, **kw):
        record = request.env[model].browse(int(id))
        binary_file = record.document
        filecontent = base64.b64decode(binary_file or '')
        content_type, disposition_content = False, False

        if not filecontent:
            return request.not_found()
        else:
            if not filename:
                filename = '%s_%s' % (model.replace('.', '_'), id)
            content_type = ('Content-Type', 'application/msword')
            disposition_content = ('Content-Disposition', content_disposition(filename))

        return request.make_response(filecontent, [content_type, disposition_content])
      

    