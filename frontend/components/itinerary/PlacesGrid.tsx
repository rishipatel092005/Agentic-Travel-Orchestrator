import { MapPinned } from "lucide-react";
import type { Place } from "@/types";

export default function PlacesGrid({
  places,
}: {
  places: Place[];
}) {
  return (
    <div className="places-grid">
      {places.map((place) => (
        <div className="place-card" key={place.id}>
          <div className="place-icon">
            <MapPinned size={16} />
          </div>

          <strong>{place.name}</strong>

          {place.location && <span>{place.location}</span>}

          {place.description && <p>{place.description}</p>}
        </div>
      ))}
    </div>
  );
}
