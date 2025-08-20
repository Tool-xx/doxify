# 🔍 Doxify - Advanced Database Search Tool

![Doxify](https://img.shields.io/badge/Version-2.0.0-ff2a6d) 
![Python](https://img.shields.io/badge/Python-3.8%2B-blue) 
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20MacOS-lightgrey)

**A powerful desktop application for searching and analyzing data across multiple database formats with advanced search capabilities and professional export features.**

---

## ✨ Key Features

### 🔍 Advanced Search System
- **Basic Search** - Simple text search across all data
- **Regex Search** - Support for regular expressions
- **Case Sensitive** - Exact character matching
- **Whole Word** - Exclude partial matches
- **Fuzzy Search** - Intelligent pattern matching

### 📊 Multi-Format Support
- **CSV Files** - Comma-separated values
- **Excel Files** - .xlsx and .xls formats
- **JSON Data** - Structured data files
- **SQLite Databases** - .db database files
- **Text Files** - Plain text documents

### 🌍 Multi-Language Interface
- **English** - Full English localization
- **Russian** - Complete Russian support
- **Easy Switching** - Instant language change

### 📤 Professional Export
- **PDF Reports** - Professionally formatted documents
- **Structured Tables** - Preserved formatting and layout
- **Search Metadata** - Includes search parameters and timestamps
- **Branded Exports** - Doxify-branded document templates

### 🎨 Modern UI/UX
- **Cyberpunk Design** - Neon aesthetics with glass morphism
- **Smooth Animations** - Floating elements and particle effects
- **Responsive Design** - Adapts to different screen sizes
- **Dark Theme** - Easy on eyes during long sessions

### ⚡ Additional Features
- **Search History** - Track previous queries with results
- **File Management** - Upload/delete database files
- **Real-time Validation** - Instant feedback and error handling
- **Cross-Platform** - Works on Windows, Linux, and macOS

---

## 🛠 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 100MB free space
- **OS**: Windows 10+, macOS 10.15+, or Linux Ubuntu 18.04+

### Recommended Specifications
- **Python**: 3.10+
- **RAM**: 8GB or more
- **Storage**: 500MB SSD
- **GPU**: Hardware acceleration support

---

## 📦 Installation

### Method 1: Quick Install (Recommended)
```bash
# Clone the repository
git clone https://github.com/Tool-xx/doxify.git
cd doxify

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Manual Dependency Installation
```bash
pip install flask==2.3.3 pywebview==4.2.2 pandas==2.0.3 
pip install openpyxl==3.1.2 requests==2.31.0 reportlab==4.0.4
```

### Method 3: Developer Installation
```bash
# Create virtual environment
python -m venv doxify_env
source doxify_env/bin/activate  # Linux/Mac
# or
doxify_env\Scripts\activate  # Windows

# Install with development tools
pip install -r requirements.txt
pip install black flake8 pytest  # Optional development tools
```

---

## 🚀 Quick Start

### Running the Application
```bash
# Navigate to project directory
cd doxify

# Start the application
python app.py
```

The application will automatically:
- Open in a dedicated window (not a browser)
- Initialize the local web server
- Load the modern graphical interface
- Be ready for immediate use

### First-Time Setup
1. **Upload Databases**: Click "Upload Database" and select your files
2. **Select Database**: Choose from the uploaded files list
3. **Perform Search**: Enter your search query and configure options
4. **View Results**: Browse through matched records
5. **Export Results**: Download PDF reports of your findings

---

## 📖 User Guide

### 1. Database Management

#### Uploading Databases
- Click the "Upload Database" button
- Select files (multiple selection supported)
- Supported formats: CSV, XLSX, JSON, DB, TXT
- Files appear instantly in the database list

#### Deleting Databases
- Click the trash icon next to any database
- Confirm deletion in the dialog
- Immediate removal from the system

### 2. Search Operations

#### Basic Search
1. Select target database from dropdown
2. Enter search term in the text field
3. Click "Search" to execute
4. View results in tabular format

#### Advanced Search Options
- **Regex Mode**: Enable for pattern matching
- **Case Sensitive**: Toggle for exact case matching
- **Whole Word**: Match complete words only

### 3. Results Management

#### Viewing Results
- Results display in sortable tables
- Hover over cells to see full content
- Scroll through paginated results
- View search statistics and metadata

#### Exporting Results
- Click "Export to PDF" button
- Automatic generation of branded report
- Includes search parameters and timestamps
- Professional table formatting

### 4. Interface Features

#### Language Switching
- Click language buttons in top-right corner
- Instant interface translation
- Persistent language preference

#### Search History
- View last 5 search operations
- See timestamps and result counts
- Quick reference for previous work

---

## 🎨 Interface Overview

### Main Components
- **Header**: Doxify logo with animated effects
- **Upload Section**: File upload with drag-and-drop support
- **Database List**: Visual file management with icons
- **Search Panel**: Advanced search configuration
- **Results Area**: Dynamic data presentation
- **Export Tools**: Professional reporting options

### Navigation
- **Keyboard Shortcuts**: Enter to search, Esc to cancel
- **Mouse Controls**: Intuitive click interactions
- **Touch Support**: Responsive touch gestures

---

## 🔧 Technical Details

### Architecture
- **Frontend**: HTML5/CSS3/JavaScript with Bootstrap 5
- **Backend**: Flask Python web framework
- **GUI**: pywebview for native window rendering
- **Data Processing**: pandas for efficient data handling

### Performance Features
- **Multithreading**: Non-blocking UI during operations
- **Memory Management**: Efficient data loading and caching
- **Error Handling**: Graceful degradation and recovery
- **Security**: Local file operations only

### Supported File Specifications
- **CSV**: UTF-8 encoding, various delimiters
- **Excel**: .xlsx (Office Open XML format)
- **JSON**: Standard JSON with object/array structures
- **SQLite**: Standard .db files with table support
- **Text**: UTF-8 encoded plain text

---

## 🐛 Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### File Upload Issues
- Ensure files are not open in other programs
- Check file permissions in the uploads directory
- Verify file format compatibility

#### Search Performance
- For large files, use more specific search terms
- Consider splitting very large databases
- Ensure adequate system memory

### Getting Help

1. **Check Documentation**: Review this README thoroughly
2. **Community Support**: GitHub Issues page
3. **Debug Mode**: Run with console visible for detailed errors

---

## 📊 Performance Tips

### For Large Databases
- Use specific search terms to reduce results
- Enable regex only when necessary
- Close other memory-intensive applications
- Consider using SSD storage for better I/O

### Optimal Settings
- **CSV Files**: Best for medium-sized data
- **Excel Files**: Ideal for structured data
- **SQLite**: Best for very large datasets
- **JSON**: Perfect for nested data structures

---

## 🔮 Future Roadmap

### Planned Features
- **Cloud Integration**: Google Drive/Dropbox support
- **API Access**: RESTful API for automation
- **Plugins**: Extensible plugin architecture
- **Mobile App**: iOS/Android companion app
- **AI Features**: Smart search suggestions

### Upcoming Improvements
- **Performance**: Faster search algorithms
- **UI/UX**: Enhanced visual design
- **Security**: Encryption and access controls
- **Compatibility**: Additional file formats

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
git clone https://github.com/Tool-xx/doxify.git
cd doxify
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt  # Development tools
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- Flask: BSD License
- pandas: BSD 3-Clause
- pywebview: BSD 2-Clause
- ReportLab: BSD-style License

---

## 🙏 Acknowledgments

- **Contributors**: All amazing people who helped shape Doxify
- **Testers**: Early users who provided valuable feedback
- **Open Source Community**: For incredible tools and libraries
- **Users**: Everyone who uses Doxify for their data needs

---

## 📞 Support

### Community
- [GitHub Discussions](https://github.com/Tool-xx/doxify/discussions)

### Professional Support
- **Enterprise**: Contact for commercial support
- **Customization**: Custom feature development
- **Training**: Team training sessions available

---

## 🚀 Ready to Get Started?

```bash
# Clone and run!
git clone https://github.com/Tool-xx/doxify.git
cd doxify
pip install -r requirements.txt
python app.py
```

**Join thousands of users who trust Doxify for their data search needs!**

---


