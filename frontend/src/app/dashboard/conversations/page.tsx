"use client";

import { useState } from "react";

interface Conversation {
  id: string;
  patient_name: string;
  channel: "whatsapp" | "web";
  last_message: string;
  last_message_at: string;
  status: "active" | "resolved";
}

const mockConversations: Conversation[] = [
  { id: "1", patient_name: "Ahmed Khan", channel: "whatsapp", last_message: "Can I book a checkup for tomorrow?", last_message_at: "10:30", status: "active" },
  { id: "2", patient_name: "Fatima Ali", channel: "web", last_message: "What are your prices for cleaning?", last_message_at: "09:15", status: "active" },
  { id: "3", patient_name: "Hassan Raza", channel: "whatsapp", last_message: "I need to reschedule my appointment", last_message_at: "Yesterday", status: "resolved" },
];

const channelColors: Record<string, string> = {
  whatsapp: "bg-green-100 text-green-800",
  web: "bg-blue-100 text-blue-800",
};

export default function ConversationsPage() {
  const [conversations] = useState<Conversation[]>(mockConversations);

  return (
    <div>
      <h1 className="text-2xl font-bold">AI Conversations</h1>
      <p className="mt-2 text-gray-600">
        Patient conversations handled by the AI receptionist
      </p>

      <div className="mt-6 space-y-4">
        {conversations.map((conv) => (
          <div
            key={conv.id}
            className="flex items-center justify-between rounded-lg border p-4 hover:bg-gray-50"
          >
            <div className="flex items-center gap-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-primary-600">
                {conv.patient_name.charAt(0)}
              </div>
              <div>
                <p className="font-medium">{conv.patient_name}</p>
                <p className="text-sm text-gray-500">{conv.last_message}</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className={`inline-flex rounded-full px-2 py-1 text-xs font-semibold ${channelColors[conv.channel]}`}>
                {conv.channel}
              </span>
              <span className="text-sm text-gray-500">{conv.last_message_at}</span>
              <span
                className={`inline-flex rounded-full px-2 py-1 text-xs font-semibold ${
                  conv.status === "active"
                    ? "bg-green-100 text-green-800"
                    : "bg-gray-100 text-gray-800"
                }`}
              >
                {conv.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
