from notifications.models import Message


class SendNotificationService:
    @staticmethod
    def seneMessagewithPaylod( title, message, recipients, data):
        messgge = Message.objects.create(
            title=title,
            message=message,
            data=data

        )
        print(recipients)
        messgge.recipients.set(recipients)
        messgge.save()
