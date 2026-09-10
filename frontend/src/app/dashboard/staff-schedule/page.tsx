"use client";

import { useState } from "react";

interface StaffSchedule {
  id: string;
  name: string;
  specialty: string;
  schedule: { day: string; start: string; end: string }[];
}

const mockSchedule: StaffSchedule[] = [
  {
    id: "1",
    name: "Dr. Sarah Ahmed",
    specialty: "General Dentistry",
    schedule: [
      { day: "Mon", start: "09:00", end: "17:00" },
      { day: "Tue", start: "09:00", end: "17:00" },
      { day: "Wed", start: "09:00", end: "13:00" },
      { day: "Thu", start: "09:00", end: "17:00" },
      { day: "Fri", start: "09:00", end: "17:00" },
    ],
  },
  {
    id: "2",
    name: "Dr. Usman Khan",
    specialty: "Orthodontics",
    schedule: [
      { day: "Mon", start: "10:00", end: "18:00" },
      { day: "Tue", start: "10:00", end: "18:00" },
      { day: "Wed", start: "10:00", end: "18:00" },
      { day: "Thu", start: "10:00", end: "18:00" },
      { day: "Fri", start: "10:00", end: "14:00" },
    ],
  },
];

const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export default function StaffSchedulePage() {
  const [schedule] = useState<StaffSchedule[]>(mockSchedule);

  return (
    <div>
      <h1 className="text-2xl font-bold">Staff Schedule</h1>
      <p className="mt-2 text-gray-600">Weekly working hours for each dentist</p>

      <div className="mt-6 overflow-x-auto">
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-50">
              <th className="border p-3 text-left text-sm font-medium text-gray-600">
                Dentist
              </th>
              {days.map((day) => (
                <th key={day} className="border p-3 text-center text-sm font-medium text-gray-600">
                  {day}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {schedule.map((staff) => (
              <tr key={staff.id}>
                <td className="border p-3">
                  <p className="font-medium">{staff.name}</p>
                  <p className="text-sm text-gray-500">{staff.specialty}</p>
                </td>
                {days.map((day) => {
                  const daySchedule = staff.schedule.find((s) => s.day === day);
                  return (
                    <td key={day} className="border p-2 text-center">
                      {daySchedule ? (
                        <div className="rounded bg-green-100 p-1">
                          <p className="text-xs font-medium text-green-800">
                            {daySchedule.start}
                          </p>
                          <p className="text-xs text-green-600">{daySchedule.end}</p>
                        </div>
                      ) : (
                        <span className="text-xs text-gray-400">Off</span>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
