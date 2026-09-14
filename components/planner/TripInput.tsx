"use client";

import { Send } from "lucide-react";
import { FormEvent, useState } from "react";

interface TripInputProps {
  onSubmit: (value: string) => void;
  loading?: boolean;
}

export default function TripInput({
  onSubmit,
  loading = false,
}: TripInputProps) {
  const [value, setValue] = useState("");

  function submit(event: FormEvent) {
    event.preventDefault();

    const cleaned = value.trim();

    if (!cleaned || loading) return;

    onSubmit(cleaned);
    setValue("");
  }

  return (
    <div className="planner-panel">
      <div className="planner-heading">
        <span>Start with a trip request</span>
        <span className="planner-hint">
          Destination · budget · duration · preferences
        </span>
      </div>

      <form className="trip-input-wrapper" onSubmit={submit}>
        <textarea
          value={value}
          onChange={(event) => setValue(event.target.value)}
          placeholder="Example: Plan a 5-day Goa trip for 2 people under ₹60,000 with beaches, food and less travel..."
          rows={4}
          disabled={loading}
        />

        <button
          type="submit"
          className="send-button"
          disabled={loading || !value.trim()}
          aria-label="Generate trip"
        >
          <Send size={18} />
        </button>
      </form>

    </div>
  );
}