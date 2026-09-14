"use client";

import { useCallback, useState } from "react";
import { generateTrip, optimizeTrip } from "@/lib/trip-api";
import type { ChatMessage } from "@/types";

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = useCallback(
    async (content: string, originalQuestion?: string, currentAnswer?: string) => {
      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        content,
        timestamp: new Date().toISOString(),
      };

      setMessages((current) => [...current, userMessage]);
      setLoading(true);

      try {
        const result = originalQuestion
          ? await optimizeTrip(originalQuestion, content, currentAnswer)
          : await generateTrip(content);

        const assistantMessage: ChatMessage = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: result.answer,
          timestamp: new Date().toISOString(),
        };

        setMessages((current) => [...current, assistantMessage]);
        return result;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    messages,
    loading,
    sendMessage,
    setMessages,
    resetMessages: () => setMessages([]),
  };
}
