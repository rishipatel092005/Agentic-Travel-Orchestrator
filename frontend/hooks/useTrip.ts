"use client";

import { useCallback, useState } from "react";
import { generateTrip, optimizeTrip } from "@/lib/trip-api";
import type { TripRecord } from "@/types";

export function useTrip() {
  const [trip, setTrip] = useState<TripRecord | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generate = useCallback(
    async (question: string, saveTrip?: (trip: TripRecord) => void) => {
      setLoading(true);
      setError("");

      try {
        const result = await generateTrip(question);

        const newTrip: TripRecord = {
          id: crypto.randomUUID(),
          title:
            question.length > 45
              ? `${question.substring(0, 45)}...`
              : question,
          question,
          answer: result.answer,
          createdAt: new Date().toISOString(),
        };

        setTrip(newTrip);
        saveTrip?.(newTrip);

        return newTrip;
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : "Unable to generate the travel plan.";

        setError(message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const optimize = useCallback(
    async (instruction: string, originalQuestion: string) => {
      setLoading(true);
      setError("");

      try {
        const result = await optimizeTrip(originalQuestion, instruction);

        setTrip((current) =>
          current
            ? {
                ...current,
                answer: result.answer,
              }
            : current
        );

        return result.answer;
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : "Unable to update the itinerary.";

        setError(message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    trip,
    loading,
    error,
    generate,
    optimize,
    setTrip,
  };
}
