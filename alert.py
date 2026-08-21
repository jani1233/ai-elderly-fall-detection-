import os
from datetime import datetime

from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()


class SMSAlert:

    def __init__(self):

        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

        self.enabled = all([
            self.account_sid,
            self.auth_token,
            self.twilio_number
        ])

        if self.enabled:
            self.client = Client(
                self.account_sid,
                self.auth_token
            )
        else:
            self.client = None

    def send_sms(
        self,
        to_number,
        message
    ):

        if not to_number:

            return {
                "success": False,
                "message": "Family member phone number is missing."
            }

        if not self.enabled:

            return {
                "success": False,
                "message": "Twilio is not configured in .env"
            }

        try:

            sms = self.client.messages.create(
                body=message,
                from_=self.twilio_number,
                to=to_number
            )

            return {
                "success": True,
                "message": "SMS sent successfully.",
                "sid": sms.sid
            }

        except Exception as e:

            return {
                "success": False,
                "message": str(e)
            }

    def send_fall_alert(
        self,
        person,
        family
    ):

        person_name = person.get(
            "name",
            "Elderly Person"
        )

        family_name = family.get(
            "name",
            "Family Member"
        )

        room = person.get(
            "room",
            "Unknown location"
        )

        current_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

        message = (
            "🚨 FALL ALERT 🚨\n\n"
            f"Hello {family_name},\n\n"
            f"A possible fall has been detected "
            f"for {person_name}.\n\n"
            f"Location: {room}\n"
            f"Time: {current_time}\n\n"
            "Please check on the person immediately.\n\n"
            "AI Elderly Fall Detection System"
        )

        return self.send_sms(
            family.get("phone"),
            message
        )

    def send_emergency_alert(
        self,
        person,
        family
    ):

        person_name = person.get(
            "name",
            "Elderly Person"
        )

        family_name = family.get(
            "name",
            "Family Member"
        )

        room = person.get(
            "room",
            "Unknown location"
        )

        current_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

        message = (
            "🚨 EMERGENCY ALERT 🚨\n\n"
            f"Hello {family_name},\n\n"
            f"Emergency assistance has been "
            f"requested for {person_name}.\n\n"
            f"Location: {room}\n"
            f"Time: {current_time}\n\n"
            "Please check on the person immediately.\n\n"
            "AI Elderly Fall Detection System"
        )

        return self.send_sms(
            family.get("phone"),
            message
        )