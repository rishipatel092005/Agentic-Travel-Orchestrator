import { MapPin } from "lucide-react";
import type { Activity } from "@/types";

export default function ActivityCard({
  activity,
}: {
  activity: Activity;
}) {
  return (
    <div className="activity-card">
      <div className="activity-top">
        <strong>{activity.title}</strong>

        {typeof activity.cost === "number" && (
          <span>₹{activity.cost.toLocaleString("en-IN")}</span>
        )}
      </div>

      {activity.description && <p>{activity.description}</p>}

      {activity.location && (
        <div className="activity-meta">
          <MapPin size={14} />
          {activity.location}
        </div>
      )}
    </div>
  );
}
