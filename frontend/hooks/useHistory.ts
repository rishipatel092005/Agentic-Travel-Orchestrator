"use client";

import { useCallback, useEffect, useState } from "react";
import type { TripRecord } from "@/types";

const STORAGE_KEY = "agentic-travel-history";
const MAX_ITEMS = 10;

export function useHistory() {
  const [history, setHistory] = useState<TripRecord[]>([]);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);

      if (stored) {
        setHistory(JSON.parse(stored) as TripRecord[]);
      }
    } catch {
      setHistory([]);
    }
  }, []);

  const saveTrip = useCallback((trip: TripRecord) => {
    setHistory((current) => {
      const next = [trip, ...current.filter((item) => item.id !== trip.id)].slice(
        0,
        MAX_ITEMS
      );

      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  const removeTrip = useCallback((id: string) => {
    setHistory((current) => {
      const next = current.filter((item) => item.id !== id);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  const clearHistory = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setHistory([]);
  }, []);

  return {
    history,
    saveTrip,
    removeTrip,
    clearHistory,
  };
}
