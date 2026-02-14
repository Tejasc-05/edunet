# 📖 User Guide - Eco Waste Management System

## Table of Contents
1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [Dashboard](#dashboard)
4. [Recording Waste](#recording-waste)
5. [Viewing Categories](#viewing-categories)
6. [Statistics & Reports](#statistics--reports)
7. [Account Management](#account-management)
8. [FAQ](#faq)

---

## Getting Started

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection
- No additional software needed

### Accessing the Application
1. Open your web browser
2. Visit: `http://127.0.0.1:8000/`
3. You'll see the login page

---

## Authentication

### Creating a New Account (Sign Up)

**Step-by-step:**

1. Click **"Sign up here!"** link on the login page
2. Fill in the registration form:
   - **Full Name**: Enter your complete name
   - **Email**: Enter a valid email address
   - **Password**: Create a strong password (minimum 6 characters)
   - **Confirm Password**: Re-enter your password
3. Click **"CREATE ACCOUNT"** button
4. You'll be automatically logged in and directed to the dashboard

**Password Requirements:**
- Minimum 6 characters
- Mix of letters and numbers recommended
- Avoid common passwords

**Email:**
- Must be unique (not used by another account)
- Used for login
- Should be a valid email address

### Logging In

**Step-by-step:**

1. On the login page, enter:
   - **Email**: Your registered email address
   - **Password**: Your account password
2. Click **"LOGIN"** button
3. If credentials are correct, you'll access the dashboard

**Forgot Password?**
- Currently not available
- Contact system administrator
- Or use Django admin to reset

### Logging Out

1. Click **"Logout"** button in the top navigation
2. You'll be redirected to the login page
3. Your session will end

---

## Dashboard

### Dashboard Overview

The dashboard is your main hub. It shows:

**Welcome Section**
- Greeting with your name
- Current date and time
- Your location

**Statistics Cards**
- **Total Waste**: Total kg of waste recorded
- **Reports**: Number of reports submitted

**Waste Categories Grid**
- Six waste type cards
- Each shows category name and description
- Click to view detailed information

**Record New Waste Section**
- Form to log new waste
- Quick and easy recording

---

## Recording Waste

### Adding a Waste Record

**Form Fields:**

1. **Category** (Required)
   - Dropdown menu
   - Options: Biodegradable, Plastic, E-Waste, Metal, Glass, Hazardous
   - Click to select

2. **Quantity** (Required)
   - Enter amount in kilograms (kg)
   - Decimals allowed (e.g., 2.5 kg)
   - Examples: 10, 5.25, 100.5

3. **Location** (Optional)
   - Pre-filled with "Bangalore, India"
   - Can be changed
   - Examples: "Your Home", "Office", "College"

4. **Notes** (Optional)
   - Additional information
   - Examples: "Plastic bags from shopping", "Old electronic equipment"
   - Helps with tracking and management

### Submitting a Waste Record

1. Fill in all required fields
2. Optionally add location and notes
3. Click **"Record Waste"** button
4. You'll see a confirmation message
5. The record is saved to your account

**Tips:**
- Record waste as soon as you dispose of it
- Be accurate with quantities
- Use descriptive notes for future reference
- Track multiple items separately if needed

---

## Viewing Categories

### Accessing Category Details

**Method 1: From Dashboard**
- Click on any waste category card
- You'll see detailed information about that waste type

**Method 2: From Navigation Menu**
- Click category name in top navigation bar
- Biodegradable, Plastic, E-Waste, Metal, Glass, Hazardous

### Category Details Page

Each category shows:

**Category Header**
- Waste type icon
- Category name
- Brief description

**Detailed Information**
- **Treatment Method**: How this waste is processed
- **Environmental Impact**: Effects on environment and benefits of recycling

**Your Statistics for This Category**
- Total waste recorded (in kg)
- Number of reports submitted

**Your Reports Table**
- Date of report
- Quantity recorded
- Location
- Notes added
- List of your recent reports for this category

---

## Statistics & Reports

### Viewing All Reports

1. Click **"Reports"** in the navigation menu
2. See all your waste records
3. Organized by date (newest first)
4. Shows all categories mixed

### Statistics View

The dashboard automatically shows:
- **Total Waste Recorded**: Sum of all waste
- **Total Reports**: Number of entries
- **Per Category Breakdown**: Available in admin panel

### Understanding Statistics

**Total Waste**: 
- All amounts in kilograms
- Across all categories
- Since account creation

**Report Count**:
- Number of individual entries
- Regardless of quantity

**Category-wise**:
- Go to category page
- View waste specific to that type

---

## Account Management

### Viewing Your Profile

1. Go to Dashboard
2. Your name appears in welcome section
3. Your location is displayed

### Changing Your Information

**Current Available**:
- Name (through admin panel)
- Location (per waste record)

**To Update**:
- Contact administrator
- Use Django admin panel
- Email information for admin to update

### Password Management

**To Change Password**:
1. Go to Django admin panel
2. Use "Change password" feature
3. Or contact administrator

**If Forgotten**:
- Ask system administrator
- They can reset your password

### Deleting Your Account

**To Delete Account**:
1. Contact system administrator
2. They can delete your account
3. All your records will be permanently deleted

⚠️ **Warning**: Account deletion is permanent!

---

## Navigation Menu

### Top Navigation Bar

| Icon | Link | Purpose |
|------|------|---------|
| 🏠 | Home | Go to dashboard |
| 🍃 | Biodegradable | View biodegradable waste details |
| 🍾 | Plastic | View plastic waste details |
| 💻 | E-Waste | View electronics waste details |
| ⚙️ | Metal | View metal waste details |
| 🥃 | Glass | View glass waste details |
| ☠️ | Hazardous | View hazardous waste details |
| 🚪 | Logout | Exit your account |

---

## Waste Categories Explained

### 1. Biodegradable Waste 🍃
**What's included:**
- Food waste and scraps
- Leaves and plant material
- Paper and cardboard
- Wood products
- Garden waste

**Treatment**: Composting and recycling
**Impact**: Can be converted to nutrient-rich soil

### 2. Plastic Waste 🍾
**What's included:**
- Plastic bags
- Bottles and containers
- Packaging materials
- Plastic films
- Single-use plastics

**Treatment**: Recycling and processing
**Impact**: Persistent in environment; recycling saves fossil fuels

### 3. E-Waste 💻
**What's included:**
- Old phones and tablets
- Computers and laptops
- TVs and monitors
- Cables and chargers
- Electronic appliances

**Treatment**: Specialized e-waste recycling facilities
**Impact**: Prevents toxic contamination; recovers valuable metals

### 4. Metal Waste ⚙️
**What's included:**
- Aluminum and steel
- Copper and brass
- Iron and tin
- Metal scraps
- Metal household items

**Treatment**: Smelting and reformation
**Impact**: Highly recyclable; saves mining resources

### 5. Glass Waste 🥃
**What's included:**
- Glass bottles and jars
- Window glass
- Drinking glasses
- Glass containers
- Glass waste

**Treatment**: Melting and reformation
**Impact**: Infinitely recyclable without quality loss

### 6. Hazardous Waste ☠️
**What's included:**
- Chemical waste
- Batteries
- Medical waste
- Pesticides
- Toxic materials

**Treatment**: Special secure disposal
**Impact**: Requires careful handling to prevent contamination

---

## Tips & Best Practices

### Recording Waste Effectively

✅ **Do's:**
- Record waste promptly after disposal
- Be accurate with quantities
- Categorize correctly
- Add descriptive notes
- Track regularly

❌ **Don'ts:**
- Don't mix different waste types in one entry
- Don't guess quantities significantly
- Don't forget to specify location
- Don't ignore hazardous waste reporting

### Reducing Waste

1. **Reduce**: Buy less, choose quality over quantity
2. **Reuse**: Use items multiple times
3. **Recycle**: Follow proper recycling guidelines
4. **Compost**: Turn organic waste to soil

### Environmental Impact

Your tracking helps:
- Monitor personal waste generation
- Identify reduction opportunities
- Support sustainable practices
- Contribute to environmental data

---

## FAQ

### Q: Is my data safe?
**A:** Yes! Your data is stored securely in the database. Only you can view your records.

### Q: Can I edit or delete a record?
**A:** Currently, you can't edit or delete your own records. Contact administrator if needed.

### Q: How accurate should quantities be?
**A:** Be as accurate as possible, but estimates are acceptable.

### Q: Can multiple people share an account?
**A:** Not recommended. Each person should have their own account.

### Q: Is there a mobile app?
**A:** Currently, it's web-based. Mobile version coming soon!

### Q: How often should I record waste?
**A:** Record it as often as you dispose of waste. Daily is ideal.

### Q: Can I see statistics for multiple categories?
**A:** Go to each category page to see category-specific stats.

### Q: What if I forget my password?
**A:** Contact the system administrator. They can reset it for you.

### Q: Can I bulk upload data?
**A:** Currently not available. Use the form to add records.

### Q: Is there an API?
**A:** Not yet. It may be available in future versions.

### Q: How long is data retained?
**A:** Data is kept indefinitely unless you delete your account.

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Alt + L | Go to Login |
| Alt + D | Go to Dashboard |
| Tab | Navigate form fields |
| Enter | Submit form |

---

## Accessibility

**Features for accessibility:**
- Keyboard navigation support
- Color contrast for readability
- Clear form labels
- Semantic HTML structure

**Using with screen readers:**
- Compatible with NVDA and JAWS
- All images have descriptions
- Form fields are properly labeled

---

## Getting Help

### For Technical Issues:
1. Try refreshing the page
2. Clear browser cache
3. Try a different browser
4. Contact administrator

### For Account Issues:
- Email administrator
- Provide your account email
- Describe the issue

### For Data Issues:
- Check your entries in category pages
- Contact administrator if needed

---

## Legal & Privacy

- Your personal data is protected
- Only you can see your records
- Admin can view all data
- No data is shared with third parties
- Compliance with data protection laws

---

**Thank you for using Eco Waste Management! Together we create a cleaner India! 🌍♻️**

For more information, contact your system administrator.
