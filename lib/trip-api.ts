import { queryTravelAgent } from "./api";

const planningAccuracyRules = `
Budget accuracy rules:
- Calculate every cost from the numbers shown in the formula.
- Verify multiplication and addition before answering.
- Never change units or add an extra zero.
- Show the formula and the resulting amount for each budget row.
- Make the category totals add up exactly to the grand total.
- Use Indian numbering for INR, for example ₹40,000 and ₹1,30,000.
- Always return Trip Summary and Budget Breakdown as markdown tables with Item, Details, Cost, and Notes columns where applicable.
- When asked to make a plan cheaper, return the full revised itinerary and full revised budget table, not only a suggestion.
- Recalculate every changed row and the grand total after reducing costs.
`;

export async function generateTrip(question: string) {
  return queryTravelAgent({
    question: `${question}\n\n${planningAccuracyRules}`,
  });
}

export async function optimizeTrip(
  originalQuestion: string,
  instruction: string,
  currentAnswer?: string
) {
  const combinedQuestion = `Revise the existing travel itinerary according to this instruction: ${instruction}

Do not ask for the destination, dates, budget, or preferences again. Return the complete revised itinerary, keeping all useful original details and clearly applying the requested change.

${planningAccuracyRules}

Original trip request:
${originalQuestion}

Current itinerary to revise:
${currentAnswer || "No previous itinerary text is available."}`;

  return queryTravelAgent({
    question: combinedQuestion,
  });
}