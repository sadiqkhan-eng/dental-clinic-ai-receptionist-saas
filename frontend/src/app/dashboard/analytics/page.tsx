"use client";

import { useState, useEffect } from "react";
import { apiRequest } from "@/lib/api";

interface Summary {
  appointments_today: number;
  total_patients: number;
  total_revenue: number;
}

interface RevenueData {
  month: string;
  revenue: number;
}

interface ServiceCount {
  service: string;
  count: number;
}

interface NoShowData {
  total_appointments: number;
  no_shows: number;
  rate: number;
}

export default function AnalyticsPage() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [revenue, setRevenue] = useState<RevenueData[]>([]);
  const [services, setServices] = useState<ServiceCount[]>([]);
  const [noShow, setNoShow] = useState<NoShowData | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [s, r, sv, ns] = await Promise.all([
        apiRequest<Summary>("/api/analytics/summary?clinic_id=1"),
        apiRequest<RevenueData[]>("/api/analytics/revenue?clinic_id=1"),
        apiRequest<ServiceCount[]>("/api/analytics/appointments-by-service?clinic_id=1"),
        apiRequest<NoShowData>("/api/analytics/no-show-rate?clinic_id=1"),
      ]);
      setSummary(s);
      setRevenue(r);
      setServices(sv);
      setNoShow(ns);
    } catch {
      console.error("Failed to load analytics");
    }
  };

  const maxRevenue = Math.max(...revenue.map((r) => r.revenue), 1);

  return (
    <div>
      <h1 className="text-2xl font-bold">Analytics</h1>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-lg border p-4 shadow-sm">
          <p className="text-sm text-gray-500">Today&apos;s Appointments</p>
          <p className="mt-1 text-3xl font-semibold">{summary?.appointments_today ?? 0}</p>
        </div>
        <div className="rounded-lg border p-4 shadow-sm">
          <p className="text-sm text-gray-500">Total Patients</p>
          <p className="mt-1 text-3xl font-semibold">{summary?.total_patients ?? 0}</p>
        </div>
        <div className="rounded-lg border p-4 shadow-sm">
          <p className="text-sm text-gray-500">Total Revenue</p>
          <p className="mt-1 text-3xl font-semibold">
            Rs. {(summary?.total_revenue ?? 0).toLocaleString()}
          </p>
        </div>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-lg border p-6">
          <h2 className="font-semibold">Revenue Trend</h2>
          <div className="mt-4 space-y-2">
            {revenue.map((r) => (
              <div key={r.month} className="flex items-center gap-4">
                <span className="w-16 text-sm text-gray-600">{r.month.split("-")[1]}</span>
                <div className="flex-1 h-6 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary-500 rounded-full"
                    style={{ width: `${(r.revenue / maxRevenue) * 100}%` }}
                  />
                </div>
                <span className="w-24 text-sm text-right">Rs. {r.revenue.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-lg border p-6">
          <h2 className="font-semibold">Appointments by Service</h2>
          <div className="mt-4 space-y-3">
            {services.map((s) => (
              <div key={s.service} className="flex items-center justify-between">
                <span className="text-sm">{s.service}</span>
                <span className="font-medium">{s.count}</span>
              </div>
            ))}
            {services.length === 0 && (
              <p className="text-sm text-gray-500">No data yet</p>
            )}
          </div>
        </div>

        <div className="rounded-lg border p-6">
          <h2 className="font-semibold">No-Show Rate</h2>
          <div className="mt-4">
            <div className="text-center">
              <p className="text-5xl font-bold text-primary-600">{noShow?.rate ?? 0}%</p>
              <p className="mt-2 text-sm text-gray-500">
                {noShow?.no_shows ?? 0} of {noShow?.total_appointments ?? 0} appointments
              </p>
            </div>
          </div>
        </div>

        <div className="rounded-lg border p-6">
          <h2 className="font-semibold">Insights</h2>
          <div className="mt-4 space-y-3">
            <div className="rounded-lg bg-blue-50 p-3">
              <p className="text-sm font-medium text-blue-800">Peak Hours</p>
              <p className="text-sm text-blue-600">10:00 AM - 12:00 PM has highest bookings</p>
            </div>
            <div className="rounded-lg bg-green-50 p-3">
              <p className="text-sm font-medium text-green-800">Best Day</p>
              <p className="text-sm text-green-600">Tuesday has 40% more appointments</p>
            </div>
            <div className="rounded-lg bg-yellow-50 p-3">
              <p className="text-sm font-medium text-yellow-800">Recall Needed</p>
              <p className="text-sm text-yellow-600">23 patients overdue for checkup</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
