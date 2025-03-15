import streamlit as st
import pandas as pd
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from db import (
    session,
    User,
    AttendanceLog,
    WorkoutSession,
    Payment,
    Feedback,
    Membership,
    UserStatus,
    PersonalTrainingPlan,
    WorkoutEquipmentAssociation,
)

# Streamlit UI
st.title("🏋️‍♂️ Gym Management System")

menu = st.sidebar.selectbox(
    "Choose a Section",
    [
        "User Registration",
        "Attendance Logging",
        "Workout Session Entry",
        "Equipment Usage Recording",
        "Payment Processing",
        "Personal Training Plan Assignment",
        "Trainer Feedback Submission",
        "User Health Metrics Update",
        "Reports & Analytics",
    ],
)

# ============================
# 📊 REPORTS & ANALYTICS SECTION
# ============================
if menu == "Reports & Analytics":
    st.header("📊 Reports & Analytics")

    # Membership Distribution Report
    st.subheader("🏅 Membership Distribution")
    membership_data = session.execute(
        text(
            "SELECT membership_type, COUNT(user_id) AS total_users FROM USER U JOIN MEMBERSHIP M ON U.membership_id = M.membership_id GROUP BY membership_type"
        )
    ).fetchall()

    if membership_data:
        df_membership = pd.DataFrame(
            membership_data, columns=["Membership Type", "Total Users"]
        )
        st.bar_chart(df_membership.set_index("Membership Type"))
        st.table(df_membership)
    else:
        st.write("No membership data available.")

    # Attendance Analysis Report
    st.subheader("📅 Attendance Trends (March 1 - March 15, 2025)")
    # Query to get attendance logs for March 1 - March 15, 2025
    attendance_data = session.execute(
        text(
            "SELECT DATE(check_in_time) AS visit_date, COUNT(*) AS total_visits FROM ATTENDANCE_LOG WHERE check_in_time BETWEEN '2025-03-01' AND '2025-03-15' GROUP BY visit_date ORDER BY visit_date"
        )
    ).fetchall()

    # Convert to Pandas DataFrame
    df_attendance = pd.DataFrame(attendance_data, columns=["Date", "Total Visits"])

    if attendance_data:
        # Display Data Table
        st.table(df_attendance)

        # Line Chart for Attendance Trends
        st.line_chart(df_attendance.set_index("Date"))
    else:
        st.write("No attendance data available.")

    # Trainer Performance Report
    st.subheader("🏋️ Trainer Performance")
    trainer_data = session.execute(
        text(
            "SELECT T.trainer_name, COUNT(P.plan_id) AS total_plans, COALESCE(AVG(F.rating), 0) AS avg_rating FROM TRAINER T LEFT JOIN PERSONAL_TRAINING_PLAN P ON T.trainer_id = P.trainer_id LEFT JOIN FEEDBACK F ON T.trainer_id = F.trainer_id GROUP BY T.trainer_name ORDER BY avg_rating DESC"
        )
    ).fetchall()

    if trainer_data:
        df_trainers = pd.DataFrame(
            trainer_data, columns=["Trainer", "Plans Assigned", "Average Rating"]
        )
        st.table(df_trainers)
    else:
        st.write("No trainer performance data available.")

    # Select Month & Year for Filtering
    selected_month = st.selectbox(
        "Select Month", ["2025-03", "2025-02", "2025-01"], index=0
    )  # Default to March 2025

    # Workout Equipment Usage Report for the Selected Month
    st.subheader(f"🏋️‍♂️ Equipment Usage for {selected_month}")

    equipment_data = session.execute(
        text(
            "SELECT E.equipment_name, COUNT(A.workout_id) AS usage_count, AVG(A.usage_duration) AS avg_duration "
            "FROM WORKOUT_EQUIPMENT E "
            "JOIN WORKOUT_EQUIPMENT_ASSOCIATION A ON E.equipment_id = A.equipment_id "
            "JOIN WORKOUT_SESSION W ON A.workout_id = W.workout_id "
            "WHERE DATE_FORMAT(W.workout_time, '%Y-%m') = :selected_month "
            "GROUP BY E.equipment_name "
            "ORDER BY usage_count DESC"
        ),
        {"selected_month": selected_month},
    ).fetchall()

    if equipment_data:
        df_equipment = pd.DataFrame(
            equipment_data, columns=["Equipment", "Usage Count", "Avg Duration (min)"]
        )
        st.table(df_equipment)
    else:
        st.write("No equipment usage data available for this month.")

    # Payment & Revenue Report
    st.subheader("💰 Revenue Trends")

    # Fetch Revenue Data
    revenue_data = session.execute(
        text(
            "SELECT DATE_FORMAT(payment_date, '%Y-%m') AS month, SUM(amount) AS total_revenue "
            "FROM PAYMENT "
            "GROUP BY month "
            "ORDER BY month ASC"
        )
    ).fetchall()

    # Convert to Pandas DataFrame
    df_revenue = pd.DataFrame(revenue_data, columns=["Month", "Total Revenue"])

    # Ensure "Total Revenue" is numeric
    df_revenue["Total Revenue"] = pd.to_numeric(df_revenue["Total Revenue"])

    # Sort months correctly
    df_revenue = df_revenue.sort_values(by="Month")

    # Display Data Table
    st.subheader("💰 Monthly Revenue Trends")
    st.table(df_revenue)

    # Plot Revenue Trends as a Line Chart
    st.line_chart(df_revenue.set_index("Month"))

    # User Retention & Churn Report
    st.subheader("🚶‍♂️ User Retention & Churn")
    churn_data = session.execute(
        text(
            "SELECT U.user_name, MAX(A.check_in_time) AS last_visit FROM USER U LEFT JOIN ATTENDANCE_LOG A ON U.user_id = A.user_id GROUP BY U.user_name HAVING last_visit < DATE_SUB(NOW(), INTERVAL 3 MONTH) OR last_visit IS NULL"
        )
    ).fetchall()

    if churn_data:
        df_churn = pd.DataFrame(churn_data, columns=["User Name", "Last Visit"])
        st.table(df_churn)
    else:
        st.write("No churn data available.")

    # User Progress Report
    st.subheader("⚕️ User Progress (Last 6 Months)")
    progress_data = session.execute(
        text(
            "SELECT U.user_name, S.weight, S.height, S.BMI, S.time_measured FROM USER_STATUS S JOIN USER U ON S.user_id = U.user_id WHERE S.time_measured >= DATE_SUB(NOW(), INTERVAL 6 MONTH) ORDER BY S.time_measured DESC"
        )
    ).fetchall()

    if progress_data:
        df_progress = pd.DataFrame(
            progress_data,
            columns=["User Name", "Weight (kg)", "Height (m)", "BMI", "Measured On"],
        )
        st.table(df_progress)
    else:
        st.write("No health progress data available.")

    # Default Date Range: Today & 30 Days Ago
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    # User Selects Date Range
    st.subheader("🏆 Most Active Users")
    start_date = st.date_input("Start Date", start_date)
    end_date = st.date_input("End Date", end_date)

    # Ensure start_date is before end_date
    if start_date > end_date:
        st.error("Start Date cannot be after End Date. Please select a valid range.")
    else:
        # Fetch Most Active Users in the Selected Date Range
        active_users_data = session.execute(
            text(
                "SELECT U.user_name, COUNT(A.log_id) AS total_visits "
                "FROM USER U "
                "JOIN ATTENDANCE_LOG A ON U.user_id = A.user_id "
                "WHERE A.check_in_time BETWEEN :start_date AND :end_date "
                "GROUP BY U.user_name "
                "ORDER BY total_visits DESC "
                "LIMIT 10"
            ),
            {"start_date": start_date, "end_date": end_date},
        ).fetchall()

        # Display the Data
        if active_users_data:
            df_active_users = pd.DataFrame(
                active_users_data, columns=["User Name", "Total Visits"]
            )
            st.table(df_active_users)
            st.bar_chart(df_active_users.set_index("User Name"))
        else:
            st.write("No active user data available for the selected period.")

