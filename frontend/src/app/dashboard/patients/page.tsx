"use client";

import { useState } from "react";

interface Patient {
  id: string;
  full_name: string;
  phone: string;
  email: string;
  last_visit: string;
}

const mockPatients: Patient[] = [
  { id: "1", full_name: "Ahmed Khan", phone: "+923001234567", email: "ahmed@email.com", last_visit: "2026-08-15" },
  { id: "2", full_name: "Fatima Ali", phone: "+923007654321", email: "fatima@email.com", last_visit: "2026-09-01" },
  { id: "3", full_name: "Hassan Raza", phone: "+923211234567", email: "hassan@email.com", last_visit: "2026-07-20" },
  { id: "4", full_name: "Ayesha Malik", phone: "+923331234567", email: "ayesha@email.com", last_visit: "2026-06-10" },
];

export default function PatientsPage() {
  const [patients] = useState<Patient[]>(mockPatients);

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Patients</h1>
        <button className="rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700">
          Add Patient
        </button>
      </div>

      <div className="mt-6 overflow-hidden rounded-lg border">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Phone
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Last Visit
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {patients.map((patient) => (
              <tr key={patient.id}>
                <td className="whitespace-nowrap px-6 py-4 font-medium">
                  {patient.full_name}
                </td>
                <td className="whitespace-nowrap px-6 py-4">{patient.phone}</td>
                <td className="whitespace-nowrap px-6 py-4">{patient.email}</td>
                <td className="whitespace-nowrap px-6 py-4">{patient.last_visit}</td>
                <td className="whitespace-nowrap px-6 py-4">
                  <button className="text-primary-600 hover:text-primary-800">
                    View
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
