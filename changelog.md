# Changelog

All notable changes to the Daiva Anughara website project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Excel Report Generation**: Implemented functionality to generate and download an Excel report of user data.
  - Includes basic user details: username, email, join date, approval date, Mandala access.
  - Calculates "Days on Mandala" for each Mandala level.
  - Provides key performance indicators (KPIs) such as total users, approved users, pending users, suspended users, and average days to approval.
  - Generates a user status distribution chart and Mandala access distribution chart within the Excel file.
  - Added `openpyxl` to `requirements.txt`.
  - Created `/admin/users/report` endpoint for downloading the report.

### Enhanced
- **Admin User Management UI/UX**: Significantly improved the user interface and experience of the `/auth/admin/users` page.
  - **Redesigned User Table**: Replaced the traditional table with a modern, responsive card-based layout for better scannability and visual appeal.
  - **Live Search & Filtering**: Implemented real-time search and filtering by username, email, status, and role without page reloads.
  - **Integrated Actions**: Moved user action buttons (approve, reject, suspend, reactivate) directly into each user card's dropdown menu.
  - **Confirmation Modals**: Added confirmation modals for critical user actions to prevent accidental changes.
  - **KPIs and Charts Dashboard**: Integrated a dashboard displaying key performance indicators and interactive charts (user status distribution, Mandala access distribution) for better user analysis.
  - **Mandala Access Visuals**: Enhanced the Mandala access display on the user detail page with more intuitive and visually appealing components (icons, toggles).
  - **Consistent Styling**: Ensured all new and modified elements adhere to the established UI style guide for a cohesive look and feel.

### Fixed
- **Admin User Action Buttons**: Resolved the issue where action buttons (approve, reject, suspend, reactivate) on the user detail page were not functioning.
  - Ensured correct JavaScript event handling for these buttons.
  - Verified proper data attribute passing for user IDs and actions.
  - Confirmed API calls are correctly triggered upon button clicks.


### Added
- **Main Navigation Enhancement**: Added "Padati for You" tab to the main header navigation
  - Added prominent navigation link in the desktop header menu
  - Positioned between "About" and "Admin" sections for optimal visibility
  - Maintains consistent styling with other navigation items
  - Enhances user accessibility to the Padati features
- **Complete Authentication System**: Implemented comprehensive user authentication with admin and user roles
  - **User Registration**: Professional registration form with spiritual practice fields
    - Username, email, password with confirmation
    - Full name, phone number, spiritual name, guru name, practice level
    - Form validation with error handling
    - Admin approval required before login access
  - **User Login**: Secure login system with remember me functionality
    - Username/password authentication
    - Account status validation (pending approval, suspended, etc.)
    - Flash message notifications for different states
  - **Admin Panel**: Complete user management system
    - User search and filtering by status and role
    - Quick approval/rejection/suspension actions
    - User detail views and management
    - Professional admin interface with responsive design
  - **Database Integration**: SQLAlchemy models with User table
    - User roles (admin/user) with proper permissions
    - Account approval workflow
    - Spiritual practice information storage
  - **Security Features**: CSRF protection, password hashing, session management
  - **Navigation Updates**: Added authentication links to header and mobile menu
    - Login/Register buttons for guests
    - User profile dropdown for authenticated users
    - Admin navigation for administrators
  - **Professional UI**: Modern authentication forms and admin interface
    - Consistent with website design theme
    - Responsive design for all devices
    - Professional styling and animations

