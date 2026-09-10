import { ChatWidget } from "@/components/chat-widget";

export default async function ClinicPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white p-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900">
          Welcome to Our Clinic
        </h1>
        <p className="mt-4 text-lg text-gray-600">
          Chat with our AI assistant to book appointments, ask questions, or
          get information about our services.
        </p>
      </div>

      <ChatWidget clinicSlug={slug} />
    </main>
  );
}
