from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = 'emails/activation.html'


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "emails/password_reset.html"


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "emails/password_changed_confirmation.html"
