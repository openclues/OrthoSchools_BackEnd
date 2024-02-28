import firebase_admin
from firebase_admin import credentials, messaging

from blog.models import Blog
from djangoProject1 import settings
from notifications.models import Device, Message
from useraccount.models import UserAccount

firebase_config = settings.firebaseConfig

cred = credentials.Certificate("djangoProject1/service_key.json")
firebase_admin.initialize_app(cred)


class FirebaseServices:
    def __init__(self):
        self.firebase_config = firebase_config
        self.cred = cred
        self.firebase_admin = firebase_admin

    def get_firebase_admin(self):
        return self.firebase_admin

    def get_firebase_config(self):
        return self.firebase_config

    def get_firebase_cred(self):
        return self.cred

    def Send_Notification_for_to_user(self, title, body, user_id, data):
        user_devices = Device.objects.filter(user_id=user_id)
        fcm_messages = []
        notification = messaging.Notification(
            title=title,
            body=body
        )

        message_data = {
            "data": str(data)  # Add your custom data here
        }

        for device in user_devices:
            token = device.fcm_token
            fcm_message = messaging.Message(
                notification=notification,
                data=message_data,
                token=token
            )
            fcm_messages.append(fcm_message)

        messaging.send_each(fcm_messages)


    def Send_Notification_for_to_all(self, title, body, data):
        user_devices = Device.objects.all()
        fcm_messages = []
        notification = messaging.Notification(
            title=title,
            body=body
        )
        message_data = {
            "data": str(data)  # Add your custom data here
        }

        for device in user_devices:
            token = device.fcm_token
            fcm_message = messaging.Message(
                notification=notification,
                data=message_data,
                token=token
            )
            fcm_messages.append(fcm_message)

        messaging.send_each(fcm_messages)

    def send_notification_for_blog_followers(self, blog_id, title, body, data):
        blog = Blog.objects.get(id=blog_id)
        user_devices = Device.objects.filter(user__in=blog.followers.all())
        fcm_messages = []
        notification = messaging.Notification(
            title=title,
            body=body
        )

        message_data = {
            "data": str(data)  # Add your custom data here
        }

        for device in user_devices:
            token = device.fcm_token
            fcm_message = messaging.Message(

                notification=notification,
                data=message_data,
                token=token
            )
            fcm_messages.append(fcm_message)

        messaging.send_each(fcm_messages)

    def register_device_for_push_notification(user_id, device_id, fcm_token):
        """
        Saves the device information in the database for sending push notifications later
        """
        device, created = Device.objects.get_or_create(user_id=user_id, device_id=device_id)
        device.fcm_token = fcm_token
        device.save()

    @staticmethod
    def sendNotification(title, message, data, recipients):
        notification = messaging.Notification(
            title=title,

            body=message
        )

        message_data = {

            "data": str(data)  # Add your custom data here
        }

        # Create the FCM message for each recipient
        fcm_messages = []
        for recipient in recipients:
            recipient = UserAccount.objects.filter(id=recipient).first()
            if recipient:
                devices = Device.objects.filter(user=recipient)
                for device in devices:
                    token = device.fcm_token
                    fcm_message = messaging.Message(

                        notification=notification,
                        data=message_data,
                        token=token
                    )
                    fcm_messages.append(fcm_message)

        # Send the FCM messages
        messaging.send_each(fcm_messages)
        FirebaseServices.SaveMessage(title, message, data, recipients)

    @staticmethod
    def SaveMessage(title, message, data, recipients):
        # Construct the message payload
        mess = Message.objects.create(
            message=message,
            title=title,
            data=data, )
        # Create and save the Message instance
        # Add recipients to the message
        mess.recipients.set(recipients)

        return mess
