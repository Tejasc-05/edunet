from django.core.management.base import BaseCommand
from waste.models import Coupon
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate sample coupons for testing'

    def handle(self, *args, **options):
        coupons = [
            {
                'name': 'Eco-Friendly Starter',
                'description': 'Get 10% off on eco-friendly products and sustainable alternatives.',
                'points_required': 50,
                'discount_percentage': 10,
                'discount_amount': 0,
                'coupon_code': 'ECO10',
                'icon': '🌱',
                'color': '#2ecc71',
                'active': True,
                'max_uses': 100,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=90),
            },
            {
                'name': 'Green Hero Premium',
                'description': 'Enjoy 15% discount on your next purchase of reusable items.',
                'points_required': 100,
                'discount_percentage': 15,
                'discount_amount': 0,
                'coupon_code': 'GREEN15',
                'icon': '🏆',
                'color': '#27ae60',
                'active': True,
                'max_uses': 50,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=120),
            },
            {
                'name': 'Waste Warrior Special',
                'description': 'Get ₹200 cashback on your next environmental product purchase.',
                'points_required': 150,
                'discount_percentage': 0,
                'discount_amount': 200,
                'coupon_code': 'WARRIOR200',
                'icon': '⚔️',
                'color': '#c0392b',
                'active': True,
                'max_uses': 75,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=150),
            },
            {
                'name': 'Planet Protector Elite',
                'description': 'Exclusive 20% discount on all sustainable lifestyle brands.',
                'points_required': 200,
                'discount_percentage': 20,
                'discount_amount': 0,
                'coupon_code': 'PLANET20',
                'icon': '🌍',
                'color': '#0084d6',
                'active': True,
                'max_uses': 30,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=180),
            },
            {
                'name': 'Zero Waste Champion',
                'description': 'Get ₹500 off on eco-certified products. Minimum purchase ₹2000.',
                'points_required': 250,
                'discount_percentage': 0,
                'discount_amount': 500,
                'coupon_code': 'ZEROWASTE500',
                'icon': '♻️',
                'color': '#16a085',
                'active': True,
                'max_uses': 20,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=365),
            },
            {
                'name': 'Sustainability Ambassador',
                'description': 'Premium member perks: 25% discount on all future purchases.',
                'points_required': 300,
                'discount_percentage': 25,
                'discount_amount': 0,
                'coupon_code': 'AMBASSADOR25',
                'icon': '👑',
                'color': '#8e44ad',
                'active': True,
                'max_uses': 10,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=365),
            },
        ]

        created_count = 0
        for coupon_data in coupons:
            coupon, created = Coupon.objects.get_or_create(
                coupon_code=coupon_data['coupon_code'],
                defaults=coupon_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created coupon: {coupon.name}'))
            else:
                self.stdout.write(f'Coupon already exists: {coupon.name}')

        self.stdout.write(self.style.SUCCESS(f'\nTotal created: {created_count} new coupons'))