### Enhanced
- **Color Scheme Reversal**: Restored original green color palette from red/fire theme
  - **Primary Colors**: Restored Army Green (#637457) from Dark Red (#8B0000)
  - **Secondary Colors**: Restored Light Green (#8BBB67) from Crimson Red (#DC143C)
  - **Accent Colors**: Restored Cream (#FCFBDF) from Dark Orange (#FF8C00)
  - **Restored Elements**: Hero sections, buttons, headings, icons, cards, borders, and shadows
  - **Original Theme**: Back to the original peaceful, spiritual green appearance
  - **Complete Restoration**: All color references reverted throughout the entire CSS
- **Website Spacing Optimization**: Reduced excessive white space while maintaining professional appearance
  - Reduced CSS spacing variables: xs (0.25rem), sm (0.5rem), md (1rem), lg (1.5rem), xl (2rem), xxl (2.5rem)
  - Optimized main content padding from large to medium spacing
  - Reduced hero section padding for better content density
  - Minimized section headers, cards, and component spacing
  - Maintained visual hierarchy while reducing unnecessary white space
  - Improved content density and professional appearance
- **Home Page Professional Design**: Completely transformed home.html from basic to professional modern design
  - Added stunning hero section with "HIS GRACE" title and gradient background
  - Implemented professional card-based layout with shadows and hover effects
  - Added visual icons and emojis throughout for better engagement
  - Enhanced typography with better hierarchy and spacing
  - Added interactive elements: hover animations, floating animations, and smooth transitions
  - Implemented responsive grid layouts for better content organization
  - Added professional color schemes and visual separators
  - Enhanced sacred messages with decorative elements and better styling
  - Added journey steps with professional card designs
  - Implemented progression info cards with visual hierarchy
  - Added Sadhana Paddhati section with numbered step cards
  - Enhanced caution section with warning styling and visual emphasis
  - Added Rudraksha section with bead information cards
  - Enhanced countdown timer with professional card design
  - Added sacred notice section with icon-based items
  - Enhanced Seva section with professional layout
  - Added external links section with hover effects
  - Enhanced mobile responsiveness with better breakpoints
  - Added CSS animations: float, fadeInUp, pulse, and hover effects

- **Devi Page Professional Design**: Completely transformed devi.html from basic to professional modern design
  - Added stunning hero section with gradient background and animated elements
  - Implemented professional card-based layout with shadows and hover effects
  - Added visual icons and emojis throughout for better engagement
  - Enhanced typography with better hierarchy and spacing
  - Added interactive elements: hover animations, floating animations, and smooth transitions
  - Implemented responsive grid layouts for better content organization
  - Added professional color schemes and visual separators
  - Enhanced sacred quotes with decorative elements and better styling
  - Added power points sidebar with animated statistics
  - Implemented modern card designs for all sections (Navratri, Guidelines, Mantras, etc.)
  - Added professional contact section with call-to-action button
  - Enhanced mobile responsiveness with better breakpoints
  - Added CSS animations: float, fadeInUp, pulse, bounce, and sparkle effects

### Changed
- **Devi Page Complete Recreation**: Completely rebuilt devi.html using content from devi.txt
  - Replaced generic content with authentic Kamakya Maa Sadhana information
  - Added comprehensive sections: Sacred Introduction, Kamakya Maa, Tantra & Yoni Peetha, Sadhana Introduction, Navratri Information, Ganapati Invocation, Guidelines, Why Kamakhya Sadhana, One Step Closer, Next Steps, and Contact
  - Included authentic Sanskrit mantras and transliterations
  - Added detailed Navratri periods and their significance
  - Included complete Sadhana guidelines and eligibility criteria
  - Added sacred quotes and spiritual teachings from the original text
  - Maintained professional structure while preserving sacred spiritual content

### Removed
- **Search Popup/Modal**: Removed search functionality and popup modal from the landing screen
  - Removed search bar from header navigation
  - Removed search results modal from base template
  - Removed search.js script reference
  - Eliminated popup that was appearing on the landing screen

### Fixed
- **Missing Admin Template**: Created admin/user_detail.html template for viewing individual user details
  - Added comprehensive user information display (basic info, account status, spiritual practice, timestamps)
  - Implemented quick action buttons for user management (approve, reject, suspend, reactivate)
  - Added professional styling with responsive grid layout
  - Integrated with existing user management system
- **Missing Profile Template**: Created auth/profile.html template for user profile viewing
  - Added user profile display with basic info, spiritual practice, and account status
  - Implemented responsive grid layout for profile information
  - Added navigation buttons for home and logout
  - Consistent styling with authentication system theme
- **Template Rendering Issues**: Fixed page_title variable not being passed to templates
  - Added page_title parameter to all auth route template renders
  - Fixed breadcrumb template to handle undefined page_title gracefully
  - Resolved template rendering errors in authentication pages
- **Countdown API Integration**: Fixed countdown timer API calls and error handling
  - Updated countdown.js to properly fetch next Ashtami date first
  - Added proper error handling for API responses
  - Improved countdown display fallback when API fails
- **Import Error Fix**: Fixed `url_parse` import error by replacing deprecated Werkzeug import with modern `urllib.parse.urlparse`
  - Updated auth.py to use `urllib.parse.urlparse` instead of `werkzeug.urls.url_parse`
  - Resolves compatibility issue with newer versions of Werkzeug
  - Ensures authentication system works properly with current package versions

### Fixed & Completed
- **Homepage Issues Resolved**: Fixed structural problems and completed professional redesign
  - **Fixed CSS Class Mismatches**: Aligned HTML structure with existing CSS classes
  - **Completed Quick Access Section**: Added missing CSS for professional navigation cards
  - **Enhanced Button Styles**: Improved button design with hover effects and icons
  - **Professional Layout**: Implemented proper grid systems and responsive design
  - **Visual Consistency**: Ensured all sections use consistent styling and spacing
  - **Mobile Optimization**: Enhanced responsive design for all device sizes
  - **Professional Appearance**: Homepage now displays with full professional styling

- **Responsive Design Issues Fixed**: Resolved all responsive design problems
  - **Hero Section Responsive**: Fixed grid layout issues and made fully responsive
  - **Mobile Layout**: Improved mobile experience with proper stacking and sizing
  - **Tablet Optimization**: Enhanced tablet view with appropriate breakpoints
  - **Touch-Friendly Elements**: Optimized button sizes and spacing for mobile
  - **Flexible Grids**: Made all grid layouts responsive with auto-fit columns
  - **Typography Scaling**: Proper font size scaling across all device sizes
  - **Spacing Adjustments**: Responsive padding and margins for all screen sizes

- **User Registration Enhanced**: Added purpose field for sadhana motivation
  - **Purpose Field**: Added required textarea for users to explain why they want to start sadhana
  - **Admin Review**: Admins can now see user's purpose before approval
  - **Purpose Preview**: Added purpose preview column in admin users table
  - **Full Purpose View**: Modal popup to read complete purpose text
  - **Form Validation**: Purpose field requires 20-1000 characters with helpful guidance
  - **Database Update**: Added purpose field to User model
  - **Admin Interface**: Enhanced user detail page to display full purpose

### Fixed
- **CSRF Token Error**: Fixed Jinja2 template error with csrf_token() function
  - Added Flask-WTF CSRF protection configuration to main app
  - Imported CSRFProtect and generate_csrf from flask_wtf.csrf
  - Initialized CSRF protection with app instance
  - Added context processor to inject CSRF token into all templates
  - Updated Flask-WTF to version 1.2.1 for Flask 3.0 compatibility
  - Resolves template rendering error in admin user detail page
- **Database Schema Error**: Fixed NOT NULL constraint violation when creating admin user
  - Added purpose field value to admin user creation in create_admin_user() function
  - Resolved sqlalchemy.exc.IntegrityError for missing purpose value
  - Admin user now created successfully with proper purpose description

### Added
- **New "Padati for You" Tab**: Implemented comprehensive mandala access system
  - **Three Internal Tabs**: Mandala 1 (Foundation), Mandala 2 (Advancement), Mandala 3 (Mastery)
  - **Access Control System**: Users start with Mandala 1 access, admin approval required for higher levels
  - **Professional UI**: Tabbed interface with access badges, progress indicators, and status displays
  - **Admin Management**: New admin interface for managing user mandala access permissions
  - **Database Integration**: Added mandala access fields to User model (mandala_1_access, mandala_2_access, mandala_3_access)
  - **Navigation Updates**: Added "Padati for You" link to main navigation and mobile menu
  - **Responsive Design**: Fully responsive design with mobile-optimized tab navigation
  - **Access Information**: Clear display of current access status and requirements for each mandala
  - **Features Coming Soon**: Placeholder content with progress indicators for future implementation

### Added
- Initial project setup and structure
- Complete Flask application with all required routes and API endpoints
- Comprehensive HTML templates for all pages (Home, Documents & Updates, Ashtami, Devi, About)
- Custom error pages (404, 500)
- Complete CSS styling with Army Green color scheme (#637457, #8BBB67, #FCFBDF)
- Responsive design for all screen sizes
- JavaScript functionality for mobile menu, dropdowns, search, and countdown timers
- Accessibility features (skip links, ARIA attributes, keyboard navigation)
- Search functionality with modal and API integration
- Real-time Ashtami countdown timer
- Project documentation (README.md)
- Python dependencies (requirements.txt)
- Git configuration (.gitignore)
- Changelog tracking system

### Cleaned Up
- **Removed Redundant Information**: Streamlined all pages to eliminate duplicate content and improve user experience
  - **Home Page**: Removed Sadhana Paddhati details, caution sections, Rudraksha information, sacred notices, and seva sections
  - **Documents Page**: Removed duplicate seva information and document viewer instructions
  - **Devi Page**: Removed redundant why-sadhana sections, contact information, and excessive practice details
  - **Added Quick Navigation**: Implemented clean quick links section on home page for better navigation
  - **Consolidated Content**: Each page now focuses on its unique purpose without wading through repetitive information
  - **Improved Focus**: Users can now find specific information without wading through duplicate content

### Technical Details
- **Backend**: Flask 2.3.3 with Jinja2 templating
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with CSS variables and responsive design
- **Features**: Mobile-responsive navigation, search system, countdown timers
- **Accessibility**: WCAG compliant with skip links and keyboard navigation
- **Performance**: Optimized CSS and JavaScript with proper loading

### Files Created
- `app.py` - Main Flask application
- `templates/base.html` - Base template with navigation and structure
- `templates/home.html` - Home page with hero section and countdown
- `templates/documents.html` - Documents & Updates page
- `templates/ashtami.html` - Ashtami Sadhana page
- `templates/devi.html` - Devi information page
- `templates/about.html` - About page
- `templates/404.html` - Custom 404 error page
- `templates/500.html` - Custom 500 error page
- `static/css/style.css` - Complete stylesheet
- `static/js/main.js` - Core JavaScript functionality
- `static/js/search.js` - Search functionality
- `static/js/countdown.js` - Countdown timer functionality
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation
- `.gitignore` - Git ignore rules
- `changelog.md` - This changelog file

### Initial Features
- Sacred spiritual website design with Army Green theme
- Complete navigation structure (Home, Documents & Updates, Ashtami, Devi, About)
- Sacred message sections and spiritual content
- Document embedding capabilities for PDF files
- External link integration
- Responsive design for all devices
- Search functionality across all content
- Real-time Ashtami countdown timer
- Mobile-friendly navigation and interactions
- Accessibility compliance
- Error handling and custom error pages

## [Latest] - Devi Page Consistency Improvements

### 🎯 **Devi Page Design Consistency**
- **Unified Visual Design**: Updated Devi page to match the overall website design language
- **Consistent Spacing**: Applied the same spacing variables and layout density as other pages
- **Enhanced Color Scheme**: Updated to use the refined color palette for better visual hierarchy
- **Professional Typography**: Applied consistent font sizes and spacing using rem units

### 🎨 **Specific Devi Page Enhancements**
- **Hero Section**: Reduced height to 50vh for better content density, enhanced gradient background
- **Section Headers**: Added decorative underlines with gradient colors for visual appeal
- **Card Design**: Consistent card styling with enhanced shadows and hover effects
- **Interactive Elements**: Improved hover states and transitions for better user experience

### 📱 **Mobile Responsiveness**
- **Enhanced Mobile Layout**: Optimized Devi page for mobile devices with responsive grids
- **Touch-Friendly Design**: Improved spacing and sizing for mobile navigation
- **Responsive Typography**: Adjusted font sizes across all breakpoints for better readability
- **Mobile-First Approach**: Ensured all Devi page elements work seamlessly on small screens

### 🔧 **Technical Improvements**
- **CSS Consistency**: Applied the same design patterns and variables used throughout the site
- **Spacing Optimization**: Reduced excessive white space while maintaining professionalism
- **Visual Hierarchy**: Enhanced section separation and content flow
- **Performance**: Optimized animations and transitions for better mobile performance

## [Previous] - Comprehensive Visual Design & Layout Improvements

### 🎨 Overall Visual Design and Layout
- **Enhanced Color Scheme**: Refined primary green (#4A5D3F) for better contrast and visual hierarchy
- **Improved Visual Hierarchy**: Added subtle shadows, enhanced borders, and better color contrast
- **Professional Typography**: Optimized font sizes using rem units for better scalability
- **Enhanced Card Design**: Added depth with improved shadows and hover effects
- **Section Headers**: Added decorative underlines with gradient colors for visual appeal

### 📱 Mobile Responsiveness Enhancements
- **Improved Mobile Navigation**: Better spacing and touch targets for mobile devices
- **Responsive Typography**: Optimized font sizes across all breakpoints
- **Enhanced Mobile Layout**: Better grid layouts and spacing for small screens
- **Touch-Friendly Elements**: Improved button sizes and navigation for mobile users
- **Flexible Grids**: Made all grid layouts responsive with auto-fit columns
- **Typography Scaling**: Proper font size scaling across all device sizes
- **Spacing Adjustments**: Responsive padding and margins for all screen sizes

### 🎯 Specific Improvements
- **Header**: Enhanced with better shadows and border styling
- **Navigation**: Improved hover effects with subtle animations and better visual feedback
- **Hero Section**: Enhanced gradient background with inset shadows
- **Buttons**: Added depth with shadows and improved hover states
- **Feature Cards**: Enhanced with better shadows and hover animations
- **Footer**: Added gradient background and improved visual appeal
- **Section Titles**: Added decorative underlines for better visual hierarchy

### 🔧 Technical Enhancements
- **CSS Variables**: Enhanced color palette with additional variables for better consistency
- **Border Radius**: Optimized for modern design (6px, 10px)
- **Shadows**: Improved shadow system for better depth perception
- **Transitions**: Maintained smooth animations while optimizing performance

## [Latest] - App-Like Experience & PWA Implementation

### 🚀 **Progressive Web App (PWA) Features**
- **Service Worker**: Implemented comprehensive service worker for offline functionality
- **PWA Manifest**: Created manifest.json with app metadata, icons, and shortcuts
- **Install Prompt**: Added "Install App" button for mobile app installation
- **Offline Support**: Cached static files and pages for offline access
- **App Icons**: Added multiple icon sizes for different devices and platforms

### 📱 **Native App-Like Behavior**
- **Pull-to-Refresh**: Implemented pull-to-refresh functionality for mobile users
- **Swipe Navigation**: Added left/right swipe gestures for page navigation
- **Haptic Feedback**: Integrated vibration feedback for touch interactions
- **Touch Gestures**: Enhanced touch interactions with proper feedback
- **Double-tap Prevention**: Prevented accidental zoom on double-tap

### 🎨 **Enhanced Mobile Experience**
- **Larger Touch Targets**: Increased minimum touch target size to 44px for accessibility
- **Enhanced Mobile Navigation**: Improved mobile menu with backdrop blur effects
- **Mobile-Optimized Cards**: Enhanced card interactions with scale animations
- **Better Mobile Typography**: Optimized text rendering and spacing for mobile
- **Mobile-First Design**: Prioritized mobile experience with responsive enhancements

### 🔧 **Technical Improvements**
- **Service Worker Registration**: Automatic service worker registration and update handling
- **Offline Detection**: Real-time online/offline status detection and notifications
- **Update Notifications**: Automatic notifications when new versions are available
- **Performance Optimization**: Enhanced mobile performance with better caching
- **Cross-Platform Support**: Optimized for iOS, Android, and desktop browsers

### 🎯 **User Experience Enhancements**
- **Install Button**: Dynamic install button appears when PWA can be installed
- **Offline Indicators**: Visual feedback when user is offline
- **Update Prompts**: User-friendly update notifications with action buttons
- **Loading States**: Enhanced loading indicators and transitions
- **Smooth Animations**: App-like smooth transitions and micro-interactions

### 📱 **Mobile-Specific Features**
- **Backdrop Filters**: Modern backdrop blur effects for mobile navigation
- **Safe Area Support**: Proper spacing for devices with notches and rounded corners
- **Touch Feedback**: Visual and haptic feedback for all touch interactions
- **Gesture Recognition**: Advanced touch gesture recognition and handling
- **Mobile Forms**: Optimized form inputs to prevent zoom on iOS

### 🔒 **Security & Performance**
- **Secure Service Worker**: Proper security headers and HTTPS requirements
- **Efficient Caching**: Smart caching strategies for different content types
- **Background Sync**: Support for background synchronization when online
- **Push Notifications**: Framework for future push notification implementation
- **App Store Features**:
- **App Shortcuts**: Quick access to key pages (Home, Documents, Padati)
- **App Categories**: Proper categorization for app stores
- **Screenshots**: Support for app store screenshots
- **App Metadata**: Complete app information for installation
- **Standalone Mode**: Full-screen app experience when installed

---
*This changelog will be updated with every code change as per project requirements.*