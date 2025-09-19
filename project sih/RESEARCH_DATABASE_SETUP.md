# Sacred Sikkim Research Database Setup

This document provides instructions for setting up the MySQL database integration for the research submission system.

## 🗄️ Database Features

- **Research Submission Form**: Users can submit research papers, manuscripts, and academic documents
- **File Upload Support**: PDF, DOC, DOCX, JPG, PNG, GIF, TIFF, BMP files (max 50MB)
- **Category System**: 6 predefined research categories for organization
- **Dynamic Display**: Submitted research appears automatically on the website
- **File Download**: Users can download approved research files
- **Admin Review**: Submissions require approval before public display

## 🚀 Quick Setup

### Prerequisites

1. **MySQL Server** installed and running
2. **Python 3.7+** with pip
3. **Node.js** (for frontend development)

### Step 1: Database Setup

1. **Start MySQL Server**
   ```bash
   # Windows (if using XAMPP/WAMP)
   # Start MySQL service from control panel
   
   # Linux/Mac
   sudo systemctl start mysql
   # or
   brew services start mysql
   ```

2. **Create Database and Tables**
   ```bash
   cd "P:\project sih\backend"
   python setup_database.py
   ```

### Step 2: Install Dependencies

```bash
cd "P:\project sih\backend"
pip install -r requirements.txt
```

### Step 3: Configure Database Connection

Edit `backend/config/database.py` and update the connection details:

```python
self.connection = mysql.connector.connect(
    host='localhost',
    database='sacred_sikkim',
    user='your_username',      # Change this
    password='your_password',   # Change this
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)
```

### Step 4: Start the Server

```bash
cd "P:\project sih\backend\api"
python server.py
```

The server will start at `http://localhost:3000`

## 📊 Database Schema

### Tables Created

1. **research_submissions**
   - Stores submitted research papers
   - Fields: id, title, author, email, institution, abstract, keywords, file_path, file_name, file_size, file_type, submission_date, status, created_at, updated_at

2. **research_categories**
   - Predefined research categories
   - Fields: id, name, description, created_at

3. **research_submission_categories**
   - Many-to-many relationship between submissions and categories
   - Fields: id, submission_id, category_id

### Default Categories

1. Monastery Architecture
2. Buddhist Manuscripts
3. Cultural Heritage
4. Environmental Studies
5. Art & Iconography
6. Historical Research

## 🔧 API Endpoints

### Research Submission
- **POST** `/api/research/submit` - Submit new research
- **GET** `/api/research/submissions` - Get approved submissions
- **GET** `/api/research/categories` - Get available categories
- **GET** `/api/research/file/<id>` - Download research file

### Example API Usage

```javascript
// Submit research
const formData = new FormData();
formData.append('title', 'My Research Title');
formData.append('author', 'Dr. John Doe');
formData.append('email', 'john@example.com');
formData.append('file', fileInput.files[0]);

fetch('/api/research/submit', {
    method: 'POST',
    body: formData
});

// Get submissions
fetch('/api/research/submissions')
    .then(response => response.json())
    .then(data => console.log(data.submissions));
```

## 🎨 Frontend Features

### Research Submission Form
- **Responsive Design**: Works on all devices
- **File Upload**: Drag & drop or click to upload
- **Category Selection**: Multiple category checkboxes
- **Form Validation**: Client and server-side validation
- **Progress Indicators**: Loading states and notifications

### Dynamic Research Display
- **Auto-loading**: Submissions appear automatically
- **Category Tags**: Visual category indicators
- **Download Buttons**: Direct file download links
- **Responsive Grid**: Adapts to screen size

## 🔒 Security Features

- **File Type Validation**: Only allowed file types accepted
- **File Size Limits**: 50MB maximum file size
- **SQL Injection Protection**: Parameterized queries
- **XSS Protection**: Input sanitization
- **CORS Configuration**: Proper cross-origin setup

## 📁 File Structure

```
backend/
├── api/
│   └── server.py              # Flask API server
├── config/
│   └── database.py            # Database connection and queries
├── setup_database.py          # Database setup script
├── requirements.txt           # Python dependencies
└── uploads/
    └── research/              # Uploaded research files

frontend/
└── index.html                 # Updated with research form
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check MySQL server is running
   - Verify credentials in `database.py`
   - Ensure database exists

2. **File Upload Fails**
   - Check file size (max 50MB)
   - Verify file type is allowed
   - Ensure uploads directory exists

3. **Categories Not Loading**
   - Check database connection
   - Verify categories table has data
   - Check browser console for errors

### Debug Mode

Enable debug mode in `server.py`:
```python
app.run(host='0.0.0.0', port=3000, debug=True)
```

## 📈 Usage Statistics

The system tracks:
- Total submissions
- Submission status (pending/approved/rejected)
- File types and sizes
- Submission dates
- Author information

## 🔄 Maintenance

### Regular Tasks
1. **Review Submissions**: Check pending submissions for approval
2. **Clean Uploads**: Remove old/rejected files periodically
3. **Backup Database**: Regular MySQL backups
4. **Monitor Storage**: Check uploads directory size

### Database Maintenance
```sql
-- Check submission counts
SELECT status, COUNT(*) FROM research_submissions GROUP BY status;

-- Clean old rejected submissions
DELETE FROM research_submissions WHERE status = 'rejected' AND created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

## 📞 Support

For technical support or questions about the research submission system, please check:
1. This documentation
2. Server logs for error messages
3. Browser console for frontend errors
4. MySQL logs for database issues

---

**Note**: This system is designed for academic and research purposes. Ensure all submitted content complies with your organization's policies and copyright laws.

