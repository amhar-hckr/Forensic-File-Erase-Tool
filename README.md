# Forensic Instance Files Delete

A powerful forensic tool for securely managing and deleting files based on metadata analysis. This tool is designed for digital forensics professionals and system administrators who need to manage files based on their creators/authors.

![Banner](https://img.shields.io/badge/Forensics-File%20Management-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

## 🌟 Features

- **Advanced Metadata Analysis**
  - Deep scanning of file metadata
  - Multiple metadata tag support
  - Creator/author identification
  - Last modified by information
  - Company and ownership details

- **Multi-Format Support**
  - 📄 Documents (.doc, .docx, .pdf, .txt, .odt)
  - 📊 Spreadsheets (.xls, .xlsx, .xlsb, .xlsm)
  - 📈 Presentations (.ppt, .pptx, .odp)
  - 🖼️ Images (.jpg, .png, .svg, .bmp, .tiff)
  - 📹 Media Files (.mp4, .mp3, .wav, .mov)
  - 🗃️ Databases (.sql, .mdb, .db, .sqlite)
  - 📦 Archives (.zip, .rar, .7z, .tar)
  - ⚙️ System Files (.log, .ini, .json)
  - 💻 Source Code (.py, .js, .html)

- **Security Features**
  - Secure deletion option
  - Detailed operation logging
  - File access verification
  - Authorization warnings
  - Error handling and reporting

## 📋 Prerequisites

1. **System Requirements**
   - Windows Operating System
   - Python 3.8 or higher
   - 4GB RAM minimum (8GB recommended)
   - Admin privileges for system-wide scans

2. **Required Software**
   - ExifTool (included)
   - Python packages (see requirements.txt)

## 🚀 Installation

1. **Clone the Repository**
   ```powershell
   git clone https://github.com/yourusername/Forensic-Instance-Files-Delete.git
   cd Forensic-Instance-Files-Delete
   ```

2. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

## 💻 Usage Guide

### Running the Tool

1. **Start the Application**
   ```powershell
   python delete_excel_by_author.py
   ```

2. **Main Menu Options**
   - Choose file category to scan
   - Select scan mode:
     - Full Drive Scan
     - Specific Folder
     - Browse for Folder

3. **Scanning Process**
   - Wait for metadata analysis
   - Review discovered files
   - Files are grouped by creator

4. **File Management**
   - Select creator group
   - Review files in group
   - Confirm deletion
   - View operation results

### Advanced Features

1. **Secure Deletion**
   - Enables thorough file removal
   - Multiple pass overwrite
   - Metadata cleansing

2. **Error Handling**
   - Automatic logging
   - Detailed error messages
   - Recovery options

## 🛡️ Security Considerations

- **Authorization**
  - Ensure proper permissions
  - Use admin account when needed
  - Verify file ownership

- **Data Protection**
  - Files cannot be recovered after deletion
  - Verify selections before confirming
  - Check logs for audit trail

## 📝 Logging

- **Location**: `logs/` directory
- **Format**: `file_operations_YYYYMMDD_HHMMSS.log`
- **Contains**:
  - Operation timestamps
  - File details
  - Success/failure status
  - Error messages

## 🔧 Troubleshooting

1. **Common Issues**
   - Access denied errors
   - File in use messages
   - Metadata extraction failures

2. **Solutions**
   - Run as administrator
   - Close applications using target files
   - Check file permissions
   - Verify ExifTool installation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool performs permanent file operations. Always verify selections before confirming deletions. Users are responsible for ensuring proper authorization for file operations.

## 👥 Author

Developed by: Amh4ck3r

## 📞 Support

- Create an issue for bugs
- Submit feature requests via GitHub
- Check documentation for common solutions

---

**Note**: Keep your installation updated and regularly check for new releases with enhanced features and security updates.
