import type { TripRecord } from "@/types";
import HistoryItem from "./HistoryItem";

export default function HistoryList({
  history,
  onDelete,
}: {
  history: TripRecord[];
  onDelete: (id: string) => void;
}) {
  if (history.length === 0) {
    return (
      <div className="empty-state">
        <h2>No saved trips yet</h2>
        <p>Your generated trips will appear here.</p>
      </div>
    );
  }

  return (
    <div className="history-list">
      {history.map((trip) => (
        <HistoryItem key={trip.id} trip={trip} onDelete={onDelete} />
      ))}
    </div>
  );
}