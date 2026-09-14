export type Trip = {
  id: string;
  destination: string;
  dates: string;
  days: number;
  travelers: number;
  budget: number;
  spent: number;
  status: "Planning" | "Ready";
  cover: string;
};

export type Activity = {
  time: string;
  title: string;
  location: string;
  description: string;
  cost: number;
  icon: "sun" | "food" | "walk" | "museum" | "moon";
};

export type DayPlan = {
  day: number;
  date: string;
  label: string;
  activities: Activity[];
};

export type PlanOption = {
  name: string;
  style: string;
  base: string;
  total: number;
  daily: number;
  weather: string;
  accent: "blue" | "mint";
};

export interface TripRequest {
  destination?: string;
  days?: number;
  people?: number;
  budget?: number;
  preferences?: string[];
  question: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export interface TripRecord {
  id: string;
  title: string;
  question: string;
  answer: string;
  createdAt: string;
}

export interface AgentStatusItem {
  id: string;
  label: string;
  status: "pending" | "active" | "complete";
}