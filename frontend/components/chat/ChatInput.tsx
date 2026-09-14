"use client";

import { FormEvent, useState } from "react";
import { Send } from "lucide-react";

interface ChatInputProps {
  onSend: (message: string) => void | Promise<void>;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [value, setValue] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const cleaned = value.trim();

    if (!cleaned || disabled) return;

    await onSend(cleaned);
    setValue("");
  }

  return (
    <form className="chat-input-wrapper" onSubmit={handleSubmit}>
      <input
        type="text"
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder="Ask follow-up questions..."
        aria-label="Travel assistant input"
        disabled={disabled}
      />

      <button type="submit" disabled={disabled || !value.trim()}>
        <Send size={16} />
      </button>
    </form>
  );
}