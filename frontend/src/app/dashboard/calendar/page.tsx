"use client";

import { useState, useEffect } from "react";
import { apiRequest, Appointment } from "@/lib/api";

export default function CalendarPage() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  useEffect(() => {
    loadAppointments();
  }, []);

  const loadAppointments = async () => {
    try {
      const data = await apiRequest<Appointment[]>("/api/appointments/?clinic_id=1");
      setAppointments(data);
    } catch {
      setAppointments([]);
    }
  };

  const daysInMonth = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth() + 1,
    0
  ).getDate();

  const firstDay = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth(),
    1
  ).getDay();

  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  const getAppointmentsForDay = (day: number) => {
    const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    return appointments.filter((apt) => apt.start_time.startsWith(dateStr));
  };

  const prevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
  };

  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
  };

  const statusColors: Record<string, string> = {
    pending: "bg-yellow-100 border-yellow-300",
    confirmed: "bg-green-100 border-green-300",
    completed: "bg-blue-100 border-blue-300",
    cancelled: "bg-red-100 border-red-300",
  };

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Calendar</h1>
        <div className="flex items-center gap-4">
          <button onClick={prevMonth} className="rounded-lg border px-3 py-1 hover:bg-gray-50">
            Previous
          </button>
          <span className="font-semibold">
            {currentDate.toLocaleString("default", { month: "long", year: "numeric" })}
          </span>
          <button onClick={nextMonth} className="rounded-lg border px-3 py-1 hover:bg-gray-50">
            Next
          </button>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-7 gap-px bg-gray-200 rounded-lg overflow-hidden">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
          <div key={day} className="bg-gray-50 p-2 text-center text-sm font-medium text-gray-600">
            {day}
          </div>
        ))}

        {Array.from({ length: firstDay }).map((_, i) => (
          <div key={`empty-${i}`} className="bg-white p-2 min-h-[100px]" />
        ))}

        {days.map((day) => {
          const dayAppts = getAppointmentsForDay(day);
          const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
          const isSelected = selectedDate === dateStr;
          const isToday =
            new Date().getDate() === day &&
            new Date().getMonth() === currentDate.getMonth() &&
            new Date().getFullYear() === currentDate.getFullYear();

          return (
            <div
              key={day}
              onClick={() => setSelectedDate(dateStr)}
              className={`bg-white p-2 min-h-[100px] cursor-pointer hover:bg-gray-50 ${
                isSelected ? "ring-2 ring-primary-500" : ""
              }`}
            >
              <div className={`text-sm font-medium ${isToday ? "text-primary-600" : ""}`}>
                {day}
              </div>
              <div className="mt-1 space-y-1">
                {dayAppts.slice(0, 3).map((apt) => (
                  <div
                    key={apt.id}
                    className={`text-xs p-1 rounded border ${statusColors[apt.status] || "bg-gray-100"}`}
                  >
                    {new Date(apt.start_time).toLocaleTimeString("en-US", {
                      hour: "numeric",
                      minute: "2-digit",
                    })}
                  </div>
                ))}
                {dayAppts.length > 3 && (
                  <div className="text-xs text-gray-500">+{dayAppts.length - 3} more</div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {selectedDate && (
        <div className="mt-6 rounded-lg border p-4">
          <h2 className="font-semibold">
            Appointments for{" "}
            {new Date(selectedDate).toLocaleDateString("en-US", {
              weekday: "long",
              month: "long",
              day: "numeric",
            })}
          </h2>
          <div className="mt-3 space-y-2">
            {getAppointmentsForDay(parseInt(selectedDate.split("-")[2])).length === 0 ? (
              <p className="text-gray-500">No appointments scheduled</p>
            ) : (
              getAppointmentsForDay(parseInt(selectedDate.split("-")[2])).map((apt) => (
                <div key={apt.id} className="flex items-center justify-between rounded-lg border p-3">
                  <div>
                    <p className="font-medium">{apt.patient_id}</p>
                    <p className="text-sm text-gray-500">
                      {new Date(apt.start_time).toLocaleTimeString("en-US", {
                        hour: "numeric",
                        minute: "2-digit",
                      })}{" "}
                      -{" "}
                      {new Date(apt.end_time).toLocaleTimeString("en-US", {
                        hour: "numeric",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                  <span
                    className={`rounded-full px-2 py-1 text-xs font-semibold ${
                      apt.status === "confirmed"
                        ? "bg-green-100 text-green-800"
                        : apt.status === "pending"
                        ? "bg-yellow-100 text-yellow-800"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {apt.status}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
