"use client";

import { useState, useEffect } from "react";
import { apiRequest } from "@/lib/api";

interface Appointment {
  id: string;
  service: string;
  dentist: string;
  start_time: string;
  status: string;
}

interface PatientData {
  id: string;
  full_name: string;
  phone: string;
  email: string;
}

export default function PatientPortalPage() {
  const [patient, setPatient] = useState<PatientData | null>(null);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [activeTab, setActiveTab] = useState<"appointments" | "profile">("appointments");

  useEffect(() => {
    const pid = localStorage.getItem("patient_id");
    if (pid) {
      apiRequest<PatientData>(`/api/patients/${pid}`).then(setPatient).catch(() => {});
    }
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex gap-4 border-b pb-4">
        <button
          onClick={() => setActiveTab("appointments")}
          className={`px-4 py-2 font-medium ${activeTab === "appointments" ? "border-b-2 border-primary-600 text-primary-600" : "text-gray-500"}`}
        >
          My Appointments
        </button>
        <button
          onClick={() => setActiveTab("profile")}
          className={`px-4 py-2 font-medium ${activeTab === "profile" ? "border-b-2 border-primary-600 text-primary-600" : "text-gray-500"}`}
        >
          My Profile
        </button>
      </div>

      {activeTab === "appointments" && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Upcoming Appointments</h2>
          {appointments.length === 0 ? (
            <p className="text-gray-500">No upcoming appointments.</p>
          ) : (
            appointments.map((apt) => (
              <div key={apt.id} className="rounded-lg border p-4">
                <p className="font-medium">{apt.service}</p>
                <p className="text-sm text-gray-500">
                  {new Date(apt.start_time).toLocaleString()}
                </p>
                <span className="inline-block mt-2 rounded-full bg-green-100 px-2 py-1 text-xs text-green-800">
                  {apt.status}
                </span>
              </div>
            ))
          )}
        </div>
      </div>

      {activeTab === "profile" && patient && (
        <div className="rounded-lg border p-6">
          <h2 className="text-lg font-semibold">My Profile</h2>
          <div className="mt-4 space-y-2">
            <p><span className="font-medium">Name:</span> {patient.full_name}</p>
            <p><span className="font-medium">Phone:</span> {patient.phone}</p>
            <p><span className="font-medium">Email:</span> {patient.email}</p>
          </div>
        </div>
      )}
    </div>
  );
}
