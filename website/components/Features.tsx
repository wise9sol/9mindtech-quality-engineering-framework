const FEATURES = [
  {
    title: "Natural Language Test Creation",
    description:
      "Write requirements in plain English. QualiOps translates them into executable pytest + Playwright code — complete with markers, docstrings, and assertions that conform to your coding standards.",
    badge: "Core",
    color: "indigo" as const,
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
      </svg>
    ),
  },
  {
    title: "Self-Healing Tests",
    description:
      "UI redesigns break brittle selectors. QualiOps detects locator drift and automatically patches tests to match the updated structure — every change logged to a full audit trail.",
    badge: "Intelligent",
    color: "purple" as const,
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
      </svg>
    ),
  },
  {
    title: "Instant Results via REST API",
    description:
      "Submit a spec, receive a run ID immediately, poll for results or receive a webhook callback. Every result includes a full Allure report and stdout log — integrates into any pipeline in minutes.",
    badge: "Fast",
    color: "emerald" as const,
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
  },
  {
    title: "8+ Scenarios from One Spec",
    description:
      "One sentence generates a complete test matrix: happy paths, invalid inputs, SQL injection, boundary values, session behaviour, performance assertions, and accessibility checks — automatically.",
    badge: "Comprehensive",
    color: "amber" as const,
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
      </svg>
    ),
  },
];

const ICON_COLORS = {
  indigo: "bg-indigo-600/10 border-indigo-500/20 text-indigo-400",
  purple: "bg-purple-600/10 border-purple-500/20 text-purple-400",
  emerald: "bg-emerald-600/10 border-emerald-500/20 text-emerald-400",
  amber: "bg-amber-600/10 border-amber-500/20 text-amber-400",
};

const BADGE_COLORS = {
  indigo: "bg-indigo-500/10 text-indigo-400",
  purple: "bg-purple-500/10 text-purple-400",
  emerald: "bg-emerald-500/10 text-emerald-400",
  amber: "bg-amber-500/10 text-amber-400",
};

export default function Features() {
  return (
    <section id="features" className="py-24 bg-zinc-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <p className="text-indigo-400 text-sm font-semibold uppercase tracking-widest mb-3">
            Features
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Everything your QA team needs — automated
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto">
            QualiOps replaces hours of manual test authoring with seconds of AI
            generation, so your engineers can focus on building.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 gap-6">
          {FEATURES.map((f) => (
            <div
              key={f.title}
              className="glass-card rounded-2xl p-8 hover:border-white/[0.12] transition-colors"
            >
              <div className="flex items-start justify-between mb-6">
                <div
                  className={`w-10 h-10 rounded-lg border flex items-center justify-center ${ICON_COLORS[f.color]}`}
                >
                  {f.icon}
                </div>
                <span
                  className={`text-xs font-semibold px-2.5 py-1 rounded-full ${BADGE_COLORS[f.color]}`}
                >
                  {f.badge}
                </span>
              </div>
              <h3 className="text-lg font-semibold text-white mb-3">{f.title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{f.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
