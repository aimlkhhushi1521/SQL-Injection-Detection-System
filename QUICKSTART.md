# Quick Start Guide - SQL Injection Detection System

This guide will help you get the application running in under 10 minutes!

## 🚀 Quick Setup (Windows)

### Step 1: Install Dependencies

**Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

**Frontend:**
```powershell
cd frontend
npm install
cd ..
```

### Step 2: Configure Database

Edit `backend\.env` with your MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=sqli_detection
```

### Step 3: Train ML Model

```powershell
python train_model.py
```

### Step 4: Start the Application

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm start
```

### Step 5: Access the App

Open your browser to: **http://localhost:3000**

---

## 🧪 Test the Application

### 1. Register a User
- Go to http://localhost:3000/register
- Create a username and password
- Click "Create Account"

### 2. Login
- Go to http://localhost:3000/login
- Enter your credentials
- Click "Sign In"

### 3. Test SQL Queries
- Navigate to "Test Query" in the navbar
- Try these examples:

**Safe Query:**
```sql
SELECT * FROM users WHERE id = 1
```

**Malicious Query:**
```sql
' OR 1=1 --
```

### 4. View Dashboard
- Click "Dashboard" to see statistics
- View charts and recent attacks

---

## 🐛 Common Issues

### "MySQL Connection Error"
- Make sure MySQL is running
- Check your password in `backend\.env`
- Create database manually: `CREATE DATABASE sqli_detection;`

### "Module not found" errors
```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend won't start
```powershell
cd frontend
rm -r node_modules
npm install
npm start
```

### Port already in use
- Backend: Edit `backend\app.py` line with `port=5000`
- Frontend: Will auto-use port 3001 if 3000 is busy

---

## 📝 Default Admin Setup

All new users are created with `role='user'` by default.

To create an admin user, run this in MySQL after registration:
```sql
UPDATE users SET role = 'admin' WHERE username = 'your_username';
```

Admin users can access the "Logs" page to view all detection logs.

---

## 🎯 What to Try Next

1. ✅ Test various SQL injection patterns
2. ✅ View detection results and severity levels
3. ✅ Check dashboard statistics
4. ✅ Export logs to CSV (admin only)
5. ✅ Review security best practices in Query Tester
6. ✅ Try the example queries provided

---

## 📚 Need Help?

- Check the full README.md for detailed documentation
- Review API documentation for endpoint details
- See troubleshooting section in README.md

---

**That's it! You're ready to detect SQL injections! 🎉**
