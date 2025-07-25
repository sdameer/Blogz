from djoser import email

class ActivationEmail(email.ActivationEmail):
    template_name = 'email/activation.html'
    
class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'email/confirmation.html'
    
class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'email/password_reset.html'
    
class PasswordChangedConfirmation(email.PasswordChangedConfirmationEmail):
    template_name = 'email/password_changed_confirmation.html'
    
    