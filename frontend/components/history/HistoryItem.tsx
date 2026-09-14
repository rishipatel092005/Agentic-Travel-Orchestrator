import Link from "next/link";
import { ArrowUpRight, Trash2 } from "lucide-react";
import type { TripRecord } from "@/types";

export default function HistoryItem({
  trip,
  onDelete,
}: {
  trip: TripRecord;
  onDelete: (id: string) => void;
}) {
  return (
    <div className="history-card">
      <Link href={`/trip/${trip.id}`} className="history-card-link">
        <div>
          <strong>{trip.title}</strong>

          <span>
            {new Date(trip.createdAt).toLocaleDateString("en-IN")}
          </span>
        </div>

        <ArrowUpRight size={17} />
      </Link>
      <button
        type="button"
        className="history-delete-button history-delete-button-large"
        aria-label={`Delete ${trip.title}`}
        title="Delete trip"
        onClick={() => onDelete(trip.id)}
      >
        <Trash2 size={15} />
      </button>
    </div>
  );
}