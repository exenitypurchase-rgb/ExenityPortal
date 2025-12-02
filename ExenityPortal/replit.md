# EXENITY Purchase Request Portal

## Overview

A production-ready, single-page Purchase Request (PR) web portal for EXENITY Systems. The application streamlines the procurement process by allowing employees to submit purchase requests and administrators to manage approvals.

**Project Type**: Single-page web application  
**Primary Purpose**: Facilitate purchase request submission and management  
**Last Updated**: November 30, 2025

## User Preferences

**Preferred communication style**: Simple, everyday language.

## Features

### Employee Features
- Submit new purchase requests via modal form with estimated cost
- View all submitted PRs in a data table
- See real-time dashboard metrics (Total PRs, Pending PRs, Approved PRs)
- No login required for regular employees
- Data automatically syncs across all computers

### Admin Features
- Secure login with password authentication
- View Comments column (hidden from regular users)
- View and edit Actual Cost for each PR (overrides estimated cost in reports)
- Approve or Reject pending purchase requests
- Update PR status through workflow: Pending → Approved → In Process → Material Received
- Generate BOM Missing Report with cost analysis based on actual costs
- Generate Expenditure Report by department and status using actual costs
- Download reports as CSV files
- Admin session persists until browser is closed

### Technical Features
- Data persistence via localStorage (survives page refresh)
- Admin session via sessionStorage (resets on browser close)
- Auto-incrementing PR IDs (PR-001, PR-002, etc.)
- Color-coded priority badges (High/Medium/Low)
- Status badges (Pending/Approved/Rejected)
- Responsive design for desktop and mobile
- XSS protection via HTML escaping

## System Architecture

### Technology Stack
- **Frontend**: Vanilla HTML, CSS, and JavaScript (single-page application)
- **Backend**: Python Flask with CORS support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Data Sync**: Real-time API-based synchronization (3-second auto-refresh)

### Frontend Architecture

**File Structure**:
- `index.html` - Single file containing all HTML, CSS, and JavaScript
- `app.py` - Flask backend server with REST API endpoints

**Design Approach**:
- Single HTML file structure with embedded styles and scripts
- Responsive design using CSS Flexbox and Grid
- Custom CSS with gradient-based visual design
- Sticky header navigation for improved UX
- Modal dialogs for forms and login

**UI Components**:
- Header with gradient background (linear-gradient from #1a5fb4 to #0d3b7a)
- Navigation buttons: Home, New PR, Admin Login/Logout
- Dashboard cards with metric counters
- Data table with sortable columns
- Modal forms with validation

**Styling Strategy**:
- CSS-in-HTML approach for simplicity
- Universal box-sizing for consistent layout
- Shadow effects for depth and visual hierarchy
- Color scheme: Blue gradient primary, light gray background (#f5f7fa)
- Font family: Segoe UI

### Data Storage

**PostgreSQL Database**: Centralized storage for all purchase request data
- Table: `purchase_requests`
- Accessible from all computers via the Flask backend
- Auto-refresh every 3 seconds keeps all connected users synchronized

**sessionStorage**: Stores admin login state (browser session only)
- Key: `exenity_admin_session`
- Value: 'true' when admin is logged in
- Resets when browser is closed

### Authentication

**Admin Password**: `Exenity@123` (hard-coded)
- Login via Admin Login button in navigation
- Session stored in sessionStorage
- Auto-logout when browser is closed

## PR Data Structure

Each purchase request contains:
- `id`: Auto-generated PR ID (PR-001 format)
- `requester`: Employee name
- `department`: Department (Production, Control, Manufacturing, Design, etc.)
- `project`: Project name
- `item`: Item being requested
- `specification`: Detailed specifications
- `purchaseType`: Missing in BOM or Regular Purchase
- `estimatedCost`: Estimated cost in INR (entered by requester)
- `actualCost`: Actual cost in INR (entered by admin, used for reporting)
- `priority`: High, Medium, or Low
- `status`: Pending, Approved, In Process, Material Received, or Rejected
- `comments`: Optional comments (visible only to admin)
- `createdAt`: ISO timestamp
- `updatedAt`: Last modification timestamp

## Running the Application

The application runs on a Flask backend server:
```
python app.py
```

Server runs on `http://0.0.0.0:5000` and serves:
- Frontend HTML/CSS/JS at `/`
- REST API endpoints at `/api/*`

**Key API Endpoints**:
- `GET /api/prs` - Fetch all purchase requests
- `POST /api/prs` - Create new PR
- `PATCH /api/prs/{pr_id}/status` - Update PR status
- `PATCH /api/prs/{pr_id}/actual-cost` - Update actual cost (admin)
- `GET /api/reports/bom-missing` - Get BOM missing items report
- `GET /api/reports/expenditure` - Get expenditure report

## External Dependencies

**Backend**:
- Flask 3.1.2 - Web framework
- Flask-CORS 6.0.1 - Cross-origin support
- SQLAlchemy 2.0.44 - ORM
- psycopg2-binary 2.9.11 - PostgreSQL driver

**Frontend**:
- Browser-native technologies only:
  - HTML5
  - CSS3
  - Vanilla JavaScript
  - Fetch API for HTTP requests

## Recent Changes (November 30, 2025)

**Upgraded from localStorage to PostgreSQL Database**:
- Migrated from device-specific localStorage to centralized PostgreSQL database
- All PRs now visible across all computers in real-time
- 3-second auto-refresh keeps all users synchronized
- Added Flask backend API server for secure data handling
- Implemented admin API authentication

**Added Actual Cost Tracking**:
- Admins can now set actual cost for each PR (separate from estimated cost)
- Reports automatically use actual cost when available, falls back to estimated cost
- Cost calculations are accurate for financial planning and auditing

## Future Enhancements

Potential additions for future development:
- Advanced search and filter functionality
- Email notifications on PR status changes
- Printable PR detail view with QR codes
- User roles and department-level permissions
- PR workflow history and audit trail
- Mobile app version
- Integration with accounting software
