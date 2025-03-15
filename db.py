import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    DECIMAL,
    Boolean,
    Date,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mysql+mysqlconnector://root:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"
)

# Create Engine
engine = create_engine(DATABASE_URL, echo=True)

# Base ORM Model
Base = declarative_base()

# ORM Models
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    DECIMAL,
    Boolean,
    Date,
    Time,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


# 1. MEMBERSHIP Table
class Membership(Base):
    __tablename__ = "MEMBERSHIP"
    membership_id = Column(Integer, primary_key=True, autoincrement=True)
    membership_type = Column(String(50))
    price = Column(DECIMAL(10, 2))
    valid_period = Column(Integer)  # Valid period in days
    discount_amount = Column(DECIMAL(10, 2))


# 2. USER Table
class User(Base):
    __tablename__ = "USER"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    membership_id = Column(Integer, ForeignKey("MEMBERSHIP.membership_id"))
    user_name = Column(String(100))
    user_email = Column(String(100))
    user_phone_number = Column(String(20))
    date_of_birth = Column(Date)
    registeration_date = Column(DateTime, default=datetime.now)


# 3. VIP Table (Specialization of Membership)
class VIP(Base):
    __tablename__ = "VIP"
    membership_id = Column(
        Integer, ForeignKey("MEMBERSHIP.membership_id"), primary_key=True
    )
    spa_access = Column(Boolean)
    free_guest_passes = Column(Integer)
    personal_trainer_discount = Column(DECIMAL(10, 2))


# 4. BASIC Table (Specialization of Membership)
class Basic(Base):
    __tablename__ = "BASIC"
    membership_id = Column(
        Integer, ForeignKey("MEMBERSHIP.membership_id"), primary_key=True
    )
    max_session_per_month = Column(Integer)
    gym_access_hours = Column(Integer)


# 5. TRAINER Table
class Trainer(Base):
    __tablename__ = "TRAINER"
    trainer_id = Column(Integer, primary_key=True, autoincrement=True)
    trainer_name = Column(String(100))
    trainer_specialization = Column(String(100))
    trainer_phone_number = Column(String(20))
    trainer_email = Column(String(100))


# 6. WORKOUT_SESSION Table
class WorkoutSession(Base):
    __tablename__ = "WORKOUT_SESSION"
    workout_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USER.user_id"))
    workout_time = Column(DateTime, default=datetime.now)
    workout_duration = Column(Integer)  # in minutes
    calorie_burned = Column(DECIMAL(10, 2))


# 7. WORKOUT_EQUIPMENT Table
class WorkoutEquipment(Base):
    __tablename__ = "WORKOUT_EQUIPMENT"
    equipment_id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_name = Column(String(100))
    equipment_category = Column(String(50))
    last_maintenance_date = Column(Date)


# 8. WORKOUT_EQUIPMENT_ASSOCIATION Table
class WorkoutEquipmentAssociation(Base):
    __tablename__ = "WORKOUT_EQUIPMENT_ASSOCIATION"
    equipment_id = Column(
        Integer, ForeignKey("WORKOUT_EQUIPMENT.equipment_id"), primary_key=True
    )
    workout_id = Column(
        Integer, ForeignKey("WORKOUT_SESSION.workout_id"), primary_key=True
    )
    usage_duration = Column(Integer)  # in minutes


# 9. ATTENDANCE_LOG Table
class AttendanceLog(Base):
    __tablename__ = "ATTENDANCE_LOG"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USER.user_id"))
    check_in_time = Column(DateTime)
    check_out_time = Column(DateTime)


# 10. USER_STATUS Table
class UserStatus(Base):
    __tablename__ = "USER_STATUS"
    user_status_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USER.user_id"))
    weight = Column(DECIMAL(5, 2))
    height = Column(DECIMAL(5, 2))
    fat_percentage = Column(DECIMAL(4, 2))
    time_measured = Column(DateTime, default=datetime.now)
    BMI = Column(DECIMAL(5, 2))


# 11. PAYMENT Table
class Payment(Base):
    __tablename__ = "PAYMENT"
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USER.user_id"))
    amount = Column(DECIMAL(10, 2))
    payment_date = Column(DateTime, default=datetime.now)
    payment_method = Column(String(50))


# 12. SESSION_SCHEDULE Table
class SessionSchedule(Base):
    __tablename__ = "SESSION_SCHEDULE"
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    trainer_id = Column(Integer, ForeignKey("TRAINER.trainer_id"))
    user_id = Column(Integer, ForeignKey("USER.user_id"))
    session_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)


# 13. PERSONAL_TRAINING_PLAN Table
class PersonalTrainingPlan(Base):
    __tablename__ = "PERSONAL_TRAINING_PLAN"
    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    trainer_id = Column(Integer, ForeignKey("TRAINER.trainer_id"))
    user_id = Column(Integer, ForeignKey("USER.user_id"))
    plan_details = Column(Text)
    plan_start_date = Column(Date)
    duration = Column(Integer)  # duration in days
    progress_status = Column(String(50))


# 14. FEEDBACK Table
class Feedback(Base):
    __tablename__ = "FEEDBACK"
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("USER.user_id"))
    trainer_id = Column(Integer, ForeignKey("TRAINER.trainer_id"))
    rating = Column(DECIMAL(3, 2))
    comments = Column(Text)
    feedback_time = Column(DateTime, default=datetime.now)


# Create Tables
Base.metadata.create_all(engine)

# Session Factory
Session = sessionmaker(bind=engine)
session = Session()
