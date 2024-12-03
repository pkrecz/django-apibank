from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management.base import BaseCommand
from .models import ParameterModel

cmd = BaseCommand()

parameter_to_be_created = {
                            "country_code": "PL",
                            "bank_number": "10101397"}


def create_parameter(parameters):
    instance, created = ParameterModel.objects.get_or_create(**parameters)
    if created:
        message = f"  Parameters have been created."
        cmd.stdout.write(cmd.style.MIGRATE_LABEL(message))


@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if sender.name == "apibankapp":
        cmd.stdout.write(cmd.style.MIGRATE_HEADING("Custom initial data upload:"))
        create_parameter(parameter_to_be_created)
        cmd.stdout.write(cmd.style.MIGRATE_LABEL("  Initial data complete."))
