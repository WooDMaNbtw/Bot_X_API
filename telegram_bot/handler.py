import time

import django
import os
""" DJANGO SETUP """
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from services import BotList, BotDetail, DialogueList, DialogueDetail, EmailVerificationCheck, EmailVerificationResend, EmailVerificationVerify, Register, Login, Logout


class Handler:

    def bot_list(self):
        '''
        Returns a list of bots
        Parameters:
            None
        '''
        bot_list = BotList.BotList(need_execute_local=True)
        response = bot_list.get_response()
        return response

    def bot_detail(self, bot_id):
        '''
        Returns a list of detailed bot
        Parameters:
            bot_id - identifier of the bot
        '''
        bot_detail = BotDetail.BotDetail(bot_id=bot_id, need_execute_local=True)
        response = bot_detail.get_response()
        return response

    def register(self, email, password):
        '''
        Registers a new user and returns its Identifier (id)
        Parameters:
            email - Email address of the user
            password - <PASSWORD>
        EXAMPLE:
        data = {"email": "telegram_admin@admin.ru", "password": "telegram12345"}
        '''
        data = {
            'email': email,
            'password': password
        }
        register = Register.Register(need_execute_local=True, data=data)
        response = register.get_response()
        return response

    def login(self, email, password):
        '''
        Login a new user and returns its id and personal token
        Parameters:
            email - Email address of the user
            password - <PASSWORD>
        EXAMPLE:
        data = {"email": "telegram_admin@admin.ru", "password": "telegram12345"}
        '''
        data = {
            'email': email,
            'password': password
        }
        login = Login.Login(need_execute_local=True, data=data)
        response = login.get_response()
        return response

    def logout(self, token):
        '''
        Returns nothing (204 response) if token is valid
        Parameters:
            token - personal user's token
        EXAMPLE:
        token = "ec7f977445e107cb2af386c42235faf210591c3d7fdc6c985503e64edb02b901"
        token=login_response["result"]["access_token"]
        '''
        logout = Logout.Logout(need_execute_local=True, token=token)
        response = logout.get_response()
        return response

    def dialogue_list(self, token):
        '''
        Returns dialogue list
        Parameters:
            token - personal user's token
        EXAMPLE:
        token = "ec7f977445e107cb2af386c42235faf210591c3d7fdc6c985503e64edb02b901"
        token=login_response["result"]["access_token"]
        '''
        dialogue_list = DialogueList.DialogueList(method="GET", need_execute_local=True, token=token)
        response = dialogue_list.get_response()
        return response

    def dialogue_detail(self, dialogue_id, token):
        '''
        Returns detailed dialogue
        Parameters:
            dialogue_id - id of the requested dialogue
            token - personal user's token
        EXAMPLE:
        dialogue_id = 2
        token = "ec7f977445e107cb2af386c42235faf210591c3d7fdc6c985503e64edb02b901"
        token=login_response["result"]["access_token"]
        '''
        dialogue_details = DialogueDetail.DialogueDetail(method="GET", dialogue_id=dialogue_id, need_execute_local=True, token=token)
        response = dialogue_details.get_response()
        return response

    def email_check(self, token):
        '''
        Returns if emailed checked or not (True/False)
        Parameters:
            token - personal user's token
        EXAMPLE:
        token = "ec7f977445e107cb2af386c42235faf210591c3d7fdc6c985503e64edb02b901"
        token=login_response["result"]["access_token"]
        '''
        email_check = EmailVerificationCheck.EmailVerificationCheck(need_execute_local=True, token=token)
        response = email_check.get_response()
        return response

    def email_resend(self, token):
        '''
        Returns nothing (204 response) if message has been sent
        otherwise 'rate_limit_exceeded'
        Parameters:
            token - personal user's token
        EXAMPLE:
        token = "ec7f977445e107cb2af386c42235faf210591c3d7fdc6c985503e64edb02b901"
        token=login_response["result"]["access_token"]
        '''
        email_resend = EmailVerificationResend.EmailVerificationResend(need_execute_local=True, token=token)
        response = email_resend.get_response()
        return response

    def email_verify(self, email, code, token):
        '''
        Returns nothing (204 response) if email, code and token are valid
        otherwise 'rate_limit_exceeded'
        Parameters:
            email - Email address of the user
            code - Email code of the user
            token - personal user's token
        EXAMPLE:
        data = {"email": "telegram_admin@admin.ru", "code": "12345"}
        token - "ec7f977445e107cb2af386c42235faf210591c3d7fdc6c985503e64edb02b901"
        token=login_response["result"]["access_token"]
        '''
        data = {
            "email": email,
            "code": code
        }
        email_verify = EmailVerificationVerify.EmailVerificationVerify(need_execute_local=True, data=data, token=token)
        response = email_verify.get_response()
        return response


