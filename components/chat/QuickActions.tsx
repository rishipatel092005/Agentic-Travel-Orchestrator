const actions = [
  "Make it cheaper",
  "Reduce travel time",
  "Add more food experiences",
  "Add more adventure",
  "Make it more relaxed",
];

interface QuickActionsProps {
  onSelect: (action: string) => void;
}

export default function QuickActions({
  onSelect,
}: QuickActionsProps) {
  return (
    <div className="quick-actions">
      {actions.map((action) => (
        <button key={action} onClick={() => onSelect(action)}>
          {action}
        </button>
      ))}
    </div>
  );
}
