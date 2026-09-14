import { CloudSun } from "lucide-react";

export default function WeatherCard({
  temperature,
  condition,
}: {
  temperature?: number;
  condition?: string;
}) {
  return (
    <div className="info-card">
      <div className="info-icon">
        <CloudSun size={17} />
      </div>

      <div>
        <span className="info-label">Weather</span>
        <strong>
          {typeof temperature === "number"
            ? `${temperature}°`
            : "Available from agent"}
        </strong>

        <small>{condition || "See generated travel plan"}</small>
      </div>
    </div>
  );
}
