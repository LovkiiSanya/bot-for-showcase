from django.db import models

FIRST_NAME_MAX_LENGTH = 30
LAST_NAME_MAX_LENGTH = 30
PHONE_NUMBER_MAX_LENGTH = 15
SELECTED_CITY_MAX_LENGTH = 100
SELECTED_DOCTOR_MAX_LENGTH = 100
CHAT_ID_MAX_LENGTH = 50
CUSTOMER_ID_MAX_LENGTH = 20
APPOINTMENT_STATUS_MAX_LENGTH = 50
APPOINTMENT_DATE_MAX_LENGTH = 200
STATE_CHAR_MAX_LENGTH = 50


STATE_CHOICES = (
    ("waiting_for_analysis_input", "Waiting for analysis input"),
    ("analysis_received", "Analysis received"),
    ("other", "Other"),
)


class Patient(models.Model):
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
    )
    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        blank=True,
        null=True,
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
    )
    selected_city = models.CharField(
        max_length=SELECTED_CITY_MAX_LENGTH,
        blank=True,
        null=True,
    )
    selected_doctor = models.CharField(
        max_length=SELECTED_CITY_MAX_LENGTH,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    review = models.TextField(
        blank=True,
        null=True,
    )
    is_anonymous = models.BooleanField(
        default=False,
    )
    chat_id = models.CharField(
        max_length=CHAT_ID_MAX_LENGTH,
    )
    customer_id = models.CharField(
        max_length=CUSTOMER_ID_MAX_LENGTH,
        blank=True,
        null=True,
    )
    requested_analysis = models.TextField(
        blank=True,
        null=True,
    )
    custom_question = models.TextField(
        null=True,
        blank=True,
    )
    appointment_status = models.CharField(
        max_length=APPOINTMENT_STATUS_MAX_LENGTH,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    appointment_date = models.CharField(
        max_length=APPOINTMENT_DATE_MAX_LENGTH,
        blank=True,
        null=True,
    )

    state = models.CharField(
        max_length=STATE_CHAR_MAX_LENGTH,
        choices=STATE_CHOICES,
        default="other",
    )

    def __str__(self):
        return "{} {} ({})".format(
            self.first_name,
            self.last_name,
            self.phone_number,
        )


class TemporaryPatient(models.Model):
    chat_id = models.CharField(
        max_length=CHAT_ID_MAX_LENGTH,
        unique=True,
    )
    selected_city = models.CharField(
        max_length=SELECTED_CITY_MAX_LENGTH,
        blank=True,
        null=True,
    )
    selected_doctor = models.CharField(
        max_length=SELECTED_DOCTOR_MAX_LENGTH,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)


STATUS_CHOICES = (
    ("open", "Open"),
    ("closed", "Closed"),
)


class TechSupportRequest(models.Model):

    phone_number = models.CharField(max_length=PHONE_NUMBER_MAX_LENGTH)
    chat_id = models.CharField(max_length=CHAT_ID_MAX_LENGTH)
    issue_description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default="open",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Tech Support Request from {} - Status: {}".format(
            self.phone_number,
            self.status,
        )
