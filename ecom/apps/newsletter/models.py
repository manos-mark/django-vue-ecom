from django.db import models

class Subscriber(models.Model):
    """
    Saves the visitor's email for newsletter
    """
    email = models.EmailField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Get the email
        Return:
            -[String] The subscriber's email
        """
        return '%s' % self.email