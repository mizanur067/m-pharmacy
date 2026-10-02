from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import User
from apps.catalog.models import Category, Manufacturer, Medicine
from apps.inventory.models import PharmacyStock
from apps.pharmacies.models import Pharmacy
from apps.news.models import NewsArticle
from django.utils import timezone


class Command(BaseCommand):
    help = "Create repeatable demo accounts, pharmacies, catalog records, and stock."

    @transaction.atomic
    def handle(self, *args, **options):
        owner, _ = User.objects.get_or_create(
            email="owner@demo.pharmacy",
            defaults={
                "first_name": "Demo",
                "last_name": "Owner",
                "role": User.Role.PHARMACY_OWNER,
            },
        )
        owner.role = User.Role.PHARMACY_OWNER
        owner.first_name = "Demo"
        owner.last_name = "Owner"
        owner.set_password("DemoOwner123!")
        owner.save()

        customer, _ = User.objects.get_or_create(
            email="customer@demo.pharmacy",
            defaults={"first_name": "Demo", "last_name": "Customer", "role": User.Role.CUSTOMER},
        )
        customer.role = User.Role.CUSTOMER
        customer.first_name = "Demo"
        customer.last_name = "Customer"
        customer.set_password("DemoCustomer123!")
        customer.save()

        pharmacy, _ = Pharmacy.objects.get_or_create(
            license_number="DEMO-LICENSE-001",
            defaults={
                "owner": owner,
                "name": "Green Cross Pharmacy",
                "address": "12 Healthcare Avenue, Dhaka",
                "phone": "+880 1700 000000",
                "hours": {"everyday": "08:00-22:00"},
                "verification_status": Pharmacy.VerificationStatus.APPROVED,
            },
        )
        Pharmacy.objects.filter(pk=pharmacy.pk).update(
            owner=owner, name="Green Cross Pharmacy",
            verification_status=Pharmacy.VerificationStatus.APPROVED,
        )
        pharmacy.refresh_from_db()

        categories = {
            name: Category.objects.get_or_create(name=name, defaults={"slug": slug})[0]
            for name, slug in (
                ("Pain relief", "pain-relief"),
                ("Vitamins", "vitamins"),
                ("Cold and flu", "cold-and-flu"),
                ("Digestive health", "digestive-health"),
            )
        }
        manufacturers = {
            name: Manufacturer.objects.get_or_create(name=name, defaults={"slug": slug})[0]
            for name, slug in (
                ("HealthCare Labs", "healthcare-labs"),
                ("Wellness Pharma", "wellness-pharma"),
                ("Nova Medicines", "nova-medicines"),
            )
        }
        medicines = [
            ("Paracetamol 500", "Paracetamol", categories["Pain relief"], manufacturers["HealthCare Labs"], "Tablet", "500mg", False, "paracetamol-500"),
            ("Vitamin C Plus", "Ascorbic acid", categories["Vitamins"], manufacturers["Wellness Pharma"], "Tablet", "1000mg", False, "vitamin-c-plus"),
            ("Cetirizine", "Cetirizine hydrochloride", categories["Cold and flu"], manufacturers["Nova Medicines"], "Tablet", "10mg", False, "cetirizine-10"),
            ("Omeprazole", "Omeprazole", categories["Digestive health"], manufacturers["HealthCare Labs"], "Capsule", "20mg", True, "omeprazole-20"),
            ("Cough Relief Syrup", "Dextromethorphan", categories["Cold and flu"], manufacturers["Wellness Pharma"], "Syrup", "100ml", False, "cough-relief-syrup"),
            ("Calcium D3", "Calcium carbonate + Vitamin D3", categories["Vitamins"], manufacturers["Nova Medicines"], "Tablet", "600mg", False, "calcium-d3"),
        ]
        for index, (name, generic, category, manufacturer, form, strength, prescription, slug) in enumerate(medicines):
            medicine, _ = Medicine.objects.update_or_create(
                slug=slug,
                defaults={
                    "created_by": owner,
                    "name": name,
                    "generic_name": generic,
                    "category": category,
                    "manufacturer": manufacturer,
                    "dosage_form": form,
                    "strength": strength,
                    "description": f"Demo catalog description for {name}.",
                    "uses": "Use only as directed on the packaging or by a healthcare professional.",
                    "side_effects": "Read the package leaflet for possible side effects.",
                    "requires_prescription": prescription,
                    "is_active": True,
                },
            )
            PharmacyStock.objects.update_or_create(
                pharmacy=pharmacy,
                medicine=medicine,
                batch_number=f"DEMO-{index + 1:03d}",
                defaults={
                    "price": Decimal(str((index + 1) * 3 + 5)),
                    "discount_percent": Decimal("5.00") if index % 2 else Decimal("0.00"),
                    "quantity": 25 + index * 5,
                    "expiry_date": date.today() + timedelta(days=180 + index * 30),
                    "is_available": True,
                    "is_active": True,
                },
            )
        NewsArticle.objects.update_or_create(
            slug="welcome-to-m-pharmacy",
            defaults={
                "title": "Welcome to M-Pharmacy",
                "summary": "Simple, reliable access to everyday healthcare products.",
                "body": "Browse our catalog, compare available stock, and place a convenient cash-on-delivery order.",
                "author": owner,
                "published_at": timezone.now(),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
        self.stdout.write("Customer: customer@demo.pharmacy / DemoCustomer123!")
        self.stdout.write("Owner:    owner@demo.pharmacy / DemoOwner123!")
        self.stdout.write("Employees are created with: python manage.py create_employees")
