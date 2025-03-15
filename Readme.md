# Gym Management System

## 📌 Project Overview
The **Gym Management System** is a **Streamlit-based web application** designed to help gym administrators efficiently manage users, memberships, attendance, workout sessions, equipment usage, payments, and trainer assignments. The system also includes an extensive analytics dashboard to visualize key gym performance metrics.

## 🚀 Features
### **1. User Management**
- Register new users with membership details.
- Log attendance with check-in and check-out times.
- Update user health metrics such as weight, height, fat percentage, and BMI.

### **2. Membership & Payments**
- Assign different types of memberships (**Basic, VIP**) with associated benefits.
- Record payments and track revenue trends.

### **3. Workout & Equipment Tracking**
- Log workout sessions, including duration and calories burned.
- Track gym equipment usage and maintenance schedules.

### **4. Personal Training & Feedback**
- Assign personal training plans to users.
- Allow users to rate trainers and leave feedback.

### **5. Reports & Analytics**
- **Membership Distribution**: View total users per membership type.
- **Attendance Trends**: Track gym visits over time.
- **Trainer Performance**: Evaluate trainers based on assigned plans and feedback ratings.
- **Equipment Usage**: Analyze which equipment is used the most.
- **Revenue Trends**: View monthly revenue breakdown.
- **User Retention & Churn**: Identify inactive users.
- **User Progress Tracking**: Monitor health metrics over time.
- **Most Active Users**: Identify top attendees in a selected period.

## 🏗️ Tech Stack
### **Backend**
- **Python**
- **SQLAlchemy** 
- **MySQL** (Database)

### **Frontend**
- **Streamlit** (Web UI)
- **Pandas & Matplotlib** (Data visualization)

## 📂 Project Structure
```
📁 4791-Database-Project/
│── db.py               # Database models and session management
│── main.py             # Streamlit application
│── .env                # Environment variables (database credentials)
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
```

## 🔧 Setup & Installation
### **1. Clone the Repository**
```sh
git clone https://github.com/HongQuan13/4791-Database-Project.git
cd 4791-Database-Project
```

### **2. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **3. Setup Environment Variables**
Create a **.env** file in the project root directory and add:
```sh
DB_PASSWORD=your_db_password
DB_PORT=your_db_port
DB_NAME=your_db_name
```

### **4. Run Database Migrations**
Ensure MySQL is running, then create the necessary tables:
```sh
python db.py
```

### **5. Run the Streamlit Application**
```sh
streamlit run main.py
```

## 📝 Usage Guide
1. Select a section from the left sidebar menu.
2. Fill out the required fields in the respective forms.
3. Submit the data, and the system will process it accordingly.
4. Navigate to the **Reports & Analytics** section to view gym insights.

## 📌 Future Improvements
- Implement user authentication.
- Add an admin dashboard for advanced management.
- Integrate real-time notifications and reminders.
- Improve UI/UX with enhanced visual elements.

## 📌 Contributors
- **Hong Quan** (Project Owner)

## 📌 License
This project is licensed under the **MIT License**.

