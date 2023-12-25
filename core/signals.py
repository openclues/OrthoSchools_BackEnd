from actstream.models import Action
from django.db.models.signals import post_save
from django.dispatch import receiver

from space.models import Space
from useraccount.models import UserAccount, ProfileModel


@receiver(post_save, sender=Space)
def add_premium_users_to_space(sender, instance, created, **kwargs):
    if created:
        print("created")
        if instance.allowed_user_types == "premium":
            premium_users = UserAccount.objects.filter(userRole=2).values_list('id', flat=True)
            instance.include_users.set(premium_users)
            space = Space.objects.filter(id=instance.id).first()
            print(space.include_users.all())

    if not created:
        print("not created")
        if instance.allowed_user_types == "premium":
            premium_users = UserAccount.objects.filter(userRole=2).values_list('id', flat=True)
            instance.include_users.set(premium_users)
            space = Space.objects.filter(id=instance.id).first()
            print(space.include_users.all())


@receiver(post_save, sender=UserAccount)
def add_premium_users_to_space(sender, instance, created, **kwargs):
    if created:
        if instance.userRole == 1:
            spaces = Space.objects.filter(allowed_user_types="premium")
            for space in spaces:
                space.include_users.remove(instance)
                space.save()
        if instance.userRole == 2:
            spaces = Space.objects.filter(allowed_user_types="premium")
            for space in spaces:
                space.include_users.add(instance)
                space.save()
                print(space.include_users.all())

    if not created:
        if instance.userRole == 1:
            print("removing")
            spaces = Space.objects.filter(allowed_user_types="premium")
            for space in spaces:
                space.include_users.remove(instance)
                space.save()
                print(space.include_users.all())

        if instance.userRole == 2:
            spaces = Space.objects.filter(allowed_user_types="premium")
            for space in spaces:
                space.include_users.add(instance)
                space.save()
                print(space.include_users.all())


@receiver(post_save, sender=UserAccount)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)
        print("profile created")
    else:
        print("profile not created")


@receiver(post_save, sender=Action)
def send_notification_on_action_with_target_post_in_users_space(sender, instance, created, **kwargs):
    if created and instance.target_content_type.name == 'space' and instance.verb == 'joined':
        space = Space.objects.filter(id=instance.target_object_id).first()
        if space is not None:
            users = space.include_users.all()
            for user in users:
                if user != instance.actor:
                    print("sending notification" + str(user.email))



