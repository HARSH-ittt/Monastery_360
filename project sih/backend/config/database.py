import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='sacred_sikkim',
                user='root',  # Change this to your MySQL username
                password='',  # Change this to your MySQL password
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("✅ Successfully connected to MySQL database")
                return True
                
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def create_tables(self):
        """Create necessary tables for research submissions"""
        try:
            # Create research_submissions table
            create_research_table = """
            CREATE TABLE IF NOT EXISTS research_submissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                institution VARCHAR(255),
                abstract TEXT,
                keywords VARCHAR(500),
                file_path VARCHAR(500) NOT NULL,
                file_name VARCHAR(255) NOT NULL,
                file_size INT,
                file_type VARCHAR(50),
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # Create research_categories table
            create_categories_table = """
            CREATE TABLE IF NOT EXISTS research_categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            # Create research_submission_categories junction table
            create_junction_table = """
            CREATE TABLE IF NOT EXISTS research_submission_categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                submission_id INT,
                category_id INT,
                FOREIGN KEY (submission_id) REFERENCES research_submissions(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES research_categories(id) ON DELETE CASCADE,
                UNIQUE KEY unique_submission_category (submission_id, category_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            self.cursor.execute(create_research_table)
            self.cursor.execute(create_categories_table)
            self.cursor.execute(create_junction_table)
            
            # Insert default categories
            default_categories = [
                ('Monastery Architecture', 'Studies on monastery construction, design, and architectural evolution'),
                ('Buddhist Manuscripts', 'Research on ancient texts, translations, and manuscript preservation'),
                ('Cultural Heritage', 'Studies on traditions, rituals, and cultural practices'),
                ('Environmental Studies', 'Research on climate impact, conservation, and sustainability'),
                ('Art & Iconography', 'Studies on religious art, murals, and symbolic representations'),
                ('Historical Research', 'Historical studies and documentation of Sikkim heritage')
            ]
            
            for category in default_categories:
                self.cursor.execute(
                    "INSERT IGNORE INTO research_categories (name, description) VALUES (%s, %s)",
                    category
                )
            
            self.connection.commit()
            print("✅ Database tables created successfully")
            return True
            
        except Error as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    def insert_research_submission(self, data):
        """Insert a new research submission"""
        try:
            query = """
            INSERT INTO research_submissions 
            (title, author, email, institution, abstract, keywords, file_path, file_name, file_size, file_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                data['title'],
                data['author'],
                data['email'],
                data.get('institution', ''),
                data.get('abstract', ''),
                data.get('keywords', ''),
                data['file_path'],
                data['file_name'],
                data['file_size'],
                data['file_type']
            )
            
            self.cursor.execute(query, values)
            submission_id = self.cursor.lastrowid
            
            # Add categories if provided
            if 'categories' in data and data['categories']:
                for category_id in data['categories']:
                    self.cursor.execute(
                        "INSERT INTO research_submission_categories (submission_id, category_id) VALUES (%s, %s)",
                        (submission_id, category_id)
                    )
            
            self.connection.commit()
            return submission_id
            
        except Error as e:
            print(f"❌ Error inserting research submission: {e}")
            return None
    
    def get_research_submissions(self, status='approved', limit=50):
        """Get research submissions with optional filtering"""
        try:
            query = """
            SELECT rs.*, GROUP_CONCAT(rc.name) as categories
            FROM research_submissions rs
            LEFT JOIN research_submission_categories rsc ON rs.id = rsc.submission_id
            LEFT JOIN research_categories rc ON rsc.category_id = rc.id
            WHERE rs.status = %s
            GROUP BY rs.id
            ORDER BY rs.submission_date DESC
            LIMIT %s
            """
            
            self.cursor.execute(query, (status, limit))
            results = self.cursor.fetchall()
            
            # Convert to list of dictionaries
            submissions = []
            for row in results:
                submission = {
                    'id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'email': row[3],
                    'institution': row[4],
                    'abstract': row[5],
                    'keywords': row[6],
                    'file_path': row[7],
                    'file_name': row[8],
                    'file_size': row[9],
                    'file_type': row[10],
                    'submission_date': row[11].isoformat() if row[11] else None,
                    'status': row[12],
                    'created_at': row[13].isoformat() if row[13] else None,
                    'updated_at': row[14].isoformat() if row[14] else None,
                    'categories': row[15].split(',') if row[15] else []
                }
                submissions.append(submission)
            
            return submissions
            
        except Error as e:
            print(f"❌ Error fetching research submissions: {e}")
            return []
    
    def get_research_categories(self):
        """Get all research categories"""
        try:
            query = "SELECT id, name, description FROM research_categories ORDER BY name"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            categories = []
            for row in results:
                categories.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2]
                })
            
            return categories
            
        except Error as e:
            print(f"❌ Error fetching categories: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✅ Database connection closed")

# Initialize database manager
db_manager = DatabaseManager()

