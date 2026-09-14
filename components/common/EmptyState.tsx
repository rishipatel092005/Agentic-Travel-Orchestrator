import { Compass } from "lucide-react";

export default function EmptyState() {
  return (
    <div className="empty-state">
      <div className="empty-icon">
        <Compass size={28} />
      </div>

      <h2>Plan your next trip</h2>

      <p>
        Tell the travel agent where you want to go, your budget, trip duration,
        and preferences.
      </p>
    </div>
  );
}