"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-09-10
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "clinics",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(255), unique=True, nullable=False),
        sa.Column("phone", sa.String(50)),
        sa.Column("address", sa.Text),
        sa.Column("timezone", sa.String(50), server_default="Asia/Karachi"),
        sa.Column("whatsapp_number", sa.String(50)),
        sa.Column("branding_json", sa.JSON, server_default="{}"),
        sa.Column("subscription_tier", sa.String(50), server_default="solo"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "staff_users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clerk_user_id", sa.String(255), unique=True, nullable=False),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, server_default="receptionist"),
        sa.Column("full_name", sa.String(255)),
        sa.Column("phone", sa.String(50)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "patients",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(50)),
        sa.Column("email", sa.String(255)),
        sa.Column("dob", sa.DateTime),
        sa.Column("medical_notes", sa.Text),
        sa.Column("insurance_info", sa.JSON),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "services",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("duration_minutes", sa.Integer, nullable=False, server_default="30"),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("category", sa.String(100)),
    )

    op.create_table(
        "dentists",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), nullable=False),
        sa.Column("staff_user_id", UUID(as_uuid=True), sa.ForeignKey("staff_users.id")),
        sa.Column("specialty", sa.String(255)),
        sa.Column("working_hours_json", sa.JSON, server_default="{}"),
    )

    op.create_table(
        "appointments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), nullable=False),
        sa.Column("patient_id", UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("dentist_id", UUID(as_uuid=True), sa.ForeignKey("dentists.id"), nullable=False),
        sa.Column("service_id", UUID(as_uuid=True), sa.ForeignKey("services.id"), nullable=False),
        sa.Column("start_time", sa.DateTime, nullable=False),
        sa.Column("end_time", sa.DateTime, nullable=False),
        sa.Column("status", sa.String(20), server_default="pending"),
        sa.Column("booked_via", sa.String(20), server_default="staff"),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "conversations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), nullable=False),
        sa.Column("patient_id", UUID(as_uuid=True), sa.ForeignKey("patients.id")),
        sa.Column("channel", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("last_message_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "messages",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", UUID(as_uuid=True), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("tool_calls_json", sa.JSON),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "recall_campaigns",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("trigger_rule", sa.String(255), nullable=False),
        sa.Column("message_template", sa.Text),
        sa.Column("active", sa.Boolean, server_default="true"),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), unique=True, nullable=False),
        sa.Column("stripe_customer_id", sa.String(255)),
        sa.Column("stripe_subscription_id", sa.String(255)),
        sa.Column("plan", sa.String(50), server_default="solo"),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("current_period_end", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table("subscriptions")
    op.drop_table("recall_campaigns")
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("appointments")
    op.drop_table("dentists")
    op.drop_table("services")
    op.drop_table("patients")
    op.drop_table("staff_users")
    op.drop_table("clinics")
