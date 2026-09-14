export default function Loading({
  label = "Planning your trip...",
}: {
  label?: string;
}) {
  return (
    <div className="loading-state">
      <div className="loader-ring" />
      <span>{label}</span>
    </div>
  );
}