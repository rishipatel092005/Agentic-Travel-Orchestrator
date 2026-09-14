"use client";

import Link from "next/link";
import {
  Compass,
  History,
  Home,
  Plus,
  Settings,
  Sparkles,
  Trash2,
} from "lucide-react";
import type { TripRecord } from "@/types";

interface SidebarProps {
  history: TripRecord[];
  onNewTrip: () => void;
  onDeleteTrip: (id: string) => void;
}

export default function Sidebar({ history, onNewTrip, onDeleteTrip }: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <Sparkles size={19} />
        </div>

        <div>
          <div className="brand-name">Travel Orchestrator</div>
          <div className="brand-subtitle">AI Travel Intelligence</div>
        </div>
      </div>

      <button className="new-trip-button" onClick={onNewTrip}>
        <Plus size={17} />
        New Trip
      </button>

      <nav className="sidebar-nav">
        <Link href="/" className="sidebar-link active">
          <Home size={17} />
          Home
        </Link>

        <Link href="/history" className="sidebar-link">
          <History size={17} />
          My Trips
        </Link>

        <div className="sidebar-link">
          <Compass size={17} />
          Explore
        </div>

        <Link href="/settings" className="sidebar-link">
          <Settings size={17} />
          Settings
        </Link>
      </nav>

      <div className="sidebar-section">
        <div className="sidebar-section-title">Recent Trips</div>

        {history.length === 0 ? (
          <div className="sidebar-empty">No trips yet</div>
        ) : (
          history.slice(0, 5).map((trip) => (
            <div key={trip.id} className="history-link-row">
              <Link href={`/trip/${trip.id}`} className="history-link">
                {trip.title}
              </Link>
              <button
                type="button"
                className="history-delete-button"
                aria-label={`Delete ${trip.title}`}
                title="Delete trip"
                onClick={() => onDeleteTrip(trip.id)}
              >
                <Trash2 size={13} />
              </button>
            </div>
          ))
        )}
      </div>

      <div className="sidebar-footer">
        <div className="status-dot" />
        <span>AI system ready</span>
      </div>
    </aside>
  );
}