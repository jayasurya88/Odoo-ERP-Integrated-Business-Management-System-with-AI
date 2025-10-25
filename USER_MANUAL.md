# Odoo ERP User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Inventory Management](#inventory-management)
3. [Sales Management](#sales-management)
4. [HR & Payroll](#hr--payroll)
5. [CRM](#crm)
6. [AI Stock Prediction](#ai-stock-prediction)
7. [Reports & Analytics](#reports--analytics)

---

## Getting Started

### Login
1. Navigate to `http://localhost:8069`
2. Enter your credentials
3. Select your database

### Dashboard Overview
After login, you'll see the main dashboard with quick access to:
- Inventory status
- Sales orders
- Employee information
- CRM pipeline
- AI predictions

---

## Inventory Management

### Managing Products

#### Create a New Product
1. Go to **ERP Inventory** → **Products** → **Products**
2. Click **Create**
3. Fill in product details:
   - **Name**: Product name
   - **Category**: Select or create category
   - **Product Type**: Storable Product
   - **Sales Price**: Selling price
   - **Cost**: Purchase cost
   - **Barcode**: Scan or enter barcode
   - **Min/Max Stock Levels**: Set reorder thresholds

4. Click **Save**

#### Track Stock Levels
- View current stock: **Inventory** → **Products**
- **Green badge**: In Stock
- **Yellow badge**: Low Stock
- **Red badge**: Out of Stock

#### Low Stock Alerts
1. Go to **ERP Inventory** → **Products** → **Low Stock Alerts**
2. View products below minimum stock level
3. Click **Generate Reorder Suggestion** for recommendations

### Warehouse Management

#### Create Warehouse
1. Go to **ERP Inventory** → **Warehouse** → **Warehouses**
2. Click **Create**
3. Enter warehouse details:
   - Name, address, manager
   - Storage capacity
   - Contact information

#### Manage Locations
1. Go to **ERP Inventory** → **Warehouse** → **Locations**
2. Create locations with:
   - Aisle, Rack, Shelf, Bin numbers
   - Temperature control settings

### Stock Movements

#### Transfer Stock
1. Go to **ERP Inventory** → **Operations** → **Transfers**
2. Click **Create**
3. Select source and destination locations
4. Add products and quantities
5. Validate transfer

---

## Sales Management

### Customer Management

#### Add New Customer
1. Go to **ERP Sales** → **Customers** → **All Customers**
2. Click **Create**
3. Enter customer information:
   - Name, email, phone
   - Address
   - Customer type (Individual/Corporate)
   - Payment preferences
   - Credit limit

#### View Customer Statistics
- Total orders
- Total sales amount
- Average order value
- Last order date

### Creating Sales Orders

#### Create Quotation
1. Go to **ERP Sales** → **Orders** → **Quotations**
2. Click **Create**
3. Select customer
4. Add products:
   - Click **Add a line**
   - Select product
   - Enter quantity
   - Adjust price/discount if needed
5. Set payment method and delivery date
6. Click **Send by Email** or **Confirm**

#### Confirm Order
1. Open quotation
2. Click **Confirm with Stock Check** (checks inventory)
3. Order status changes to **Sales Order**
4. Delivery order is automatically created

#### Track Payment
- **Unpaid**: No payment received
- **Partially Paid**: Some payment received
- **Fully Paid**: Payment complete

### Invoicing
1. Open confirmed sales order
2. Click **Create Invoice**
3. Review invoice details
4. Click **Confirm**
5. Print or email invoice to customer

---

## HR & Payroll

### Employee Management

#### Add New Employee
1. Go to **ERP HR** → **Employees** → **All Employees**
2. Click **Create**
3. Fill in employee information:
   - **Personal**: Name, DOB, blood group, emergency contact
   - **Employment**: Employee code, joining date, department, job position
   - **Salary**: Basic salary, allowances, deductions
   - **Bank Details**: Account number, bank name, IFSC code

#### Employee Status
- **Active**: Currently working
- **On Leave**: Temporarily absent
- **Terminated**: Employment ended
- **Resigned**: Voluntarily left

### Attendance Management

#### Record Attendance
1. Go to **ERP HR** → **Attendance** → **Attendance Records**
2. Click **Create** or use check-in/check-out buttons
3. System automatically calculates:
   - Work hours
   - Overtime
   - Late arrivals

#### Attendance Status
- **Present**: Normal working hours
- **Late**: Arrived after 9 AM
- **Half Day**: Less than 4 hours
- **Overtime**: More than 8 hours

### Leave Management

#### Request Leave
1. Go to **ERP HR** → **Leave Management** → **Leave Requests**
2. Click **Create**
3. Fill in:
   - Leave type (Sick, Casual, Annual)
   - Date from/to
   - Reason for leave
4. Submit for approval

#### Approve/Reject Leave (Manager)
1. Open leave request
2. Review details
3. Click **Approve** or **Refuse**
4. If refusing, provide rejection reason

### Payroll

#### Generate Payslip
1. Go to **ERP HR** → **Payroll** → **Payslips**
2. Click **Create**
3. Select employee and date range
4. System auto-fills salary components
5. Add overtime hours if applicable
6. Add bonus or additional deductions
7. Click **Submit for Verification**

#### Payslip Components
- **Earnings**: Basic salary + Allowances + Overtime + Bonus
- **Deductions**: Tax + Insurance + Other deductions
- **Net Salary**: Gross salary - Total deductions

#### Process Payment
1. Open verified payslip
2. Click **Mark as Paid**
3. Select payment method
4. Print payslip for employee

---

## CRM

### Lead Management

#### Create New Lead
1. Go to **ERP CRM** → **Leads** → **All Leads**
2. Click **Create**
3. Enter lead information:
   - Contact name, email, phone
   - Company details
   - Lead source
   - Expected revenue

#### Lead Scoring
System automatically assigns lead score based on:
- Contact frequency
- Engagement level
- Qualification status

**Lead Quality**:
- **Cold** (0-39): Low priority
- **Warm** (40-69): Medium priority
- **Hot** (70-100): High priority

#### Track Lead Activities
1. Open lead record
2. Click **Log Contact** after each interaction
3. Click **Schedule Follow-up** to set reminder
4. Update lead score and status

#### Convert Lead to Opportunity
1. Open lead
2. Click **Qualify Lead**
3. Lead converts to opportunity
4. Move through sales pipeline stages

### Sales Pipeline

#### Pipeline Stages
1. **New**: Initial contact
2. **Qualified**: Verified interest
3. **Proposition**: Proposal sent
4. **Negotiation**: Discussing terms
5. **Won**: Deal closed
6. **Lost**: Deal lost

#### Manage Opportunities
1. Go to **ERP CRM** → **Opportunities** → **Pipeline**
2. Drag and drop opportunities between stages
3. Update expected revenue and probability
4. Schedule activities and follow-ups

---

## AI Stock Prediction

### Generate Predictions

#### Manual Prediction
1. Go to **AI Predictions** → **Stock Predictions** → **All Predictions**
2. Click **Create**
3. Select product
4. Choose prediction period (Week/Month)
5. Select prediction method:
   - **Moving Average**: Simple average of recent sales
   - **Linear Regression**: Trend-based prediction
   - **Hybrid**: Combination of both (recommended)
6. Click **Generate Prediction**

#### View Results
- **Predicted Demand**: Forecasted sales quantity
- **Confidence Score**: Prediction reliability (0-100%)
- **Reorder Quantity**: Suggested purchase amount
- **Priority**: Urgency level (Low/Medium/High/Urgent)

### Automatic Predictions
System automatically generates predictions daily for all products via scheduled job.

### Reorder Suggestions

#### Review Urgent Reorders
1. Go to **AI Predictions** → **Stock Predictions** → **Urgent Reorders**
2. View products requiring immediate attention
3. Click **Create Purchase Order** to initiate procurement

#### Reorder Priority Levels
- **Low**: Stock sufficient for predicted demand
- **Medium**: Stock below optimal level
- **High**: Stock below minimum level
- **Urgent**: Out of stock or critically low

### Prediction Accuracy

#### Track Accuracy
1. After prediction period ends, enter actual demand
2. System calculates accuracy percentage
3. Use accuracy data to improve future predictions

---

## Reports & Analytics

### Inventory Reports
1. **Inventory Valuation**: Current stock value
2. **Stock Movement Report**: All stock transfers
3. **Low Stock Report**: Products needing reorder

### Sales Reports
1. **Sales Analysis**: Revenue by product, customer, period
2. **Top Customers**: Best performing customers
3. **Sales Dashboard**: Real-time sales metrics

### HR Reports
1. **Employee Performance**: Attendance, productivity
2. **Payroll Summary**: Salary expenses by department
3. **Leave Analysis**: Leave patterns and trends

### CRM Reports
1. **Pipeline Analysis**: Opportunities by stage
2. **Conversion Rate**: Lead to customer conversion
3. **Team Performance**: Sales team statistics

### AI Prediction Reports
1. **Prediction Accuracy**: Historical accuracy trends
2. **Predicted vs Actual**: Comparison charts
3. **Reorder History**: Past reorder recommendations

---

## Tips & Best Practices

### Inventory
- Set realistic min/max stock levels
- Regularly update product costs
- Conduct periodic physical inventory counts
- Use barcode scanning for accuracy

### Sales
- Keep customer information up to date
- Follow up on quotations promptly
- Track payment status regularly
- Offer discounts strategically

### HR
- Record attendance daily
- Process payroll on time
- Maintain accurate employee records
- Approve leave requests promptly

### CRM
- Log all customer interactions
- Update lead scores regularly
- Schedule follow-ups consistently
- Move opportunities through pipeline stages

### AI Predictions
- Review predictions weekly
- Update actual demand for accuracy tracking
- Act on urgent reorder suggestions
- Adjust min/max stock levels based on predictions

---

## Keyboard Shortcuts

- **Ctrl + K**: Quick search
- **Ctrl + S**: Save record
- **Ctrl + Alt + N**: Create new record
- **Esc**: Close dialog

---

## Support & Help

For assistance:
1. Check this manual
2. Contact your system administrator
3. Review error messages in notifications
4. Check system logs for technical issues

---

**Version**: 17.0.1.0.0  
**Last Updated**: 2025-10-25
