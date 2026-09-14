"use client";

import { Bell, Command, Moon, Search, Sun } from "lucide-react";
import { useTheme } from "next-themes";

export function Header() {
  const { resolvedTheme, setTheme } = useTheme();

  return (
    <header className="flex h-20 items-center justify-between border-b border-slate-200/80 bg-white/80 px-5 backdrop-blur-xl dark:border-slate-800 dark:bg-slate-950/80 lg:px-8">
      <div className="flex items-center gap-3 lg:hidden">
        <div className="grid size-9 place-items-center rounded-xl bg-blue-600 text-white shadow-lg shadow-blue-600/20">
          <Command size={17} />
        </div>
        <span className="text-sm font-semibold tracking-tight">ATO Planner</span>
      </div>
      <div className="relative hidden w-full max-w-sm lg:block">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={17} />
        <input className="h-10 w-full rounded-xl border border-slate-200 bg-slate-50 pl-10 pr-16 text-sm outline-none transition focus:border-blue-400 focus:ring-4 focus:ring-blue-500/10 dark:border-slate-800 dark:bg-slate-900" placeholder="Search trips, places, ideas..." />
        <span className="absolute right-2 top-1/2 -translate-y-1/2 rounded-md border border-slate-200 bg-white px-1.5 py-0.5 text-[10px] font-bold text-slate-400 dark:border-slate-700 dark:bg-slate-800">⌘ K</span>
      </div>
      <div className="flex items-center gap-2 sm:gap-4">
        <button aria-label="Notifications" className="relative grid size-10 place-items-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-white"><Bell size={18} /><span className="absolute right-2.5 top-2 size-1.5 rounded-full bg-emerald-500" /></button>
        <button aria-label="Toggle theme" onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")} className="grid size-10 place-items-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-white">
          {resolvedTheme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <div className="hidden h-8 w-px bg-slate-200 dark:bg-slate-800 sm:block" />
        <div className="flex items-center gap-2.5">
          <div className="grid size-9 place-items-center rounded-full bg-gradient-to-br from-amber-200 to-orange-400 text-sm font-bold text-orange-950">AR</div>
          <div className="hidden leading-tight sm:block"><p className="text-sm font-semibold">Aarav Rao</p><p className="text-xs text-slate-400">Explorer plan</p></div>
        </div>
      </div>
    </header>
  );
}
