# from django.db.models.signals import pre_delete
# from django.dispatch import receiver
# from .models import Account, Destination, AccountMember

# @receiver(pre_delete, sender=Account)
# def delete_related_destinations_and_members(sender, instance, **kwargs):
#     # Delete all destinations related to the account
#     destinations = Destination.objects.filter(account=instance)
#     destinations.delete()

#     # Delete all account members related to the account
#     account_members = AccountMember.objects.filter(account=instance)
#     account_members.delete()