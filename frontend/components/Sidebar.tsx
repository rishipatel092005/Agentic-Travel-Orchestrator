"use client";

import { BarChart3, Compass, LayoutDashboard, Map, MessageSquareText, Plus, Settings2, Sparkles } from "lucide-react";

const items = [
  { label: "Overview", icon: LayoutDashboard },
  { label: "Plan a trip", icon: Plus },
  { label: "My itineraries", icon: Map },
  { label: "Budget insights", icon: BarChart3 },
  { label: "Trip assistant", icon: MessageSquareText },
];

export function Sidebar({ active, onNavigate }: { active: string; onNavigate: (label: string) => void }) {
  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-slate-200/80 bg-white px-4 py-6 dark:border-slate-800 dark:bg-slate-950 lg:flex">
      <div className="mb-10 flex items-center gap-3 px-3">
        <div className="grid size-10 place-items-center rounded-xl bg-blue-600 text-white shadow-lg shadow-blue-600/20"><Compass size={21} /></div>
        <div><p className="text-[15px] font-bold tracking-tight">Agentic Travel</p><p className="text-[11px] font-medium text-slate-400">OPTIMIZER & PLANNER</p></div>
      </div>
      <div className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-400">Workspace</div>
      <nav className="space-y-1">
        {items.map(({ label, icon: Icon }) => <button key={label} onClick={() => onNavigate(label)} className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${active === label ? "bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-300" : "text-slate-500 hover:bg-slate-50 hover:text-slate-900 dark:hover:bg-slate-900 dark:hover:text-white"}`}><Icon size={17} strokeWidth={active === label ? 2.4 : 1.8} />{label}</button>)}
      </nav>
      <div className="mt-auto space-y-4">
        <div className="overflow-hidden rounded-2xl border border-blue-100 bg-gradient-to-br from-blue-50 via-white to-cyan-50 p-4 dark:border-blue-900/50 dark:from-blue-950/60 dark:via-slate-950 dark:to-cyan-950/40"><Sparkles className="mb-8 text-blue-600 dark:text-blue-300" size={18} /><p className="text-sm font-semibold">Powered by intelligent planning</p><p className="mt-1 text-xs leading-5 text-slate-500 dark:text-slate-400">LangGraph orchestration, live travel data, and deterministic budget logic.</p><div className="mt-4 flex gap-1.5"><span className="rounded-md bg-white px-2 py-1 text-[10px] font-bold text-blue-700 shadow-sm dark:bg-slate-900 dark:text-blue-300">LangGraph</span><span className="rounded-md bg-white px-2 py-1 text-[10px] font-bold text-slate-500 shadow-sm dark:bg-slate-900">APIs</span></div></div>
        <button className="flex w-full items-center gap-3 px-3 py-2 text-sm font-medium text-slate-500 transition hover:text-slate-900 dark:hover:text-white"><Settings2 size={17} />Settings</button>
      </div>
    </aside>
  );
}
