import type { ChatMessage } from "@/types";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";

export default function MessageBubble({
  message,
}: {
  message: ChatMessage;
}) {
  const isUser = message.role === "user";

  return (
    <div className={`message-row ${isUser ? "message-user" : ""}`}>
      <div className={`message-bubble ${isUser ? "user-bubble" : "ai-bubble"}`}>
        {!isUser && <div className="message-label">Travel AI</div>}
        <div className="message-content">
          <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
            {message.content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}