import { marked } from "marked";

export function downloadTripAsPdf(title: string, answer: string) {
  const printWindow = window.open("", "_blank", "width=1200,height=900");
  if (!printWindow) return;

  const safeTitle = title || "Generated travel plan";
  const markdown = answer || "No itinerary content was returned.";
  const renderedAnswer = marked.parse(markdown, { gfm: true, breaks: true });
  const printTitle = `${safeTitle} - Travel Plan`;

  printWindow.document.open();
  printWindow.document.write(`<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${escapeHtml(printTitle)}</title>
    <style>
      @page { size: A4 landscape; margin: 12mm; }
      * { box-sizing: border-box; }
      html, body { margin: 0; padding: 0; background: #fff; color: #111; }
      body { font-family: Arial, "Noto Sans", sans-serif; font-size: 11pt; line-height: 1.55; }
      .document { width: 100%; }
      .document-header { border-bottom: 2px solid #1f5f88; margin-bottom: 18px; padding-bottom: 10px; }
      .document-title { color: #123b5b; font-size: 20pt; font-weight: 700; margin: 0; }
      .document-subtitle { color: #4f6474; font-size: 9pt; margin-top: 3px; }
      h1, h2, h3, h4 { color: #123b5b; break-after: avoid; line-height: 1.2; margin: 20px 0 8px; }
      h1 { font-size: 17pt; } h2 { font-size: 15pt; } h3 { font-size: 13pt; } h4 { font-size: 11pt; }
      p { margin: 0 0 10px; }
      ul, ol { margin: 8px 0 14px; padding-left: 24px; }
      li { margin: 4px 0; }
      strong { color: #0b2f4a; }
      hr { border: 0; border-top: 1px solid #9bb4c4; margin: 18px 0; }
      .table-wrap { overflow: visible; width: 100%; }
      table { border-collapse: collapse; break-inside: auto; margin: 12px 0 18px; table-layout: auto; width: 100%; }
      thead { display: table-header-group; }
      tr { break-inside: avoid; page-break-inside: avoid; }
      th, td { border: 1px solid #718596; color: #111; padding: 7px 8px; text-align: left; vertical-align: top; overflow-wrap: anywhere; }
      th { background: #dceefa; color: #123b5b; font-weight: 700; }
      td { background: #fff; }
      code { background: #eef3f6; padding: 1px 4px; }
      a { color: #0b5d8d; }
      @media print { .document { width: 100%; } }
    </style>
  </head>
  <body>
    <main class="document">
      <header class="document-header">
        <h1 class="document-title">Agentic Travel Orchestrator</h1>
        <div class="document-subtitle">${escapeHtml(safeTitle)} · Complete travel itinerary</div>
      </header>
      <section>${renderedAnswer}</section>
    </main>
  </body>
</html>`);
  printWindow.document.close();
  printWindow.focus();
  printWindow.setTimeout(() => {
    printWindow.print();
    printWindow.setTimeout(() => printWindow.close(), 500);
  }, 300);
}

function escapeHtml(value: string) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

export async function copyTripText(text: string): Promise<boolean> {
  if (!navigator?.clipboard) return false;

  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    return false;
  }
}

