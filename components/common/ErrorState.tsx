import { AlertCircle } from "lucide-react";

export default function ErrorState({ message }: { message: string }) {
  return (
    <div className="error-state">
      <AlertCircle size={20} />
      <div>
        <strong>Something went wrong</strong>
        <p>{message}</p>
      </div>
    </div>
  );
}
