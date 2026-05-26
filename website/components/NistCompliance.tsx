const CONTROLS = [
  { family: "AC", name: "Access Control", count: 9 },
  { family: "AU", name: "Audit & Accountability", count: 9 },
  { family: "SC", name: "System & Communications Protection", count: 6 },
  { family: "IA", name: "Identification & Authentication", count: 6 },
  { family: "SI", name: "System & Information Integrity", count: 10 },
  { family: "IR", name: "Incident Response", count: 6 },
];

export default function NistCompliance() {
  return (
    <section id="nist" className="py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-zinc-950 via-emerald-950/[0.06] to-zinc-950 pointer-events-none" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <p className="text-emerald-400 text-sm font-semibold uppercase tracking-widest mb-3">
            Compliance Validation
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Continuous technical validation for{" "}
            <span className="text-emerald-400">NIST 800-53</span>
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto mb-4">
            QualiOps maps test execution directly to NIST 800-53 control families.
            47 control checks run on every deployment — producing timestamped,
            auditor-ready evidence without any manual documentation.
          </p>
          <p className="text-slate-500 text-sm max-w-2xl mx-auto italic">
            QualiOps provides continuous technical control validation and audit
            support. Final compliance determination requires a qualified assessor.
          </p>
        </div>

        {/* Live stats */}
        <div className="grid grid-cols-3 sm:grid-cols-3 gap-4 mb-12 max-w-2xl mx-auto">
          <div className="glass-card rounded-2xl p-6 text-center">
            <div className="text-4xl font-bold text-emerald-400 mb-1">47</div>
            <div className="text-slate-400 text-sm">controls passing</div>
          </div>
          <div className="glass-card rounded-2xl p-6 text-center">
            <div className="text-4xl font-bold text-emerald-400 mb-1">6</div>
            <div className="text-slate-400 text-sm">control families</div>
          </div>
          <div className="glass-card rounded-2xl p-6 text-center">
            <div className="text-4xl font-bold text-emerald-400 mb-1">100%</div>
            <div className="text-slate-400 text-sm">pass rate</div>
          </div>
        </div>

        {/* Control families */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
          {CONTROLS.map((c) => (
            <div
              key={c.family}
              className="glass-card rounded-xl p-5 flex items-center gap-4 hover:border-emerald-500/30 transition-colors"
            >
              <div className="w-12 h-12 rounded-lg bg-emerald-600/10 border border-emerald-500/20 flex items-center justify-center flex-shrink-0">
                <span className="text-emerald-400 text-xs font-bold font-mono">{c.family}</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-white text-sm font-medium truncate">{c.name}</p>
                <p className="text-slate-500 text-xs">{c.count} checks passing</p>
              </div>
              <div className="flex-shrink-0">
                <span className="inline-flex items-center gap-1 text-emerald-400 text-xs font-semibold">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  PASS
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* CTA to live report */}
        <div className="text-center">
          <a
            href="https://wise9sol.github.io/9mindtech-quality-engineering-framework/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 bg-emerald-600/15 hover:bg-emerald-600/25 border border-emerald-500/30 text-emerald-400 font-semibold rounded-xl transition-all text-sm"
          >
            View Live NIST Validation Report
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </a>
          <p className="text-slate-600 text-xs mt-3">
            Live report · Regenerated on every push to main · Powered by Allure
          </p>
        </div>
      </div>
    </section>
  );
}
