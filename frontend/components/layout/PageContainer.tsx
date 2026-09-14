import { ReactNode } from "react";

export default function PageContainer({
  children,
}: {
  children: ReactNode;
}) {
  return <main className="page-container">{children}</main>;
}
