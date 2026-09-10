"use client";

import { useState } from "react";

export default function BroadcastPage() {
  const [message, setMessage] = useState("");
  const [channel, setChannel] = useState<"whatsapp" | "sms" | "email">("whatsapp");
  const [sent, setSent] = useState(false);

  const handleSend = () => {
    if (!message.trim()) return;
    setSent(true);
    setTimeout(() => setSent(false), 3000);
    setMessage("");
  };

  return (
    <div>
      <h1 className="text-2xl font-bold">Broadcast Message</h1>
      <p className="mt-2 text-gray-600">Send bulk messages to all patients</p>

      <div className="mt-6 max-w-2xl space-y-6">
        <div className="rounded-lg border p-6">
          <h2 className="font-semibold">Compose Message</h2>

          <div className="mt-4 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Channel</label>
              <div className="mt-2 flex gap-4">
                {(["whatsapp", "sms", "email"] as const).map((ch) => (
                  <label key={ch} className="flex items-center gap-2">
                    <input
                      type="radio"
                      name="channel"
                      checked={channel === ch}
                      onChange={() => setChannel(ch)}
                      className="text-primary-600"
                    />
                    <span className="capitalize">{ch}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Message</label>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                rows={5}
                placeholder="Type your message here..."
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-primary-500"
              />
              <p className="mt-1 text-sm text-gray-500">{message.length} characters</p>
            </div>

            <div className="rounded-lg bg-blue-50 p-3">
              <p className="text-sm text-blue-800">
                This message will be sent to all patients who have opted in for {channel} notifications.
              </p>
            </div>

            <button
              onClick={handleSend}
              disabled={!message.trim()}
              className="rounded-lg bg-primary-600 px-6 py-2 text-white hover:bg-primary-700 disabled:opacity-50"
            >
              Send Broadcast
            </button>

            {sent && (
              <div className="rounded-lg bg-green-50 p-3">
                <p className="text-sm text-green-800">Message sent successfully!</p>
              </div>
            )}
          </div>
        </div>

        <div className="rounded-lg border p-6">
          <h2 className="font-semibold">Recent Broadcasts</h2>
          <div className="mt-4 space-y-3">
            <div className="flex items-center justify-between rounded-lg bg-gray-50 p-3">
              <div>
                <p className="text-sm font-medium">Holiday Hours Announcement</p>
                <p className="text-xs text-gray-500">Sent via WhatsApp to 142 patients</p>
              </div>
              <span className="text-xs text-gray-500">2 days ago</span>
            </div>
            <div className="flex items-center justify-between rounded-lg bg-gray-50 p-3">
              <div>
                <p className="text-sm font-medium">Free Cleaning Camp</p>
                <p className="text-xs text-gray-500">Sent via SMS to 98 patients</p>
              </div>
              <span className="text-xs text-gray-500">1 week ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
