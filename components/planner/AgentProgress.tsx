"use client";

import {
  Check,
  Circle,
  LoaderCircle,
} from "lucide-react";

const stages = [
  "Understanding requirements",
  "Researching travel information",
  "Checking weather",
  "Calculating budget",
  "Evaluating itinerary",
  "Finalizing plan",
];

export default function AgentProgress({ active }: { active: boolean }) {
  return (
    <div className="agent-progress-card">
      <div className="section-title">
        <span>AI planning process</span>

        {active && (
          <span className="live-badge">
            <span className="live-dot" />
            Processing
          </span>
        )}
      </div>

      <div className="progress-list">
        {stages.map((stage, index) => {
          const complete = !active || index < 2;
          const current = active && index === 2;

          return (
            <div className="progress-item" key={stage}>
              <div className="progress-icon">
                {complete ? (
                  <Check size={14} />
                ) : current ? (
                  <LoaderCircle size={14} className="spin" />
                ) : (
                  <Circle size={12} />
                )}
              </div>

              <span>{stage}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}