from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import WasteCategory, WasteReport, UserProfile, UserPoints, PointsTransaction, Coupon, UserCoupon
from .forms import LoginForm, SignUpForm, WasteReportForm
from .waste_classifier import WasteClassifier, WASTE_DESCRIPTIONS
import json
from datetime import datetime
from PIL import Image
import base64
import io

# Authentication Views
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('waste:dashboard')
                else:
                    form.add_error(None, 'Invalid email or password')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    
    return render(request, 'waste/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('waste:dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'waste/signup.html', {'form': form})


@login_required(login_url='waste:login')
def logout_view(request):
    logout(request)
    return redirect('waste:login')


# Main Views
@login_required(login_url='waste:login')
def index_view(request):
    """Home/Dashboard page"""
    waste_categories = WasteCategory.objects.all()
    user_reports = WasteReport.objects.filter(user=request.user)
    
    # Calculate statistics
    total_waste = user_reports.aggregate(Sum('quantity'))['quantity__sum'] or 0
    reports_count = user_reports.count()
    
    # Get user profile
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_profile.total_waste_recorded = total_waste
    user_profile.save()
    
    # Get or create user points
    user_points, _ = UserPoints.objects.get_or_create(user=request.user)
    
    # Build URLs for each category
    for category in waste_categories:
        category.detail_url = reverse('waste:' + category.name)
    
    context = {
        'waste_categories': waste_categories,
        'total_waste': total_waste,
        'reports_count': reports_count,
        'user_name': request.user.first_name or request.user.username,
        'location': user_profile.location,
        'user_points': user_points,
    }
    
    return render(request, 'waste/dashboard.html', context)


@login_required(login_url='waste:login')
def category_detail(request, category_name):
    """Detailed view for each waste category"""
    category = get_object_or_404(WasteCategory, name=category_name)
    user_reports = WasteReport.objects.filter(user=request.user, category=category)
    
    total_for_category = user_reports.aggregate(Sum('quantity'))['quantity__sum'] or 0
    reports_for_category = user_reports.count()
    
    context = {
        'category': category,
        'total_waste': total_for_category,
        'reports_count': reports_for_category,
        'user_reports': user_reports[:10],  # Latest 10 reports
    }
    
    return render(request, 'waste/category_detail.html', context)


# API Views for AJAX requests
@login_required(login_url='waste:login')
@require_http_methods(["POST"])
def add_waste_report(request):
    """Add a new waste report via AJAX"""
    form = WasteReportForm(request.POST)
    
    if form.is_valid():
        waste_report = form.save(commit=False)
        waste_report.user = request.user
        waste_report.save()
        
        # Award points for the waste disposal
        points_earned = add_points_for_waste(request.user, waste_report.quantity)
        
        return render(request, 'waste/report_success.html', {
            'report': waste_report,
            'message': f'Successfully recorded {waste_report.quantity}kg of {waste_report.category.name} waste!',
            'points_earned': points_earned,
        })
    else:
        return render(request, 'waste/report_form.html', {'form': form})


@login_required(login_url='waste:login')
def get_statistics(request):
    """Get user statistics as JSON"""
    user_reports = WasteReport.objects.filter(user=request.user)
    
    stats_by_category = {}
    for category in WasteCategory.objects.all():
        category_total = user_reports.filter(category=category).aggregate(Sum('quantity'))['quantity__sum'] or 0
        stats_by_category[category.name] = {
            'total': category_total,
            'color': category.color,
            'icon': category.icon
        }
    
    return render(request, 'waste/statistics.json', {
        'stats': json.dumps(stats_by_category),
        'total_waste': user_reports.aggregate(Sum('quantity'))['quantity__sum'] or 0,
        'reports_count': user_reports.count(),
    }, content_type='application/json')


@login_required(login_url='waste:login')
def user_reports(request):
    """View all user reports"""
    reports = WasteReport.objects.filter(user=request.user)
    
    context = {
        'reports': reports,
        'total_waste': reports.aggregate(Sum('quantity'))['quantity__sum'] or 0,
    }
    
    return render(request, 'waste/user_reports.html', context)


