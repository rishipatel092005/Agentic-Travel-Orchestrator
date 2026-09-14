interface QuickPromptsProps {
  onSelect: (value: string) => void;
}

const prompts = [
  "Plan 5 days in Goa under ₹60,000",
  "Plan a 7-day Japan trip under ₹2 lakh",
  "Plan a relaxed Kerala trip for 4 days",
  "Plan a budget-friendly Bali trip",
];

export default function QuickPrompts({ onSelect }: QuickPromptsProps) {
  return (
    <div className="quick-prompts">
      {prompts.map((prompt) => (
        <button key={prompt} onClick={() => onSelect(prompt)}>
          {prompt}
        </button>
      ))}
    </div>
  );
}