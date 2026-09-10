import Link from "next/link";
import { SignedIn, SignedOut } from "@clerk/nextjs";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl items-center justify-between text-center">
        <h1 className="text-5xl font-bold tracking-tight text-primary-600">
          DentalOS
        </h1>
        <p className="mt-4 text-xl text-gray-600">
          AI-Powered Dental Clinic Platform
        </p>
        <p className="mt-2 text-gray-500">
          Automated booking, patient communication, and clinic management
        </p>

        <div className="mt-10 flex gap-4 justify-center">
          <SignedOut>
            <Link
              href="/sign-in"
              className="rounded-lg bg-primary-600 px-6 py-3 text-white font-medium hover:bg-primary-700 transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/sign-up"
              className="rounded-lg border border-primary-600 px-6 py-3 text-primary-600 font-medium hover:bg-primary-50 transition-colors"
            >
              Get Started
            </Link>
          </SignedOut>
          <SignedIn>
            <Link
              href="/dashboard"
              className="rounded-lg bg-primary-600 px-6 py-3 text-white font-medium hover:bg-primary-700 transition-colors"
            >
              Go to Dashboard
            </Link>
          </SignedIn>
        </div>
      </div>
    </main>
  );
}