# ============================
# EXISTING FORMS (Unchanged)
# ============================
elif menu == "User Registration":
    st.header("📋 New User Registration")
    with st.form("register_form"):
        membership_id = st.number_input("Membership ID", min_value=1, step=1)
        user_name = st.text_input("User Name")
        user_email = st.text_input("User Email")
        user_phone = st.text_input("User Phone Number")
        dob = st.date_input("Date of Birth")
        reg_date = datetime.now()

        submit = st.form_submit_button("Register User")
        if submit:
            session.rollback()
            new_user = User(
                membership_id=membership_id,
                user_name=user_name,
                user_email=user_email,
                user_phone_number=user_phone,
                date_of_birth=dob,
                registeration_date=reg_date,
            )
            session.add(new_user)
            session.commit()
            st.success(f"User {user_name} registered successfully!")

# Form 2: Attendance Logging
elif menu == "Attendance Logging":
    st.header("🛂 Attendance Logging")
    with st.form("attendance_form"):
        user_id = st.number_input("User ID", min_value=1, step=1)
        check_in = st.time_input("Check-In Time", value=datetime.now().time())
        check_out = st.time_input("Check-Out Time")

        submit = st.form_submit_button("Log Attendance")
        if submit:

            check_in_datetime = datetime.combine(datetime.today(), check_in)
            check_out_datetime = datetime.combine(datetime.today(), check_out)
            session.rollback()
            new_attendance = AttendanceLog(
                user_id=user_id,
                check_in_time=check_in_datetime,
                check_out_time=check_out_datetime,
            )
            session.add(new_attendance)
            session.commit()
            st.success(f"Attendance recorded for User ID {user_id}")

