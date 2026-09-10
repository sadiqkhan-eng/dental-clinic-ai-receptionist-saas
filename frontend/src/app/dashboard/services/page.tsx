"use client";

import { useState } from "react";

interface Service {
  id: string;
  name: string;
  duration_minutes: number;
  price: number;
  category: string;
}

const mockServices: Service[] = [
  { id: "1", name: "General Checkup", duration_minutes: 30, price: 2000, category: "General" },
  { id: "2", name: "Teeth Cleaning", duration_minutes: 45, price: 3500, category: "Preventive" },
  { id: "3", name: "Root Canal", duration_minutes: 90, price: 15000, category: "Endodontics" },
  { id: "4", name: "Teeth Whitening", duration_minutes: 60, price: 8000, category: "Cosmetic" },
];

export default function ServicesPage() {
  const [services] = useState<Service[]>(mockServices);

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Services</h1>
        <button className="rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700">
          Add Service
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
                Duration
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Price (PKR)
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Category
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {services.map((service) => (
              <tr key={service.id}>
                <td className="whitespace-nowrap px-6 py-4 font-medium">
                  {service.name}
                </td>
                <td className="whitespace-nowrap px-6 py-4">
                  {service.duration_minutes} min
                </td>
                <td className="whitespace-nowrap px-6 py-4">
                  Rs. {service.price.toLocaleString()}
                </td>
                <td className="whitespace-nowrap px-6 py-4">
                  <span className="inline-flex rounded-full bg-blue-100 px-2 py-1 text-xs font-semibold text-blue-800">
                    {service.category}
                  </span>
                </td>
                <td className="whitespace-nowrap px-6 py-4">
                  <button className="text-primary-600 hover:text-primary-800">
                    Edit
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
