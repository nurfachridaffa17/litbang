from odoo import models, api, fields
from odoo.exceptions import ValidationError

class WhatsappSendMessage(models.TransientModel):
    _name = 'whatsapp.message.wizard'


    mobile = fields.Char(required=True)
    message = fields.Text(string="message", required=True)

    def send_message(self):
        if self.message and self.mobile:
            message_string = ''
            message = self.message.split(' ')
            for msg in message:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            number = str(self.mobile)
            if number[0] == "0":
                number = "+62"+number[1:] 
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone="+number+"&text=" + message_string,
                'target': 'new',
                'res_id': self.id,
            }