# Form 3: Workout Session Entry
elif menu == "Workout Session Entry":
    st.header("🏋️‍♂️ Workout Session Entry")
    with st.form("workout_form"):
        user_id = st.number_input("User ID", min_value=1, step=1)
        workout_duration = st.number_input("Workout Duration (minutes)", min_value=1)
        calories_burned = st.number_input("Calories Burned", min_value=0.0)

        submit = st.form_submit_button("Save Workout")
        if submit:
            new_workout = WorkoutSession(
                user_id=user_id,
                workout_duration=workout_duration,
                calorie_burned=calories_burned,
            )
            session.add(new_workout)
            session.commit()
            st.success(f"Workout session for User ID {user_id} saved!")

# Form 4: Equipment Usage Recording
elif menu == "Equipment Usage Recording":
    st.header("🛠️ Equipment Usage Recording")
    with st.form("equipment_form"):
        equipment_id = st.number_input("Equipment ID", min_value=1, step=1)
        workout_id = st.number_input("Workout Session ID", min_value=1, step=1)
        usage_duration = st.number_input("Usage Duration (minutes)", min_value=1)

        submit = st.form_submit_button("Record Equipment Usage")
        if submit:
            new_usage = WorkoutEquipmentAssociation(
                equipment_id=equipment_id,
                workout_id=workout_id,
                usage_duration=usage_duration,
            )
            session.rollback()
            session.add(new_usage)
            session.commit()
            st.success(
                f"Equipment {equipment_id} usage recorded for Workout {workout_id}"
            )

# Form 5: Payment Processing
elif menu == "Payment Processing":
    st.header("💳 Payment Processing")
    with st.form("payment_form"):
        user_id = st.number_input("User ID", min_value=1, step=1)
        amount = st.number_input("Payment Amount", min_value=1.0, format="%.2f")
        payment_method = st.selectbox(
            "Payment Method", ["Credit Card", "Debit Card", "Cash", "Bank Transfer"]
        )

        submit = st.form_submit_button("Process Payment")
        if submit:
            session.rollback()
            new_payment = Payment(
                user_id=user_id, amount=amount, payment_method=payment_method
            )
            session.add(new_payment)
            session.commit()
            st.success(f"Payment of ${amount} received from User ID {user_id}")

# Form 6: Personal Training Plan Assignment
elif menu == "Personal Training Plan Assignment":
    st.header("📑 Assign Training Plan")
    with st.form("training_plan_form"):
        trainer_id = st.number_input("Trainer ID", min_value=1, step=1)
        user_id = st.number_input("User ID", min_value=1, step=1)
        plan_details = st.text_area("Plan Details")
        plan_start_date = st.date_input("Plan Start Date")
        duration = st.number_input("Duration (days)", min_value=1)
        progress_status = st.selectbox("Progress Status", ["In Progress", "Completed"])

        submit = st.form_submit_button("Assign Plan")
        if submit:
            new_plan = PersonalTrainingPlan(
                trainer_id=trainer_id,
                user_id=user_id,
                plan_details=plan_details,
                plan_start_date=plan_start_date,
                duration=duration,
                progress_status=progress_status,
            )
            session.add(new_plan)
            session.commit()
            st.success(f"Training plan assigned to User ID {user_id}")

# Form 7: Trainer Feedback Submission
elif menu == "Trainer Feedback Submission":
    st.header("📝 Trainer Feedback")
    with st.form("feedback_form"):
        user_id = st.number_input("User ID", min_value=1, step=1)
        trainer_id = st.number_input("Trainer ID", min_value=1, step=1)
        rating = st.slider("Rating", 1, 5)
        comments = st.text_area("Comments")

        submit = st.form_submit_button("Submit Feedback")
        if submit:
            new_feedback = Feedback(
                user_id=user_id, trainer_id=trainer_id, rating=rating, comments=comments
            )
            session.add(new_feedback)
            session.commit()
            st.success(f"Feedback for Trainer ID {trainer_id} submitted!")

# Form 8: User Health Metrics Update
elif menu == "User Health Metrics Update":
    st.header("⚕️ User Health Metrics")
    with st.form("health_metrics_form"):
        user_id = st.number_input("User ID", min_value=1, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.1, format="%.1f")
        height = st.number_input("Height (m)", min_value=1.5, format="%.1f")
        fat_percentage = st.number_input(
            "Fat Percentage", min_value=0.0, max_value=100.0, format="%.1f"
        )

        submit = st.form_submit_button("Update Health Metrics")
        if submit:
            session.rollback()
            new_health = UserStatus(
                user_id=user_id,
                weight=weight,
                height=height,
                fat_percentage=fat_percentage,
                BMI=weight / ((height) ** 2),
            )
            session.add(new_health)
            session.commit()
            st.success(f"Health metrics for User ID {user_id} updated!")
