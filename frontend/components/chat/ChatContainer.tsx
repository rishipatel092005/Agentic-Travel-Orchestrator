"use client";

import { Bot } from "lucide-react";
import type { ChatMessage } from "@/types";
import MessageBubble from "./MessageBubble";

export default function ChatContainer({
  messages,
}: {
  messages: ChatMessage[];
}) {
  if (messages.length === 0) {
    return (
      <div className="chat-empty">
        <div className="empty-icon">
          <Bot size={23} />
        </div>

        <strong>Your AI travel conversation</strong>
        <span>
          Ask for a trip, then refine it naturally with follow-up requests.
        </span>
      </div>
    );
  }

  return (
    <div className="chat-container">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
    </div>
  );
}