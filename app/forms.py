"""
A module containing the forms used in the application.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from email_validator import validate_email, EmailNotValidError


class FileUploadForm(FlaskForm):
    """
    A form for uploading files and sharing them with other users via email.

    Attributes:
    -----------
    file : FileField
        The file to be uploaded.
    emails : FieldList
        A list of email addresses to share the file with.
    submit : SubmitField
        A button to submit the form and upload the file.
    """

    file = FileField("Choose File", validators=[DataRequired()])
    emails = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Upload")

    def validate_emails(self, field):
        """
        Validates Emails by splitting them by comma and validating each one.
        """
        emails = field.data.split(",")
        emails = [email.strip() for email in emails]
        if len(emails) > 5:
            raise ValidationError("You can only share with a maximum of 5 people.")
        for email in emails:
            try:
                validate_email(email)
            except EmailNotValidError as exe:
                raise ValidationError(f"Invalid email: {email}. Try Again") from exe


class RegistrationForm(FlaskForm):
    """
    A class representing a registration form for the application.

    Attributes:
    -----------
    email : str
        The email address of the user.
    password : str
        The password of the user.
    confirm_password : str
        The password of the user, entered a second time to confirm it was entered correctly.

    Methods:
    --------
    validate_email(self, email: str):
        Returns True if the given email address is not already in use, False otherwise.
    """

    full_name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """
    A class representing a login form for the application.

    Attributes:
    -----------
    email : str
        The email address of the user.
    password : str
        The password of the user.

    Methods:
    --------
    validate_email(self, email: str):
        Returns True if the given email address is in use, False otherwise.
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
