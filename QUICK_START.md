# Quick Start Guide - Run Odoo ERP

## Prerequisites Check

Before running, ensure you have:
- ✅ Python 3.8+ installed
- ✅ PostgreSQL 12+ installed and running
- ✅ Odoo 17 downloaded

## Step-by-Step: Run the System

### 1. Install PostgreSQL (if not installed)

**Windows:**
```powershell
# Download from: https://www.postgresql.org/download/windows/
# Run installer and remember your password
```

**Create Database:**
```powershell
# Open Command Prompt as Administrator
psql -U postgres

# In PostgreSQL prompt:
CREATE USER odoo WITH PASSWORD 'odoo';
CREATE DATABASE odoo_erp_ai OWNER odoo;
ALTER USER odoo CREATEDB;
\q
```

### 2. Install Python Dependencies

```powershell
# Navigate to project directory
cd "d:\Jayasurya\My projects\Odoo-ERP"

# Install required packages
pip install -r requirements.txt
```

### 3. Download Odoo 17

**Option A: Using Git**
```powershell
cd d:\Jayasurya\
git clone https://github.com/odoo/odoo.git --depth 1 --branch 17.0 --single-branch
cd odoo
pip install -r requirements.txt
```

**Option B: Download ZIP**
- Go to: https://www.odoo.com/page/download
- Download Odoo 17 Community Edition
- Extract to `d:\Jayasurya\odoo`

### 4. Update Configuration

Edit `odoo.conf` file:
```ini
[options]
# Database settings
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = odoo_erp_ai

# Addons path - UPDATE THIS LINE
addons_path = d:/Jayasurya/odoo/addons,d:/Jayasurya/My projects/Odoo-ERP

# Server settings
http_port = 8069
admin_passwd = admin123
```

### 5. Start Odoo Server

```powershell
# Navigate to Odoo directory
cd d:\Jayasurya\odoo

# Start Odoo with your config file
python odoo-bin -c "d:\Jayasurya\My projects\Odoo-ERP\odoo.conf"
```

**You should see:**
```
INFO ? odoo: Odoo version 17.0
INFO ? odoo: Using configuration file at d:\Jayasurya\My projects\Odoo-ERP\odoo.conf
INFO ? odoo.service.server: HTTP service (werkzeug) running on http://0.0.0.0:8069
```

### 6. Access Web Interface

1. Open your browser
2. Go to: **http://localhost:8069**
3. You'll see the database creation screen

**Create Database:**
- **Master Password**: admin123
- **Database Name**: odoo_erp_ai
- **Email**: admin@example.com
- **Password**: admin
- **Language**: English
- **Country**: India
- Click **Create Database**

### 7. Install Custom Modules

Once logged in:

1. Go to **Apps** menu (top menu bar)
2. Click **Update Apps List** (top-right corner)
3. Search and install these modules one by one:
   - **ERP Inventory Management**
   - **ERP Sales Management**
   - **ERP HR & Payroll**
   - **ERP CRM**
   - **ERP AI Stock Prediction**

### 8. Explore the System

After installation, you'll see new menu items:

**📦 ERP Inventory**
- Products → Create products with stock levels
- Low Stock Alerts → View products needing reorder
- Warehouses → Manage warehouse locations

**💰 ERP Sales**
- Orders → Create quotations and sales orders
- Customers → Manage customer database
- Top Customers → View best customers

**👥 ERP HR**
- Employees → Add employee records
- Attendance → Track employee attendance
- Payroll → Generate payslips

**📊 ERP CRM**
- Leads → Manage sales leads
- Hot Leads → High-priority opportunities
- Pipeline → Visual sales pipeline

**🤖 AI Predictions**
- Stock Predictions → Generate AI forecasts
- Urgent Reorders → Products needing immediate attention

## Quick Demo Workflow

### Test Inventory & AI Prediction

1. **Create a Product:**
   - Go to **ERP Inventory** → **Products** → **Create**
   - Name: "Laptop"
   - Min Stock: 10
   - Max Stock: 100
   - Current Stock: 25
   - Save

2. **Create Sales Orders** (for AI training data):
   - Go to **ERP Sales** → **Orders** → **Quotations** → **Create**
   - Add customer and product
   - Confirm order
   - Repeat 5-10 times with different quantities

3. **Generate AI Prediction:**
   - Go to **AI Predictions** → **Stock Predictions** → **Create**
   - Select product: Laptop
   - Prediction Period: Next Week
   - Method: Hybrid
   - Click **Generate Prediction**
   - View predicted demand and reorder suggestion!

### Test HR & Payroll

1. **Add Employee:**
   - Go to **ERP HR** → **Employees** → **Create**
   - Fill in details, salary information
   - Save

2. **Generate Payslip:**
   - Open employee record
   - Click **Generate Payslip**
   - Review and confirm
   - Print payslip

## Troubleshooting

### Port Already in Use
```powershell
# Change port in odoo.conf
http_port = 8070

# Or find and kill process using port 8069
netstat -ano | findstr :8069
taskkill /PID <process_id> /F
```

### Database Connection Error
```powershell
# Check PostgreSQL is running
# Windows: Services → PostgreSQL
# Or restart it:
net stop postgresql-x64-14
net start postgresql-x64-14
```

### Module Not Found
```powershell
# Verify addons_path in odoo.conf includes:
# d:/Jayasurya/My projects/Odoo-ERP

# Restart Odoo server after changing config
```

### AI Module Error
```powershell
# Install ML libraries
pip install numpy pandas scikit-learn matplotlib scipy

# Restart Odoo
```

## Stopping the Server

Press **Ctrl + C** in the terminal where Odoo is running.

## Next Steps

1. ✅ Configure company information
2. ✅ Import sample data
3. ✅ Create user accounts with different roles
4. ✅ Test all modules
5. ✅ Review AI predictions daily
6. ✅ Set up automated backups

## Support

- Check logs in terminal for errors
- Review `odoo.log` file
- See `USER_MANUAL.md` for detailed usage
- See `INSTALLATION_GUIDE.md` for detailed setup

---

**Ready to go!** 🚀 Your Odoo ERP with AI is now running!
