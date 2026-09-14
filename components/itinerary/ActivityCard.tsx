import { ReactNode } from "react";

export default function DayCard({
  day,
  children,
}: {
  day: number;
  children: ReactNode;
}) {
  return (
    <section className="day-card">
      <div className="day-number">DAY {day}</div>
      <div>{children}</div>
    </section>
  );
}
