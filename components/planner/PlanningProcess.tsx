import { Brain, Calculator, CloudSun, MapPinned } from "lucide-react";

export default function PlanningProcess() {
  const items = [
    {
      icon: Brain,
      title: "Agent reasoning",
      text: "LangGraph coordinates the planning workflow.",
    },
    {
      icon: MapPinned,
      title: "Travel research",
      text: "Travel tools provide destination information.",
    },
    {
      icon: CloudSun,
      title: "Weather awareness",
      text: "Weather data can influence itinerary decisions.",
    },
    {
      icon: Calculator,
      title: "Budget validation",
      text: "Cost calculations remain separate from LLM reasoning.",
    },
  ];

  return (
    <div className="process-grid">
      {items.map(({ icon: Icon, title, text }) => (
        <div className="process-card" key={title}>
          <div className="process-icon">
            <Icon size={17} />
          </div>

          <div>
            <strong>{title}</strong>
            <p>{text}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
