# Odoo ERP Installation Guide

## Prerequisites

### 1. System Requirements
- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), or macOS
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 10GB free space
- **Python**: Version 3.8 or higher
- **PostgreSQL**: Version 12 or higher

### 2. Install Python
```bash
# Windows: Download from python.org
# Linux:
sudo apt update
sudo apt install python3 python3-pip python3-dev

# Verify installation
python3 --version
```

### 3. Install PostgreSQL
```bash
# Windows: Download from postgresql.org
# Linux:
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 4. Create PostgreSQL User and Database
```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE USER odoo WITH PASSWORD 'odoo';
CREATE DATABASE odoo_erp_ai OWNER odoo;
ALTER USER odoo CREATEDB;
\q
```

## Installation Steps

### Step 1: Download Odoo 17
```bash
# Clone Odoo repository
git clone https://github.com/odoo/odoo.git --depth 1 --branch 17.0 --single-branch

# Or download from odoo.com
```

### Step 2: Install Python Dependencies
```bash
# Navigate to your project directory
cd "d:/Jayasurya/My projects/Odoo-ERP"

# Install requirements
pip install -r requirements.txt

# Install Odoo dependencies (if using Odoo source)
pip install -r odoo/requirements.txt
```

### Step 3: Configure Odoo
Edit `odoo.conf` file with your settings:
```ini
[options]
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = odoo_erp_ai

addons_path = /path/to/odoo/addons,d:/Jayasurya/My projects/Odoo-ERP

http_port = 8069
admin_passwd = admin123
```

### Step 4: Start Odoo Server
```bash
# If using Odoo source
python3 odoo-bin -c odoo.conf

# Or if Odoo is installed via pip
odoo -c odoo.conf
```

### Step 5: Access Odoo Web Interface
1. Open browser and go to: `http://localhost:8069`
2. Create a new database or select existing one
3. Login with default credentials:
   - **Email**: admin
   - **Password**: admin

### Step 6: Install Custom Modules
1. Go to **Apps** menu
2. Click **Update Apps List**
3. Search and install the following modules:
   - ERP Inventory Management
   - ERP Sales Management
   - ERP HR & Payroll
   - ERP CRM
   - ERP AI Stock Prediction

## Module Configuration

### Inventory Module
1. Go to **ERP Inventory** → **Products** → **Products**
2. Create product categories
3. Add products with:
   - Basic information
   - Stock levels (min/max)
   - Barcode/QR codes
   - Warehouse locations

### Sales Module
1. Go to **ERP Sales** → **Customers**
2. Add customer information
3. Create quotations and sales orders
4. Configure payment methods

### HR Module
1. Go to **ERP HR** → **Employees**
2. Add employee records with:
   - Personal information
   - Employment details
   - Salary information
   - Bank details
3. Configure departments and job positions

### CRM Module
1. Go to **ERP CRM** → **Leads**
2. Create sales pipeline stages
3. Add leads and opportunities
4. Track conversions

### AI Prediction Module
1. Go to **AI Predictions** → **Stock Predictions**
2. Create new prediction for a product
3. Click **Generate Prediction**
4. Review reorder suggestions
5. Enable automatic daily predictions via cron job

## User Management

### Create Users
1. Go to **Settings** → **Users & Companies** → **Users**
2. Create new user
3. Assign appropriate groups:
   - **Inventory Manager**: Full inventory access
   - **Sales Manager**: Full sales access
   - **HR Manager**: Full HR access
   - **CRM Manager**: Full CRM access

### Security Groups
- **Admin**: Full system access
- **Manager**: Department-level access
- **User**: Limited operational access
- **Employee**: Self-service access

## Troubleshooting

### Common Issues

#### 1. Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify credentials in odoo.conf
```

#### 2. Module Installation Fails
```bash
# Update module list
# Check module dependencies
# Review odoo.log for errors
```

#### 3. AI Module Not Working
```bash
# Install required Python packages
pip install numpy pandas scikit-learn matplotlib

# Restart Odoo server
```

#### 4. Port Already in Use
```bash
# Change port in odoo.conf
http_port = 8070

# Or kill process using port 8069
# Windows: netstat -ano | findstr :8069
# Linux: sudo lsof -i :8069
```

## Performance Optimization

### 1. Enable Workers (Production)
```ini
workers = 4
max_cron_threads = 2
```

### 2. Configure Memory Limits
```ini
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
```

### 3. Database Optimization
```sql
-- Regular vacuum
VACUUM ANALYZE;

-- Create indexes for frequently queried fields
```

### 4. Enable Caching
```ini
# Add to odoo.conf
db_maxconn = 64
```

## Backup and Restore

### Backup Database
```bash
# Using pg_dump
pg_dump -U odoo -h localhost odoo_erp_ai > backup.sql

# Or use Odoo web interface
# Settings → Database Manager → Backup
```

### Restore Database
```bash
# Using psql
psql -U odoo -h localhost odoo_erp_ai < backup.sql

# Or use Odoo web interface
# Settings → Database Manager → Restore
```

## Production Deployment

### 1. Use NGINX as Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Enable SSL/HTTPS
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### 3. Run as System Service
Create `/etc/systemd/system/odoo.service`:
```ini
[Unit]
Description=Odoo ERP
After=network.target postgresql.service

[Service]
Type=simple
User=odoo
ExecStart=/usr/bin/python3 /path/to/odoo-bin -c /path/to/odoo.conf

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable odoo
sudo systemctl start odoo
```

## Support

For issues or questions:
- Check `odoo.log` for error messages
- Review module documentation
- Consult Odoo community forums
- Contact system administrator

## Next Steps

1. Configure company information
2. Import initial data (products, customers, employees)
3. Set up workflows and automations
4. Train users on system usage
5. Monitor AI predictions and adjust parameters
6. Regular backups and maintenance

---

**Version**: 17.0.1.0.0  
**Last Updated**: 2025-10-25
