import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


def send_mail_users(template:str, subject:str, receivers:list, context:dict):

	""" This function help us to send email to a set of users or to simple users"""

	try:
		message = render_to_string(template, context)

		send_mail(
			subject,
			message,
			settings.DEFAULT_FROM_EMAIL,
			fail_silently=True,
			html_message=message,
			recipient_list=receivers
			)
		return True

	except Exception as e:
		logger.error(e)

	return False