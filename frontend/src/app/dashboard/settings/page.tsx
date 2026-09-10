"use client";

import { useState } from "react";

export default function SettingsPage() {
  const [clinicName, setClinicName] = useState("Smile Dental Clinic");
  const [phone, setPhone] = useState("+923001234567");
  const [address, setAddress] = useState("123 Main Street, Lahore");
  const [whatsappNumber, setWhatsappNumber] = useState("+923001234567");

  return (
    <div>
      <h1 className="text-2xl font-bold">Clinic Settings</h1>
      <p className="mt-2 text-gray-600">Manage your clinic profile and configuration</p>

      <div className="mt-6 max-w-2xl space-y-6">
        <div className="rounded-lg border p-6">
          <h2 className="text-lg font-semibold">Clinic Profile</h2>
          <div className="mt-4 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Clinic Name
              </label>
              <input
                type="text"
                value={clinicName}
                onChange={(e) => setClinicName(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Phone
              </label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Address
              </label>
              <textarea
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                rows={2}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                WhatsApp Number
              </label>
              <input
                type="tel"
                value={whatsappNumber}
                onChange={(e) => setWhatsappNumber(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500"
              />
            </div>
          </div>
          <button className="mt-4 rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700">
            Save Changes
          </button>
        </div>

        <div className="rounded-lg border p-6">
          <h2 className="text-lg font-semibold">Danger Zone</h2>
          <p className="mt-2 text-sm text-gray-600">
            Permanently delete your clinic and all associated data.
          </p>
          <button className="mt-4 rounded-lg border border-red-600 px-4 py-2 text-red-600 hover:bg-red-50">
            Delete Clinic
          </button>
        </div>
      </div>
    </div>
  );
}
