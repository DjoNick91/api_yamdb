import secrets
import string
from django.core.mail import send_mail


def generate_code():
    confirmation_code = "".join(
        secrets.choice(string.digits + string.ascii_letters) for i in range(30)
    )
    return confirmation_code


def new_user(email, confirmation_code):
    send_mail(
        "Регистрация на сайте YaMDb",
        (
            f'{"Для регистрации на сайте YaMDb отправьте Ваш userneme и"}',
            f'{"полученный код подтверждений {confirmation_code}"}',
            f'{"на /api/v1/auth/token/"}',
        ),
        from_email=None,
        recipient_list=[email],
    )
