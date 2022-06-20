from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from backends.tokens import EmailVerificationTokenGenerator


class SendEmailVerificationMixin:
    token_generator = EmailVerificationTokenGenerator()

    def get(self, request, *args, **kwargs):
        if not self.request.user.profile.is_email_verified:
            mail_kwargs = {
                'user': self.request.user,
                'request': self.request,
                'token_generator': self.token_generator,
                'use_https': self.request.is_secure(),
            }
            self.send_mail(**mail_kwargs)
        else:
            print("aaa")
        return super().get(request, *args, **kwargs)

    def send_mail(self, user=None, request=None, token_generator=None, use_https=None):
        current_site = get_current_site(request)
        context = {
            'email': user.email,
            'domain': current_site.domain,
            'site_name': current_site.name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
        }
        email_message = EmailMultiAlternatives(
            subject=self.get_email_subject(context),
            body=self.get_email_body(context),
            to=[user.email],
        )
        email_message.send()

    def get_email_subject(self, context):
        subject_template_name = 'user/password_reset_subject.txt'
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        return ''.join(subject.splitlines())

    def get_email_body(self, context):
        email_template_name = 'user/password_reset_email.html'
        return loader.render_to_string(email_template_name, context)
