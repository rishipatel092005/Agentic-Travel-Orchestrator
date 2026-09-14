"use client";

import Link from "next/link";
import { History, Home, Plus } from "lucide-react";

export default function MobileNav({ onNewTrip }: { onNewTrip: () => void }) {
  return (
    <div className="mobile-nav">
      <Link href="/">
        <Home size={18} />
        Home
      </Link>

      <button onClick={onNewTrip}>
        <Plus size={18} />
        New
      </button>

      <Link href="/history">
        <History size={18} />
        Trips
      </Link>
    </div>
  );
}