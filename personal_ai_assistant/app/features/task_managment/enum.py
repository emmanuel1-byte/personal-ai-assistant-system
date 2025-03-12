from enum import Enum


class Email_Provider(Enum):
    GMAIL = "Gmail"
    ZOHO_MAIL = "Zoho mail"


class Email_Type(Enum):
    REPORT_EMAIL = "Report"
    INVITATION_EMAIL = "Invitation"
    PERSONAL_EMAIL = "Personal"
    BUSINESS_EMAIL = "Business"