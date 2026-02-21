from django.db import models
from django.contrib.auth.models import User

class WasteCategory(models.Model):
    CATEGORY_CHOICES = [
        ('biodegradable', 'Biodegradable'),
        ('plastic', 'Plastic'),
        ('ewaste', 'E-Waste'),
        ('metal', 'Metal'),
        ('glass', 'Glass'),
        ('hazardous', 'Hazardous'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    icon = models.CharField(max_length=50)  # Font Awesome icon class
    description = models.TextField()
    color = models.CharField(max_length=7, default='#2ecc71')  # Hex color
    treatment_method = models.TextField(default='')
    environmental_impact = models.TextField(default='')
    
    class Meta:
        verbose_name_plural = "Waste Categories"
    
    def __str__(self):
        return self.get_name_display()


class WasteReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    quantity = models.FloatField()  # in kg
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=255, default='Bangalore, India')
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.quantity}kg"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, default='Bangalore, India — 560061')
    total_waste_recorded = models.FloatField(default=0)
    
    def __str__(self):
        return self.user.username


class UserPoints(models.Model):
    """Track points earned by users for waste disposal"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='points')
    total_points = models.IntegerField(default=0)
    redeemed_points = models.IntegerField(default=0)
    available_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Points"
        verbose_name_plural = "User Points"
    
    def __str__(self):
        return f"{self.user.username} - {self.available_points} points"
    
    def save(self, *args, **kwargs):
        """Auto-calculate available points"""
        self.available_points = self.total_points - self.redeemed_points
        super().save(*args, **kwargs)


class PointsTransaction(models.Model):
    """Log all points transactions (earned/redeemed)"""
    TRANSACTION_TYPES = [
        ('earned', 'Earned'),
        ('redeemed', 'Redeemed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_transactions')
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255)
    waste_report = models.ForeignKey(WasteReport, null=True, blank=True, on_delete=models.SET_NULL)
    coupon = models.ForeignKey('Coupon', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.points}pts"


class Coupon(models.Model):
    """Redeemable coupons for accumulated points"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.IntegerField()
    discount_percentage = models.IntegerField(default=10)  # 10% off
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Fixed amount
    coupon_code = models.CharField(max_length=20, unique=True)
    icon = models.CharField(max_length=50, default='fa-tag')  # Font Awesome icon
    color = models.CharField(max_length=7, default='#06b6d4')  # Hex color
    active = models.BooleanField(default=True)
    max_uses = models.IntegerField(null=True, blank=True)  # Unlimited if null
    current_uses = models.IntegerField(default=0)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)  # No expiry if null
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['points_required']
    
    def __str__(self):
        return f"{self.name} ({self.points_required} pts) - {self.coupon_code}"
    
    def is_available(self):
        """Check if coupon is still available"""
        if not self.active:
            return False
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        if self.valid_until and self.valid_until < models.F('created_at'):
            return False
        return True


class UserCoupon(models.Model):
    """Track redeemed coupons by users - allows multiple of same coupon"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='redeemed_coupons')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Number of this coupon owned
    first_redeemed_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'coupon')  # Still unique per user-coupon pair, but tracks quantity
        ordering = ['-last_updated']
    
    def __str__(self):
        return f"{self.user.username} - {self.coupon.coupon_code}"
