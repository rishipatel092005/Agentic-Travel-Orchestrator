"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import ItineraryView from "@/components/itinerary/ItineraryView";
import type { TripRecord } from "@/types";

export default function TripDetailsPage() {
  const params = useParams<{ id: string }>();
  const [trip, setTrip] = useState<TripRecord | null>(null);

  useEffect(() => {
    try {
      const stored = localStorage.getItem("agentic-travel-history");

      if (!stored) return;

      const history = JSON.parse(stored) as TripRecord[];
      const found = history.find((item) => item.id === params.id);

      if (found) {
        setTrip(found);
      }
    } catch {
      setTrip(null);
    }
  }, [params.id]);

  return (
    <div className="simple-page">
      <div className="simple-page-inner">
        <Link href="/" className="back-link">
          <ArrowLeft size={16} />
          Back to planner
        </Link>

        {trip ? (
          <ItineraryView answer={trip.answer} />
        ) : (
          <div className="empty-state">
            <h2>Trip not found</h2>
            <p>This trip may no longer exist in local history.</p>
          </div>
        )}
      </div>
    </div>
  );
}