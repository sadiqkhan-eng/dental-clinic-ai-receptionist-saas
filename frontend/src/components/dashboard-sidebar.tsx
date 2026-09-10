"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { SignOutButton } from "@clerk/nextjs";
import {
  Calendar,
  Users,
  MessageSquare,
  Settings,
  LayoutDashboard,
  Stethoscope,
  BarChart3,
  Clock,
  Radio,
  CalendarDays,
  Brain,
} from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/dashboard/appointments", label: "Appointments", icon: Calendar },
  { href: "/dashboard/calendar", label: "Calendar", icon: CalendarDays },
  { href: "/dashboard/patients", label: "Patients", icon: Users },
  { href: "/dashboard/services", label: "Services", icon: Stethoscope },
  { href: "/dashboard/staff-schedule", label: "Staff Schedule", icon: Clock },
  { href: "/dashboard/conversations", label: "Conversations", icon: MessageSquare },
  { href: "/dashboard/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/dashboard/broadcast", label: "Broadcast", icon: Radio },
  { href: "/dashboard/training", label: "AI Training", icon: Brain },
  { href: "/dashboard/settings", label: "Settings", icon: Settings },
];

export function DashboardSidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-64 flex-col border-r bg-gray-50">
      <div className="p-4">
        <h2 className="text-lg font-bold text-primary-600">DentalOS</h2>
      </div>

      <nav className="flex-1 space-y-1 px-3 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-primary-100 text-primary-700"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              }`}
            >
              <item.icon className="h-5 w-5" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t p-4">
        <SignOutButton>
          <button className="w-full rounded-lg px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100">
            Sign Out
          </button>
        </SignOutButton>
      </div>
    </aside>
  );
}
