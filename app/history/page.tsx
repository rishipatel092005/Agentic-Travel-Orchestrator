"use client";

import Link from "next/link";
import { ArrowLeft, Trash2 } from "lucide-react";
import HistoryList from "@/components/history/HistoryList";
import { useHistory } from "@/hooks/useHistory";
import Button from "@/components/common/Button";

export default function HistoryPage() {
  const { history, clearHistory, removeTrip } = useHistory();

  return (
    <div className="simple-page">
      <div className="simple-page-inner">
        <div className="page-header">
          <div>
            <Link href="/" className="back-link">
              <ArrowLeft size={16} />
              Back
            </Link>

            <h1>Trip History</h1>
            <p>Your recently generated travel plans.</p>
          </div>

          {history.length > 0 && (
            <Button variant="secondary" onClick={clearHistory}>
              <Trash2 size={15} />
              Clear history
            </Button>
          )}
        </div>

        <HistoryList history={history} onDelete={removeTrip} />
      </div>
    </div>
  );
}