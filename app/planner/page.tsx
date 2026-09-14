"use client";

import { useRouter } from "next/navigation";
import { PlannerForm } from "@/components/PlannerForm";

export default function PlannerPage() {
  const router = useRouter();
  return <main className="min-h-screen bg-[var(--background)] p-6 sm:p-10"><PlannerForm onCreated={() => router.push("/itinerary")} /></main>;
}
