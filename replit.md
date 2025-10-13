# Pilot App - Airport Map Application

## Overview
This is a Django-based web application that displays an interactive map of airports worldwide using Leaflet.js. Users can view airports on a map with clustering, zoom to see details, and manage their profiles.

## Current State
✅ Successfully configured for Replit environment
✅ Django 5.2.7 running on Python 3.12
✅ Database migrations applied
✅ Development server running on port 5000
✅ Deployment configured with Gunicorn

## Recent Changes
- **2025-10-13**: Initial Replit setup
  - Removed geospatial database dependency (PostGIS) and switched to SQLite
  - Removed django-leaflet package (using Leaflet.js directly from CDN)
  - Configured ALLOWED_HOSTS for Replit proxy
  - Set up development workflow with Django dev server
  - Configured production deployment with Gunicorn
  - Created requirements.txt with all dependencies
  - Added .gitignore for Python/Django projects

## Project Architecture

### Technology Stack
- **Backend**: Django 5.2.7
- **Database**: SQLite (development)
- **Frontend**: HTML/CSS with Leaflet.js for interactive maps
- **Forms**: Django Crispy Forms with Bootstrap 4
- **Authentication**: Django built-in auth system

### Project Structure
```
pilotapp/           # Main Django project settings
├── settings.py     # Application settings
├── urls.py         # URL routing
└── wsgi.py         # WSGI configuration

home/              # Main app - handles map and airports
├── models.py      # Airport model
├── views.py       # Map view and API endpoints
└── templates/     # HTML templates

users/             # User authentication and profiles
├── models.py      # User profile model
├── views.py       # Auth views
├── forms.py       # User forms
└── templates/     # Auth templates

media/             # User uploaded files (profile pics)
db.sqlite3         # SQLite database
airports.csv       # Airport data file
```

### Key Features
1. **Interactive Map**: Leaflet.js map showing airports globally
2. **Marker Clustering**: Airports are clustered based on zoom level
3. **Dynamic Loading**: Airports load based on map bounds and zoom level
4. **User Authentication**: Login, registration, password reset
5. **User Profiles**: Profile management with image upload

## User Preferences
- Uses Django's built-in development server for local development
- Production deployment uses Gunicorn WSGI server
- All static assets (Leaflet, markers) served from CDN

## Environment Variables (Required)
- `SECRET_KEY`: Django secret key (REQUIRED - must be set for security)
- `DEBUG`: Set to `True` for development, `False` for production (defaults to False if not set)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames for production (e.g., `yourdomain.com,www.yourdomain.com`). In development with DEBUG=True, defaults to allow all hosts.

## Optional Environment Variables
- `EMAIL_USER`: Email for password reset functionality
- `EMAIL_PASS`: Email password for SMTP

## Dependencies
See `requirements.txt` for full list:
- Django 5.2.7
- django-crispy-forms (Bootstrap 4)
- Pillow (image handling)
- gunicorn (production server)

## Running the Application
- **Development**: Workflow "Django Server" runs `python manage.py runserver 0.0.0.0:5000`
- **Production**: Configured for autoscale deployment using `gunicorn --bind=0.0.0.0:5000 --reuse-port pilotapp.wsgi:application`
  - Set ALLOWED_HOSTS environment variable with your production domain(s)
  - Ensure DEBUG=False for production

## Known Issues
- **Safari/iPad Login**: Safari on iOS blocks cookies in iframes due to privacy settings. To login on iPad:
  - Click "Open in new tab" to view the app outside the iframe, OR
  - Use Chrome/Firefox instead of Safari, OR
  - Temporarily disable "Prevent Cross-Site Tracking" in Safari settings

## Notes
- The original project used PostGIS for geospatial data, but this has been simplified to use SQLite with latitude/longitude fields
- Leaflet.js is loaded from CDN rather than django-leaflet package
- GDAL dependencies have been removed for Replit compatibility
