"use client";

import { useState } from "react";

interface Appointment {
  id: string;
  patient_name: string;
  service: string;
  dentist: string;
  date: string;
  time: string;
  status: "pending" | "confirmed" | "completed" | "cancelled";
  booked_via: "web" | "whatsapp" | "staff";
}

const mockAppointments: Appointment[] = [
  { id: "1", patient_name: "Ahmed Khan", service: "General Checkup", dentist: "Dr. Sarah", date: "2026-09-10", time: "10:00", status: "confirmed", booked_via: "whatsapp" },
  { id: "2", patient_name: "Fatima Ali", service: "Teeth Cleaning", dentist: "Dr. Usman", date: "2026-09-10", time: "11:00", status: "confirmed", booked_via: "web" },
  { id: "3", patient_name: "Hassan Raza", service: "Root Canal", dentist: "Dr. Sarah", date: "2026-09-10", time: "14:00", status: "pending", booked_via: "staff" },
  { id: "4", patient_name: "Ayesha Malik", service: "Teeth Whitening", dentist: "Dr. Usman", date: "2026-09-11", time: "09:00", status: "confirmed", booked_via: "whatsapp" },
];

const statusColors: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  confirmed: "bg-green-100 text-green-800",
  completed: "bg-blue-100 text-blue-800",
  cancelled: "bg-red-100 text-red-800",
};

export default function AppointmentsPage() {
  const [appointments] = useState<Appointment[]>(mockAppointments);

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Appointments</h1>
        <button className="rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700">
          New Appointment
        </button>
      </div>

      <div className="mt-6 overflow-hidden rounded-lg border">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Patient
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Service
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Dentist
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Date & Time
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Booked Via
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {appointments.map((apt) => (
              <tr key={apt.id}>
                <td className="whitespace-nowrap px-6 py-4 font-medium">
                  {apt.patient_name}
                </td>
                <td className="whitespace-nowrap px-6 py-4">{apt.service}</td>
                <td className="whitespace-nowrap px-6 py-4">{apt.dentist}</td>
                <td className="whitespace-nowrap px-6 py-4">
                  {apt.date} at {apt.time}
                </td>
                <td className="whitespace-nowrap px-6 py-4">
                  <span className={`inline-flex rounded-full px-2 py-1 text-xs font-semibold ${statusColors[apt.status]}`}>
                    {apt.status}
                  </span>
                </td>
                <td className="whitespace-nowrap px-6 py-4 capitalize">
                  {apt.booked_via}
                </td>
                <td className="whitespace-nowrap px-6 py-4">
                  <button className="text-primary-600 hover:text-primary-800">
                    Manage
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
