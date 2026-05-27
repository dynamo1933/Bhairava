# 🕉️ Daiva Anughara - Sacred Spiritual Practice Website

A sacred spiritual website dedicated to Bhairava Sadhana and Sādhanā Paddhati, built with Flask and designed with reverence for spiritual practice.

## 🌟 Overview

Daiva Anughara is a sacred digital space that provides access to authentic spiritual knowledge, particularly focused on:
- **Bhairava Sadhana** - Ancient spiritual practices
- **Sādhanā Paddhati** - Practice methodology and guidelines
- **Ashtami Sadhana** - Sacred timing for spiritual advancement
- **Devi Worship** - Divine feminine energy practices

## ✨ Features

### 🎯 Core Functionality
- **Sacred Document Access** - PDF downloads for spiritual texts
- **Ashtami Countdown Timer** - Real-time countdown to next sacred practice
- **Site-wide Search** - Find spiritual content quickly
- **Responsive Design** - Mobile-first approach for all devices
- **Accessibility Features** - WCAG compliant with screen reader support

### 🎨 Design & User Experience
- **Sacred Color Scheme** - Army Green (#637457), Light Green (#8BBB67), Cream (#FCFBDF)
- **Typography** - Roboto for headings, Open Sans for body text
- **Spiritual Symbols** - Proper use of Om symbol (🕉️) and sacred imagery
- **Custom Icons** - Devi navigation uses Unicode cherry blossom (🌸) for divine feminine representation
- **Smooth Animations** - Gentle transitions honoring the spiritual nature

### 📱 Technical Features
- **Flask Backend** - Python-based web framework
- **RESTful APIs** - For countdown and search functionality
- **Mobile Navigation** - Hamburger menu with smooth animations
- **Cross-browser Support** - Modern browser compatibility
- **SEO Optimized** - Meta tags and structured data

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd daiva-anughara
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
daiva-anughara/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   ├── main.js            # Core functionality
│   │   ├── search.js          # Search functionality
│   │   └── countdown.js       # Countdown timer
│   ├── images/                 # Images and icons
│   └── documents/              # PDF documents
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── home.html              # Home page
│   ├── documents.html         # Documents page
│   ├── ashtami.html           # Ashtami page
│   ├── devi.html              # Devi page
│   ├── about.html             # About page
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
└── .gitignore                 # Git ignore file
```

## 🔧 Configuration

### Environment Variables
The application uses the following configuration:

```python
app.config['SECRET_KEY'] = 'daiva_anughara_sacred_key_2024'
app.config['UPLOAD_FOLDER'] = 'static/documents'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Ashtami Dates
Update the `ASHTAMI_DATES` list in `app.py` with upcoming dates:

```python
ASHTAMI_DATES = [
    {
        "date": "2024-09-14",
        "start_time": "05:04",
        "end_time": "2024-09-15 03:06",
        "timezone": "IST"
    }
]
```

## 📚 Sacred Documents

Place your PDF documents in the `static/documents/` directory:

- `Bhairava Sadhana Guidelines-M25.pdf`
- `Bhairava Ashtami Sadhana.pdf`
- `Bhaiarva Sadhana & Viniyoga.pdf`

## 🌐 API Endpoints

### Countdown API
- `GET /api/countdown` - Get countdown to next Ashtami
- `GET /api/next-ashtami` - Get next Ashtami date

### Search API
- `GET /search?q=<query>` - Search site content

## 🎨 Customization

### Colors
Modify the CSS variables in `static/css/style.css`:

```css
:root {
    --primary-green: #637457;      /* Army Green */
    --secondary-green: #8BBB67;    /* Light Green */
    --accent-cream: #FCFBDF;       /* Cream */
    --text-dark: #212121;          /* Dark Text */
}
```

### Typography
Update font imports in `templates/base.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@300;400;600&display=swap" rel="stylesheet">
```

## 📱 Responsive Design

The website is built with a mobile-first approach:

- **Mobile**: 480px and below
- **Tablet**: 481px to 1279px
- **Desktop**: 1280px and above

## ♿ Accessibility Features

- **Skip Links** - Quick navigation for screen readers
- **ARIA Labels** - Proper labeling for interactive elements
- **Keyboard Navigation** - Full keyboard support
- **Focus Indicators** - Clear focus states
- **Screen Reader Support** - Semantic HTML structure

## 🔍 Search Functionality

The site-wide search includes:

- **Real-time Results** - As you type (debounced)
- **Content Grouping** - Results organized by page
- **Query Highlighting** - Matched terms highlighted
- **Search History** - Local storage for recent searches
- **Keyboard Shortcuts** - Ctrl/Cmd + K to open search

## ⏰ Countdown Timer

Features include:

- **Real-time Updates** - Updates every minute/30 seconds
- **Visual Feedback** - Different styles for urgent/approaching times
- **Notifications** - Browser notifications for urgent countdowns
- **Error Handling** - Graceful fallbacks for API failures

## 🚀 Deployment

### Production Setup

1. **Set environment variables**
   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=0
   ```

2. **Use production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Configure reverse proxy** (Nginx/Apache)

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🧪 Testing

Run basic tests:

```bash
python -m pytest tests/
```

## 📊 Performance

- **Optimized Images** - WebP format support
- **Minified Assets** - Compressed CSS/JS
- **Lazy Loading** - Images load as needed
- **Caching** - Browser and server-side caching

## 🔒 Security

- **CSRF Protection** - Flask-WTF integration
- **Input Validation** - Sanitized user inputs
- **Secure Headers** - Security-focused HTTP headers
- **Rate Limiting** - API request throttling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Sacred Notice

**Important**: This website contains sacred spiritual content. Please approach with reverence and respect. The knowledge shared here is offered freely as a transmission of divine grace, not as a commercial transaction.

## 📞 Support

For spiritual guidance and technical support:
- **Spiritual Matters**: Contact through the website
- **Technical Issues**: Open an issue on GitHub

## 🌟 Acknowledgments

- **Bhairava Sadhana** tradition and lineage
- **Sādhanā Paddhati** methodology
- **Sacred spiritual community**
- **Open source contributors**

---

🕉️ **Om Namah Shivaya** 🕉️

*May the divine grace of Bhairava guide your spiritual journey.*



### Colors

Modify the CSS variables in `static/css/style.css`:



```css

:root {

    --primary-green: #637457;      /* Army Green */

    --secondary-green: #8BBB67;    /* Light Green */

    --accent-cream: #FCFBDF;       /* Cream */

    --text-dark: #212121;          /* Dark Text */

}

```



### Typography

Update font imports in `templates/base.html`:



```html

<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@300;400;600&display=swap" rel="stylesheet">

```



## 📱 Responsive Design



The website is built with a mobile-first approach:



- **Mobile**: 480px and below

- **Tablet**: 481px to 1279px

- **Desktop**: 1280px and above



## ♿ Accessibility Features



- **Skip Links** - Quick navigation for screen readers

- **ARIA Labels** - Proper labeling for interactive elements

- **Keyboard Navigation** - Full keyboard support

- **Focus Indicators** - Clear focus states

- **Screen Reader Support** - Semantic HTML structure



## 🔍 Search Functionality



The site-wide search includes:



- **Real-time Results** - As you type (debounced)

- **Content Grouping** - Results organized by page

- **Query Highlighting** - Matched terms highlighted

- **Search History** - Local storage for recent searches

- **Keyboard Shortcuts** - Ctrl/Cmd + K to open search



## ⏰ Countdown Timer



Features include:



- **Real-time Updates** - Updates every minute/30 seconds

- **Visual Feedback** - Different styles for urgent/approaching times

- **Notifications** - Browser notifications for urgent countdowns

- **Error Handling** - Graceful fallbacks for API failures



## 🚀 Deployment



### Production Setup



1. **Set environment variables**

   ```bash

   export FLASK_ENV=production

   export FLASK_DEBUG=0

   ```



2. **Use production WSGI server**

   ```bash

   pip install gunicorn

   gunicorn -w 4 -b 0.0.0.0:5000 app:app

   ```



3. **Configure reverse proxy** (Nginx/Apache)



### Docker Deployment



```dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

```



## 🧪 Testing



Run basic tests:



```bash

python -m pytest tests/

```



## 📊 Performance



- **Optimized Images** - WebP format support

- **Minified Assets** - Compressed CSS/JS

- **Lazy Loading** - Images load as needed

- **Caching** - Browser and server-side caching



## 🔒 Security



- **CSRF Protection** - Flask-WTF integration

- **Input Validation** - Sanitized user inputs

- **Secure Headers** - Security-focused HTTP headers

- **Rate Limiting** - API request throttling



## 🤝 Contributing



1. Fork the repository

2. Create a feature branch

3. Make your changes

4. Test thoroughly

5. Submit a pull request



## 📄 License



This project is licensed under the MIT License - see the LICENSE file for details.



## 🙏 Sacred Notice



**Important**: This website contains sacred spiritual content. Please approach with reverence and respect. The knowledge shared here is offered freely as a transmission of divine grace, not as a commercial transaction.



## 📞 Support



For spiritual guidance and technical support:

- **Spiritual Matters**: Contact through the website

- **Technical Issues**: Open an issue on GitHub



## 🌟 Acknowledgments



- **Bhairava Sadhana** tradition and lineage

- **Sādhanā Paddhati** methodology

- **Sacred spiritual community**

- **Open source contributors**



---



🕉️ **Om Namah Shivaya** 🕉️



*May the divine grace of Bhairava guide your spiritual journey.*


