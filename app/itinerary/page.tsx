"use client";

import { useRouter } from "next/navigation";
import { ItineraryView } from "@/components/ItineraryView";

export default function ItineraryPage() {
  const router = useRouter();
  return <main className="min-h-screen bg-[var(--background)] p-6 sm:p-10"><ItineraryView onBudget={() => router.push("/budget")} onChat={() => router.push("/assistant")} /></main>;
}
