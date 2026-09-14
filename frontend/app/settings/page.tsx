"use client";

import Link from "next/link";
import { ArrowLeft, Check, Moon } from "lucide-react";
import { useTheme } from "next-themes";
import { useState } from "react";

const appearanceOptions = [
  { value: "dark", label: "Dark blue", icon: Moon },
] as const;

export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const [currency, setCurrency] = useState("INR");
  const [units, setUnits] = useState("kilometers");

  return (
    <div className="simple-page">
      <div className="simple-page-inner">
        <Link href="/" className="back-link">
          <ArrowLeft size={16} />
          Back
        </Link>

        <div className="page-header">
          <div>
            <h1>Settings</h1>
            <p>Keep your travel planning workspace comfortable and useful.</p>
          </div>
        </div>

        <div className="settings-grid">
          <section className="settings-card settings-card-wide">
            <div className="settings-card-heading">
              <div>
                <span>Appearance</span>
                <strong>Choose your workspace theme</strong>
              </div>
              <span className="settings-status">{theme || "dark"}</span>
            </div>
            <div className="appearance-options" role="group" aria-label="Theme preference">
              {appearanceOptions.map(({ value, label, icon: Icon }) => (
                <button
                  key={value}
                  type="button"
                  className={`appearance-option ${theme === value ? "selected" : ""}`}
                  onClick={() => setTheme(value)}
                  aria-pressed={theme === value}
                >
                  <Icon size={17} />
                  <span>{label}</span>
                  {theme === value && <Check size={15} />}
                </button>
              ))}
            </div>
          </section>

          <section className="settings-card">
            <span>Currency</span>
            <strong>Budget display</strong>
            <select value={currency} onChange={(event) => setCurrency(event.target.value)}>
              <option value="INR">Indian Rupee (INR)</option>
              <option value="USD">US Dollar (USD)</option>
              <option value="EUR">Euro (EUR)</option>
              <option value="GBP">Pound Sterling (GBP)</option>
            </select>
          </section>

          <section className="settings-card">
            <span>Distance</span>
            <strong>Route measurements</strong>
            <select value={units} onChange={(event) => setUnits(event.target.value)}>
              <option value="kilometers">Kilometers</option>
              <option value="miles">Miles</option>
            </select>
          </section>

          <section className="settings-card">
            <span>Planning style</span>
            <strong>Preference-aware itineraries</strong>
            <p>Budget, weather, places, and travel time stay visible in generated plans.</p>
          </section>

          <section className="settings-card">
            <span>Connected services</span>
            <strong>Travel intelligence</strong>
            <p>FastAPI, LangGraph, Groq, and MongoDB power the planning workflow.</p>
          </section>
        </div>
      </div>
    </div>
  );
}
