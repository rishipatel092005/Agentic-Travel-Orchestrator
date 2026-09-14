import { ShieldCheck } from "lucide-react";

export default function Navbar() {
  return (
    <header className="navbar">
      <div>
        <div className="navbar-kicker">AI TRAVEL ASSISTANT</div>
        <div className="navbar-title">Agentic Travel Orchestrator</div>
      </div>

      <div className="navbar-status">
        <ShieldCheck size={15} />
        Constraint-aware planning
      </div>
    </header>
  );
}
