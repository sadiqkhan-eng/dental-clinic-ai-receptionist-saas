"use client";

import { useState } from "react";
import { apiRequest } from "@/lib/api";

interface TrainingMessage {
  role: string;
  content: string;
}

interface Evaluation {
  score: number;
  feedback: string;
  strengths: string[];
  improvements: string[];
}

export default function TrainingPage() {
  const [clinicName, setClinicName] = useState("Smile Dental Clinic");
  const [scenario, setScenario] = useState("General booking and FAQ");
  const [isRunning, setIsRunning] = useState(false);
  const [conversation, setConversation] = useState<TrainingMessage[]>([]);
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);

  const runSimulation = async () => {
    setIsRunning(true);
    setConversation([]);
    setEvaluation(null);

    try {
      const result = await apiRequest<{ conversation: TrainingMessage[]; evaluation: Evaluation }>(
        "/api/training/evaluate",
        {
          method: "POST",
          body: JSON.stringify({ clinic_name: clinicName, scenario, turns: 8 }),
        }
      );
      setConversation(result.conversation);
      setEvaluation(result.evaluation);
    } catch {
      console.error("Training failed");
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold">AI Training Mode</h1>
      <p className="mt-2 text-gray-600">
        Test your AI assistant with simulated conversations before going live
      </p>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-1">
          <div className="rounded-lg border p-6">
            <h2 className="font-semibold">Configuration</h2>
            <div className="mt-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Clinic Name</label>
                <input
                  type="text"
                  value={clinicName}
                  onChange={(e) => setClinicName(e.target.value)}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Scenario</label>
                <select
                  value={scenario}
                  onChange={(e) => setScenario(e.target.value)}
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                >
                  <option>General booking and FAQ</option>
                  <option>Emergency call handling</option>
                  <option>Price negotiation</option>
                  <option>Complaint handling</option>
                  <option>Multi-language test</option>
                </select>
              </div>
              <button
                onClick={runSimulation}
                disabled={isRunning}
                className="w-full rounded-lg bg-primary-600 px-4 py-2 text-white hover:bg-primary-700 disabled:opacity-50"
              >
                {isRunning ? "Running..." : "Start Simulation"}
              </button>
            </div>
          </div>

          {evaluation && (
            <div className="mt-6 rounded-lg border p-6">
              <h2 className="font-semibold">Evaluation</h2>
              <div className="mt-4">
                <div className="text-center">
                  <p className="text-5xl font-bold text-primary-600">{evaluation.score}%</p>
                  <p className="text-sm text-gray-500">Overall Score</p>
                </div>
                <div className="mt-4 space-y-3">
                  <div>
                    <p className="text-sm font-medium text-green-700">Strengths</p>
                    <ul className="mt-1 space-y-1">
                      {evaluation.strengths.map((s, i) => (
                        <li key={i} className="text-sm text-gray-600">- {s}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-yellow-700">Improvements</p>
                    <ul className="mt-1 space-y-1">
                      {evaluation.improvements.map((s, i) => (
                        <li key={i} className="text-sm text-gray-600">- {s}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="lg:col-span-2">
          <div className="rounded-lg border p-6">
            <h2 className="font-semibold">Conversation</h2>
            <div className="mt-4 space-y-4 max-h-[600px] overflow-y-auto">
              {conversation.length === 0 && (
                <p className="text-gray-500 text-center py-8">
                  Click "Start Simulation" to begin training
                </p>
              )}
              {conversation.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
                      msg.role === "user"
                        ? "bg-blue-100 text-blue-900"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    <p className="text-xs font-medium text-gray-500 mb-1">
                      {msg.role === "user" ? "Test Patient" : "AI Agent"}
                    </p>
                    {msg.content}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
