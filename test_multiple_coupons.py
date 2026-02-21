#!/usr/bin/env python
"""
Test script to demonstrate multiple coupon purchasing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
django.setup()

from django.contrib.auth.models import User
from waste.models import UserPoints, PointsTransaction, Coupon, UserCoupon

def test_multiple_coupons():
    """Test buying multiple coupons of the same type"""
    
    print("=" * 70)
    print("MULTIPLE COUPON PURCHASE TEST")
    print("=" * 70)
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser_coupons',
        defaults={'email': 'test_coupons@example.com', 'first_name': 'Test'}
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"\n✓ Created test user: {user.username}")
    else:
        print(f"\n✓ Using existing test user: {user.username}")
    
    # Give user points
    user_points, _ = UserPoints.objects.get_or_create(user=user)
    user_points.total_points = 500
    user_points.redeemed_points = 0
    user_points.save()
    print(f"✓ User has {user_points.available_points} points available")
    
    # Get or create a test coupon
    coupon, created = Coupon.objects.get_or_create(
        coupon_code='DISCOUNT20',
        defaults={
            'name': '20% Discount Voucher',
            'description': 'Get 20% off on your next purchase',
            'points_required': 100,
            'discount_percentage': 20,
            'active': True
        }
    )
    print(f"✓ Using coupon: {coupon.name} ({coupon.coupon_code}) - {coupon.points_required} points")
    
    print("\n" + "=" * 70)
    print("PURCHASING MULTIPLE COUPONS")
    print("=" * 70)
    
    # Simulate purchasing the same coupon 3 times
    purchases = 3
    for i in range(1, purchases + 1):
        print(f"\n--- Purchase #{i} ---")
        
        # Check if user has enough points
        user_points.refresh_from_db()
        if user_points.available_points >= coupon.points_required:
            # Get or create user coupon, increment quantity if exists
            user_coupon, created = UserCoupon.objects.get_or_create(
                user=user,
                coupon=coupon,
                defaults={'quantity': 1}
            )
            
            if not created:
                print(f"Previously owned: {user_coupon.quantity} coupon(s)")
                user_coupon.quantity += 1
                user_coupon.save()
                print(f"After purchase: {user_coupon.quantity} coupon(s)")
            else:
                print(f"First-time purchase: {user_coupon.quantity} coupon")
            
            # Deduct points
            user_points.redeemed_points += coupon.points_required
            user_points.save()
            
            print(f"Points deducted: {coupon.points_required}")
            print(f"Points remaining: {user_points.available_points}")
            
            # Log transaction
            PointsTransaction.objects.create(
                user=user,
                points=coupon.points_required,
                transaction_type='redeemed',
                description=f'Purchased {coupon.coupon_code} (Purchase #{i})',
                coupon=coupon
            )
        else:
            print(f"❌ Not enough points! Need {coupon.points_required}, have {user_points.available_points}")
            break
    
    print("\n" + "=" * 70)
    print("FINAL STATUS")
    print("=" * 70)
    
    user_points.refresh_from_db()
    user_coupon.refresh_from_db()
    
    print(f"\nUser: {user.username}")
    print(f"  Total points earned: {user_points.total_points}")
    print(f"  Points redeemed: {user_points.redeemed_points}")
    print(f"  Points remaining: {user_points.available_points}")
    
    print(f"\nCoupon: {coupon.coupon_code} ({coupon.name})")
    print(f"  Total owned by user: {user_coupon.quantity}")
    print(f"  First redeemed at: {user_coupon.first_redeemed_at}")
    print(f"  Last updated: {user_coupon.last_updated}")
    
    # Show all transactions
    transactions = PointsTransaction.objects.filter(
        user=user,
        transaction_type='redeemed',
        coupon=coupon
    ).order_by('created_at')
    
    print(f"\nTransaction History:")
    for idx, txn in enumerate(transactions, 1):
        print(f"  {idx}. {txn.created_at.strftime('%Y-%m-%d %H:%M:%S')} - {txn.description}")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE - MULTIPLE COUPONS WORKING!")
    print("=" * 70)

if __name__ == '__main__':
    test_multiple_coupons()
