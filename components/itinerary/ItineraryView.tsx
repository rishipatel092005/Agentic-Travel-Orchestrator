"use client";

import {
  Check,
  Copy,
  Download,
} from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import { copyTripText, downloadTripAsPdf } from "@/lib/download";
import Button from "@/components/common/Button";

interface ItineraryViewProps {
  answer: string;
  destination?: string;
}
import type { ReactNode } from "react";

const markdownComponents = {
  h1: ({ children }: { children?: ReactNode }) => <h2 className="answer-heading">{children}</h2>,
  h2: ({ children }: { children?: ReactNode }) => <h2 className="answer-heading">{children}</h2>,
  h3: ({ children }: { children?: ReactNode }) => <h3 className="answer-heading">{children}</h3>,
  p: ({ children }: { children?: ReactNode }) => <p className="answer-paragraph">{children}</p>,
  ul: ({ children }: { children?: ReactNode }) => <ul className="answer-list">{children}</ul>,
  ol: ({ children }: { children?: ReactNode }) => <ol className="answer-list">{children}</ol>,
  table: ({ children }: { children?: ReactNode }) => (
    <div className="answer-table-wrap">
      <table className="answer-table">{children}</table>
    </div>
  ),
  hr: () => <hr className="answer-separator" />,
};

export default function ItineraryView({
  answer,
  destination,
}: ItineraryViewProps) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    const success = await copyTripText(answer);

    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    }
  }

  return (
    <section className="itinerary-section">
      <div className="result-header">
        <div>
          <div className="result-kicker">GENERATED TRAVEL PLAN</div>
          <h2>{destination || "Your personalized itinerary"}</h2>
        </div>

        <div className="result-actions">
          <Button variant="secondary" onClick={handleCopy}>
            {copied ? <Check size={15} /> : <Copy size={15} />}
            {copied ? "Copied" : "Copy"}
          </Button>

          <Button
            variant="secondary"
            onClick={() => downloadTripAsPdf(destination || "travel-plan", answer)}
          >
            <Download size={15} />
            PDF
          </Button>
        </div>
      </div>

      <article className="final-answer printable-trip">
        <div className="print-document-title">Agentic Travel Orchestrator</div>
        <div className="print-document-subtitle">Generated travel plan</div>
        <div className="answer-markdown">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
            components={markdownComponents}
          >
            {answer}
          </ReactMarkdown>
        </div>
      </article>
    </section>
  );
}
