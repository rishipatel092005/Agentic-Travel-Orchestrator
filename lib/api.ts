import type { QueryRequest, QueryResponse } from "@/types";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

export async function queryTravelAgent(
  payload: QueryRequest,
  signal?: AbortSignal
): Promise<QueryResponse> {
  const response = await fetch(`${API_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
    signal,
    cache: "no-store",
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const data = await response.json();

      if (typeof data?.detail === "string") {
        message = data.detail;
      } else if (typeof data?.message === "string") {
        message = data.message;
      } else if (typeof data?.error === "string") {
        message = data.error;
      }
    } catch {
      // Keep the default message.
    }

    throw new Error(message);
  }

  const data = (await response.json()) as Partial<QueryResponse>;

  const answer =
    typeof data.answer === "string"
      ? data.answer
      : typeof data.content === "string"
        ? data.content
        : "";

  if (!answer.trim()) {
    throw new Error("The backend returned an empty answer.");
  }

  return {
    answer,
    thread_id: data.thread_id,
  };
}

export async function checkBackendHealth(
  signal?: AbortSignal
): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/health`, {
      method: "GET",
      cache: "no-store",
      signal,
    });

    return response.ok;
  } catch {
    return false;
  }
}

export { API_URL };