# Camera Scanning Views
@login_required(login_url='waste:login')
def camera_scan(request):
    """Camera scanning interface for waste classification"""
    waste_categories = WasteCategory.objects.all()
    
    context = {
        'waste_categories': waste_categories,
    }
    
    return render(request, 'waste/camera_scan.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def classify_waste_api(request):
    """API endpoint for waste classification from camera image"""
    try:
        # Get image data from request (handle both POST form data and JSON)
        image_data = None
        
        # Try JSON first
        try:
            data = json.loads(request.body)
            image_data = data.get('image')
        except:
            # Fall back to POST data
            image_data = request.POST.get('image')
        
        if not image_data:
            return JsonResponse({
                'success': False,
                'message': 'No image provided'
            }, status=400)
        
        # Get other optional parameters from POST
        quantity = float(request.POST.get('quantity', 0)) or 0
        location = request.POST.get('location', '')
        notes = request.POST.get('notes', '')
        
        # Decode base64 image
        try:
            if ',' in image_data:
                # Remove data:image/jpeg;base64, or data:image/png;base64, prefix
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            # Verify image is valid by checking it can be read
            image.load()
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=400)
        
        # Classify the waste using AI model
        try:
            classifier = WasteClassifier()
            classification_result = classifier.classify_image(image)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Classification error: {str(e)}'
            }, status=500)
        
        if not classification_result['success']:
            return JsonResponse({
                'success': False,
                'message': classification_result.get('message', 'Classification failed')
            }, status=400)
        
        # Get the waste category
        category_name = classification_result['category']
        category = get_object_or_404(WasteCategory, name=category_name)
        
        # Create waste report if user confirms
        if request.POST.get('save_report') == 'true':
            if quantity <= 0:
                return JsonResponse({
                    'success': False,
                    'message': 'Please enter quantity in kg'
                }, status=400)
            
            waste_report = WasteReport.objects.create(
                user=request.user,
                category=category,
                quantity=quantity,
                location=location or 'Bangalore, India',
                notes=notes
            )
            
            # Update user profile
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            user_reports = WasteReport.objects.filter(user=request.user)
            user_profile.total_waste_recorded = user_reports.aggregate(Sum('quantity'))['quantity__sum'] or 0
            user_profile.save()
            
            return JsonResponse({
                'success': True,
                'message': f"{classification_result['category_display']} waste recorded successfully!",
                'category': category_name,
                'category_display': classification_result['category_display'],
                'confidence': classification_result['confidence'],
                'description': classification_result['description'],
                'examples': classification_result['examples'],
                'saved': True,
                'icon': category.icon,
                'color': category.color
            })
        else:
            # Just return classification result without saving
            return JsonResponse({
                'success': True,
                'message': classification_result['message'],
                'category': category_name,
                'category_display': classification_result['category_display'],
                'confidence': classification_result['confidence'],
                'description': classification_result['description'],
                'examples': classification_result['examples'],
                'all_scores': classification_result.get('all_scores', {}),
                'saved': False,
                'icon': category.icon,
                'color': category.color
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


# Points and Coupon Views
def add_points_for_waste(user, quantity_kg):
    """Award points to user for waste disposal (1 kg = 10 points)"""
    points_earned = int(quantity_kg * 10)
    
    # Get or create UserPoints
    user_points, created = UserPoints.objects.get_or_create(user=user)
    user_points.total_points += points_earned
    user_points.save()
    
    # Log transaction
    PointsTransaction.objects.create(
        user=user,
        points=points_earned,
        transaction_type='earned',
        description=f'Earned for disposing {quantity_kg}kg of waste'
    )
    
    return points_earned


@login_required(login_url='waste:login')
def coupons_view(request):
    """Display available coupons for redemption"""
    user_points, _ = UserPoints.objects.get_or_create(user=request.user)
    all_coupons = Coupon.objects.filter(active=True)
    
    # Mark which coupons user can afford
    for coupon in all_coupons:
        coupon.can_redeem = user_points.available_points >= coupon.points_required
        coupon.already_redeemed = UserCoupon.objects.filter(user=request.user, coupon=coupon).exists()
    
    context = {
        'user_points': user_points,
        'coupons': all_coupons,
    }
    return render(request, 'waste/coupons.html', context)


@login_required(login_url='waste:login')
@require_http_methods(["POST"])
def redeem_coupon(request):
    """Redeem a coupon using accumulated points"""
    try:
        coupon_id = request.POST.get('coupon_id')
        coupon = get_object_or_404(Coupon, id=coupon_id)
        
        user_points, _ = UserPoints.objects.get_or_create(user=request.user)
        
        # Check if user has enough points
        if user_points.available_points < coupon.points_required:
            return JsonResponse({
                'success': False,
                'message': f'Not enough points. You need {coupon.points_required} points but have {user_points.available_points}.'
            })
        
        # Check if already redeemed
        if UserCoupon.objects.filter(user=request.user, coupon=coupon).exists():
            return JsonResponse({
                'success': False,
                'message': 'You have already redeemed this coupon.'
            })
        
        # Redeem coupon
        user_coupon = UserCoupon.objects.create(user=request.user, coupon=coupon)
        user_points.redeemed_points += coupon.points_required
        user_points.save()
        
        # Log transaction
        PointsTransaction.objects.create(
            user=request.user,
            points=coupon.points_required,
            transaction_type='redeemed',
            description=f'Redeemed {coupon.coupon_code}',
            coupon=coupon
        )
        
        # Increment coupon usage
        coupon.current_uses += 1
        coupon.save()
        
        return JsonResponse({
            'success': True,
            'message': f'✓ Coupon {coupon.coupon_code} redeemed successfully!',
            'remaining_points': user_points.available_points
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)


@login_required(login_url='waste:login')
def my_coupons_view(request):
    """Display user's redeemed coupons"""
    user_coupons = UserCoupon.objects.filter(user=request.user).select_related('coupon')
    user_points, _ = UserPoints.objects.get_or_create(user=request.user)
    
    context = {
        'user_coupons': user_coupons,
        'user_points': user_points,
    }
    return render(request, 'waste/my_coupons.html', context)
