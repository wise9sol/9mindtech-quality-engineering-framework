const STATS = [
  { value: "9.47s", label: "Average execution time" },
  { value: "8+", label: "Scenarios per spec" },
  { value: "100%", label: "CI/CD compatible" },
];

export default function Demo() {
  return (
    <section id="demo" className="py-24 bg-zinc-950">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            See QualiOps in Action
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto">
            Watch how a single sentence becomes a full test suite — generated
            and executed in under 10 seconds.
          </p>
        </div>

        {/* Video placeholder */}
        <div className="relative glass-card rounded-2xl overflow-hidden aspect-video flex items-center justify-center group cursor-pointer mb-8">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-900/20 to-purple-900/20" />
          <div className="absolute inset-0 bg-grid-pattern bg-grid opacity-30" />

          <div className="relative z-10 flex flex-col items-center gap-5">
            <div className="w-20 h-20 rounded-full bg-indigo-600/90 flex items-center justify-center group-hover:scale-110 transition-transform duration-200 shadow-2xl shadow-indigo-500/40">
              <svg className="w-8 h-8 text-white ml-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M6.3 2.841A1.5 1.5 0 004 4.11v11.78a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
              </svg>
            </div>
            <div className="text-center">
              <p className="text-white font-semibold text-lg">Watch the Demo</p>
              <p className="text-slate-400 text-sm mt-1">3 min &middot; No sign-up required</p>
            </div>
          </div>

          <div className="absolute top-4 right-4 px-3 py-1 bg-black/60 rounded-full text-xs text-slate-400 border border-white/10">
            Loom recording — coming soon
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          {STATS.map((s) => (
            <div key={s.label} className="glass-card rounded-xl p-5 text-center">
              <div className="text-3xl font-bold gradient-text mb-1">{s.value}</div>
              <div className="text-slate-400 text-sm">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
