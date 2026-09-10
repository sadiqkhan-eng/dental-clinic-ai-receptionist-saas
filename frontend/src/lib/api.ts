const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiRequest<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `API error: ${res.status}`);
  }

  return res.json();
}

export interface Clinic {
  id: string;
  name: string;
  slug: string;
  phone: string;
  address: string;
  timezone: string;
  whatsapp_number: string;
  subscription_tier: string;
}

export interface Patient {
  id: string;
  clinic_id: string;
  full_name: string;
  phone: string;
  email: string;
  dob: string;
  medical_notes: string;
}

export interface Service {
  id: string;
  clinic_id: string;
  name: string;
  duration_minutes: number;
  price: number;
  category: string;
}

export interface Dentist {
  id: string;
  clinic_id: string;
  staff_user_id: string;
  specialty: string;
  working_hours_json: string;
}

export interface Appointment {
  id: string;
  clinic_id: string;
  patient_id: string;
  dentist_id: string;
  service_id: string;
  start_time: string;
  end_time: string;
  status: "pending" | "confirmed" | "completed" | "cancelled" | "no_show";
  booked_via: "web" | "whatsapp" | "staff";
  notes: string;
}

export interface Conversation {
  id: string;
  clinic_id: string;
  patient_id: string;
  channel: "whatsapp" | "web";
  status: string;
  last_message_at: string;
}

export interface Message {
  id: string;
  role: "user" | "agent" | "staff";
  content: string;
  created_at: string;
}
