#############################################################
#
#  Module Name: muk_dm
#  Created On: 2018-10-25 13:55
#  File Name: forum.py
#  Author: Nathan Sadeli
#
#############################################################
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning as UserError

class KarmaDefaultValue(models.Model):
    #                                                    #
    #                                                    #
    # ________________ ORM mulai disini ________________ #
    #                                                    #
    #                                                    #
    
    #_name               = 'karma.defaultvalue'
    _inherit            = ['forum.forum']
    _description        = 'Inherit Model odoo/addons/forum'
    
    #                                                    #
    #                                                    #
    # ____________ field-field mulai disini ____________ #
    #                                                    #
    #                                                    #
    
    # karma generation
    karma_gen_question_new = fields.Integer(string='Asking a question', default=0)
    karma_gen_question_upvote = fields.Integer(string='Question upvoted', default=0)
    karma_gen_question_downvote = fields.Integer(string='Question downvoted', default=0)
    karma_gen_answer_upvote = fields.Integer(string='Answer upvoted', default=0)
    karma_gen_answer_downvote = fields.Integer(string='Answer downvoted', default=0)
    karma_gen_answer_accept = fields.Integer(string='Accepting an answer', default=0)
    karma_gen_answer_accepted = fields.Integer(string='Answer accepted', default=0)
    karma_gen_answer_flagged = fields.Integer(string='Answer flagged', default=0)
    # karma-based actions
    karma_ask = fields.Integer(string='Ask questions', default=0)
    karma_answer = fields.Integer(string='Answer questions', default=0)
    karma_edit_own = fields.Integer(string='Edit own posts', default=0)
    karma_edit_all = fields.Integer(string='Edit all posts', default=0)
    karma_edit_retag = fields.Integer(string='Change question tags', default=0, oldname="karma_retag")
    karma_close_own = fields.Integer(string='Close own posts', default=0)
    karma_close_all = fields.Integer(string='Close all posts', default=0)
    karma_unlink_own = fields.Integer(string='Delete own posts', default=0)
    karma_unlink_all = fields.Integer(string='Delete all posts', default=0)
    karma_tag_create = fields.Integer(string='Create new tags', default=0)
    karma_upvote = fields.Integer(string='Upvote', default=0)
    karma_downvote = fields.Integer(string='Downvote', default=0)
    karma_answer_accept_own = fields.Integer(string='Accept an answer on own questions', default=0)
    karma_answer_accept_all = fields.Integer(string='Accept an answer to all questions', default=0)
    karma_comment_own = fields.Integer(string='Comment own posts', default=0)
    karma_comment_all = fields.Integer(string='Comment all posts', default=0)
    karma_comment_convert_own = fields.Integer(string='Convert own answers to comments and vice versa', default=0)
    karma_comment_convert_all = fields.Integer(string='Convert all answers to comments and vice versa', default=0)
    karma_comment_unlink_own = fields.Integer(string='Unlink own comments', default=0)
    karma_comment_unlink_all = fields.Integer(string='Unlink all comments', default=0)
    karma_flag = fields.Integer(string='Flag a post as offensive', default=0)
    karma_dofollow = fields.Integer(string='Nofollow links', help='If the author has not enough karma, a nofollow attribute is added to links', default=0)
    karma_editor = fields.Integer(string='Editor Features: image and links',
                                  default=0, oldname='karma_editor_link_files')
    karma_user_bio = fields.Integer(string='Display detailed user biography', default=0)
    karma_post = fields.Integer(string='Ask questions without validation', default=0)
    karma_moderate = fields.Integer(string='Moderate posts', default=0)
    
    #                                                    #
    #                                                    #
    # _______________ method mulai disini ______________ #
    #                                                    #
    #                                                    #
    
    #