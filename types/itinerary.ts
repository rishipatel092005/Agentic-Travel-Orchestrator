export interface BudgetSummary {
  total?: number;
  budget?: number;
  remaining?: number;
  currency?: string;
  withinBudget?: boolean;
}

export interface WeatherInfo {
  temperature?: number;
  condition?: string;
  description?: string;
}

export interface Place {
  id: string;
  name: string;
  description?: string;
  location?: string;
}

export interface ActivityItem {
  id: string;
  title: string;
  time?: string;
  location?: string;
  cost?: number;
}

export interface DayPlanItem {
  id: string;
  day: number;
  label: string;
  activities: ActivityItem[];
}

export interface ItinerarySummary {
  id: string;
  destination: string;
  days: DayPlanItem[];
  totalBudget?: number;
}
