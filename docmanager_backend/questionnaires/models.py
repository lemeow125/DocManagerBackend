from django.db import models
from django.utils.timezone import now


class Questionnaire(models.Model):
    # Personal Information
    # Email address is derived from the user and is no longer optional
    client = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    CLIENT_TYPE_CHOICES = (
        ("citizen", "Citizen"),
        ("business", "Business"),
        ("government", "Government (Employee or Another Agency)"),
    )
    client_type = models.CharField(
        max_length=32, choices=CLIENT_TYPE_CHOICES, null=False, blank=False
    )

    date_submitted = models.DateTimeField(default=now, editable=False)

    region_of_residence = models.CharField(
        max_length=64, null=False, blank=False)
    service_availed = models.CharField(max_length=64, null=False, blank=False)
    I_AM_I_CHOICES = (
        ("faculty", "Faculty"),
        ("non-teaching staff", "Non-Teaching Staff"),
        ("student", "Student"),
        ("guardian", "Guardian/Parent of Student"),
        ("alumna", "Alumna"),
        ("other", "Other"),
    )
    i_am_a = models.CharField(
        max_length=32, choices=I_AM_I_CHOICES, null=False, blank=False
    )
    # This is filled up if i_am_a=other
    i_am_a_other = models.CharField(max_length=64, null=True, blank=True)

    # CC Questions
    Q1_CHOICES = (
        ("1", "I know what a CC is and I saw this office's CC"),
        ("2", "I know what a CC is but I did NOT see this office's CC"),
        ("3", "I learned of the CC only when I saw this office's CC"),
        ("4", "I do not know what a CC is and I did not see one in this office"),
    )
    q1_answer = models.CharField(
        max_length=64, choices=Q1_CHOICES, null=False, blank=False
    )

    Q2_CHOICES = (
        ("1", "Easy to see"),
        ("2", "Somewhat easy to see"),
        ("3", "Difficult to see"),
        ("4", "Not visible at all"),
        ("5", "N/A"),
    )
    q2_answer = models.CharField(
        max_length=64, choices=Q2_CHOICES, null=False, blank=False
    )

    Q3_CHOICES = (
        ("1", "Helped very much"),
        ("2", "Somewhat helped"),
        ("3", "Did not help"),
        ("4", "N/A"),
    )
    q3_answer = models.CharField(
        max_length=64, choices=Q3_CHOICES, null=False, blank=False
    )

    # SQD Questions
    SQD_CHOICES = (
        ("1", "Strongly Disagree"),
        ("2", "Disagree"),
        ("3", "Neither Agree nor Disagree"),
        ("4", "Agree"),
        ("5", "Strongly Agree"),
        ("6", "N/A"),
    )

    sqd0_answer = models.CharField(
        max_length=16, choices=SQD_CHOICES, null=False, blank=False
    )
    sqd1_answer = models.CharField(
        max_length=16, choices=SQD_CHOICES, null=False, blank=False
    )
    sqd2_answer = models.CharField(
        max_length=16, choices=SQD_CHOICES, null=False, blank=False
    )
    sqd3_answer = models.CharField(
        max_length=16, choices=SQD_CHOICES, null=False, blank=False
    )
    sqd4_answer = models.CharField(
        max_length=16, choices=SQD_CHOICES, null=False, blank=False
    )
    sqd5_answer = models.CharField(
        max_length=16, choices=SQD_CHOICES, null=False, blank=False
    )
    sqd6_answer = models.CharField(
        max_length=16, choices=SQD_CHOICES, null=False, blank=False
    )
    sqd7_answer = models.CharField(
        max_length=16, choices=SQD_CHOICES, null=False, blank=False
    )
    sqd8_answer = models.CharField(
        max_length=16, choices=SQD_CHOICES, null=False, blank=False
    )

    extra_suggestions = models.TextField(max_length=512, null=True, blank=True)
