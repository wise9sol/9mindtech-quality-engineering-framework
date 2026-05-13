const STEPS = [
  {
    number: "01",
    title: "Describe",
    description:
      "Write your test requirement in plain English. No syntax, no selectors, no framework knowledge needed. Just describe what the user should be able to do.",
    example: '"Test that a user can log in with valid credentials"',
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
      </svg>
    ),
  },
  {
    number: "02",
    title: "Generate",
    description:
      "Claude AI translates your spec into 8+ production-grade pytest + Playwright test scenarios — covering happy paths, edge cases, error states, and security inputs automatically.",
    example: "8 tests generated in 2.1s",
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    ),
  },
  {
    number: "03",
    title: "Execute",
    description:
      "Tests run instantly in Playwright (Chromium). Results stream back via REST API or webhook — Allure reports included, ready to integrate into any CI/CD pipeline.",
    example: "8 passed in 9.47s ✓",
    icon: (
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-zinc-950 via-indigo-950/[0.08] to-zinc-950 pointer-events-none" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <p className="text-indigo-400 text-sm font-semibold uppercase tracking-widest mb-3">
            Process
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            From spec to results in three steps
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto">
            No QA engineers needed to write tests. No framework configuration.
            Describe it, ship it.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 relative">
          {STEPS.map((step, i) => (
            <div key={step.number} className="relative flex flex-col">
              <div className="glass-card rounded-2xl p-8 flex-1 hover:border-indigo-500/30 transition-colors">
                <div className="flex items-start justify-between mb-6">
                  <div className="w-12 h-12 rounded-xl bg-indigo-600/15 border border-indigo-500/25 flex items-center justify-center text-indigo-400">
                    {step.icon}
                  </div>
                  <span className="text-5xl font-bold text-white/[0.05] select-none">
                    {step.number}
                  </span>
                </div>

                <h3 className="text-xl font-semibold text-white mb-3">{step.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed mb-6">
                  {step.description}
                </p>

                <div className="bg-black/30 rounded-lg px-4 py-3 border border-white/[0.06]">
                  <p className="text-xs font-mono text-emerald-400">{step.example}</p>
                </div>
              </div>

              {i < STEPS.length - 1 && (
                <div className="hidden md:flex absolute -right-3 top-12 z-10 w-6 h-6 rounded-full bg-zinc-900 border border-white/[0.08] items-center justify-center">
                  <svg className="w-3 h-3 text-indigo-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
