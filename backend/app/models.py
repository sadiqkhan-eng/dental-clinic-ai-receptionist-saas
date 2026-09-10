import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50))
    address = Column(Text)
    timezone = Column(String(50), default="Asia/Karachi")
    whatsapp_number = Column(String(50))
    branding_json = Column(JSON, default=dict)
    subscription_tier = Column(String(50), default="solo")
    created_at = Column(DateTime, default=datetime.utcnow)

    staff_users = relationship("StaffUser", back_populates="clinic")
    patients = relationship("Patient", back_populates="clinic")
    services = relationship("Service", back_populates="clinic")
    dentists = relationship("Dentist", back_populates="clinic")
    appointments = relationship("Appointment", back_populates="clinic")
    conversations = relationship("Conversation", back_populates="clinic")
    recall_campaigns = relationship("RecallCampaign", back_populates="clinic")
    subscription = relationship("Subscription", back_populates="clinic", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="clinic")
    waiting_list = relationship("WaitingList", back_populates="clinic")
    referrals = relationship("Referral", back_populates="clinic")
    invoices = relationship("Invoice", back_populates="clinic")


class StaffUser(Base):
    __tablename__ = "staff_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clerk_user_id = Column(String(255), unique=True, nullable=False)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    role = Column(String(50), nullable=False, default="receptionist")
    full_name = Column(String(255))
    phone = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("Clinic", back_populates="staff_users")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50))
    email = Column(String(255))
    dob = Column(DateTime)
    medical_notes = Column(Text)
    insurance_info = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("Clinic", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")


class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    name = Column(String(255), nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=30)
    price = Column(Float, nullable=False)
    category = Column(String(100))

    clinic = relationship("Clinic", back_populates="services")


class Dentist(Base):
    __tablename__ = "dentists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    staff_user_id = Column(UUID(as_uuid=True), ForeignKey("staff_users.id"))
    specialty = Column(String(255))
    working_hours_json = Column(JSON, default=dict)

    clinic = relationship("Clinic", back_populates="dentists")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    dentist_id = Column(UUID(as_uuid=True), ForeignKey("dentists.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(20), default="pending")
    booked_via = Column(String(20), default="staff")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("Clinic", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    channel = Column(String(20), nullable=False)
    status = Column(String(20), default="active")
    sentiment_score = Column(Float, nullable=True)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("Clinic", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    tool_calls_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class RecallCampaign(Base):
    __tablename__ = "recall_campaigns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    name = Column(String(255), nullable=False)
    trigger_rule = Column(String(255), nullable=False)
    message_template = Column(Text)
    active = Column(Boolean, default=True)

    clinic = relationship("Clinic", back_populates="recall_campaigns")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), unique=True, nullable=False)
    stripe_customer_id = Column(String(255))
    stripe_subscription_id = Column(String(255))
    plan = Column(String(50), default="solo")
    status = Column(String(20), default="active")
    current_period_end = Column(DateTime)

    clinic = relationship("Clinic", back_populates="subscription")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    user_id = Column(String(255))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(255))
    details = Column(JSON)
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("Clinic", back_populates="audit_logs")


class WaitingList(Base):
    __tablename__ = "waiting_list"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"))
    preferred_date = Column(DateTime)
    status = Column(String(20), default="waiting")
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("Clinic", back_populates="waiting_list")


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    referrer_patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    referred_patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    referral_code = Column(String(50))
    reward_applied = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("Clinic", back_populates="referrals")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="PKR")
    status = Column(String(20), default="pending")
    payment_method = Column(String(50))
    payment_reference = Column(String(255))
    pdf_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("Clinic", back_populates="invoices")
