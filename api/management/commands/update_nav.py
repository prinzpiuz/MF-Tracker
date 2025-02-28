from django.core.management.base import BaseCommand
from api.models import MutualFund
from api.utils import get_single_fund_details


class Command(BaseCommand):
    help = "Updates NAV values for mutual funds"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Updating NAV values..."))
        funds = MutualFund.objects.all()
        for fund in funds:
            self.stdout.write(f"Updating NAV for {fund.name}")
            scheme_code = fund.scheme_Code
            fund_details = get_single_fund_details(scheme_code=scheme_code)
            if fund_details:
                try:
                    nav = fund_details["Net_Asset_Value"]
                    self.style.SUCCESS("Updated NAV for {fund.name}")
                    fund.nav = nav
                    fund.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"Updated NAV for {fund.name}")
                    )
                except KeyError:
                    self.stdout.write(
                        self.style.ERROR(f"Invalid fund details for {scheme_code}")
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f"Failed to fetch fund details for {scheme_code}")
                )
        self.stdout.write(self.style.SUCCESS("NAV update completed."))
