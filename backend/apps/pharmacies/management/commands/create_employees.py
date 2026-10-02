from django.core.management.base import BaseCommand
from django.db import transaction
from apps.accounts.models import User
from apps.pharmacies.models import Pharmacy, PharmacyEmployee


class Command(BaseCommand):
    help = "Create or update the three demo employees for the single pharmacy."

    @transaction.atomic
    def handle(self, *args, **options):
        pharmacy = Pharmacy.objects.filter(license_number="DEMO-LICENSE-001").first()
        if not pharmacy:
            self.stderr.write("Run seed_demo before create_employees.")
            return
        for index in range(1, 4):
            email = f"employee{index}@demo.pharmacy"
            user, _ = User.objects.get_or_create(email=email)
            user.role = User.Role.EMPLOYEE
            user.first_name = f"Employee {index}"
            user.last_name = "M-Pharmacy"
            user.set_password(f"DemoEmployee{index}123!")
            user.save()
            PharmacyEmployee.objects.update_or_create(
                user=user, defaults={"pharmacy": pharmacy, "display_name": f"Employee {index}"}
            )
        self.stdout.write(self.style.SUCCESS("Three demo employees are ready."))
