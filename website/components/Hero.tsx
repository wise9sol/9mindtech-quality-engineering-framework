import BrandLogo from "@/components/BrandLogo";

const CHECK_ICON = (
  <svg className="w-4 h-4 text-emerald-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
  </svg>
);

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
      {/* Grid background */}
      <div className="absolute inset-0 bg-grid-pattern bg-grid opacity-100" />

      {/* Glow orbs */}
      <div className="absolute top-1/3 left-1/4 w-[500px] h-[500px] bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="flex flex-col items-center text-center mb-20">
          {/* Hero badge logo */}
          <div className="mb-6">
            <BrandLogo
              height={60}
              priority
              className="drop-shadow-[0_0_40px_rgba(99,102,241,0.35)]"
            />
          </div>

          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-400 text-xs font-medium mb-8">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
            Powered by Claude AI &middot; Built by 9MindTech
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight mb-6 max-w-4xl leading-tight">
            <span className="gradient-text">Continuous Compliance Validation</span>
            <br />
            <span className="text-white">for the SDLC.</span>
          </h1>

          <p className="text-lg sm:text-xl text-slate-400 max-w-2xl mb-10 leading-relaxed">
            Continuously validate and document technical control enforcement
            across your software delivery lifecycle.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 mb-12">
            <a
              href="https://calendly.com/9mindtech_qa-automation-call"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-all hover:shadow-xl hover:shadow-indigo-500/25 text-sm"
            >
              Book a Free Demo
            </a>
            <a
              href="#how-it-works"
              className="px-8 py-4 bg-white/[0.06] hover:bg-white/[0.1] border border-white/[0.1] text-white font-semibold rounded-xl transition-all text-sm"
            >
              See How It Works
            </a>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-6 text-slate-500 text-sm">
            {[
              "Technical control validation",
              "Continuous evidence generation",
              "Audit support",
              "Compliance acceleration",
            ].map((t) => (
              <div key={t} className="flex items-center gap-2">
                {CHECK_ICON}
                <span>{t}</span>
              </div>
            ))}
          </div>
        </div>

        {/* NL → Code transformation visual */}
        <div className="grid md:grid-cols-2 gap-4 max-w-4xl mx-auto">
          {/* Input */}
          <div className="glass-card rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-5">
              <div className="w-2.5 h-2.5 rounded-full bg-red-500/70" />
              <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/70" />
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/70" />
              <span className="ml-2 text-xs text-slate-500 font-mono">test_spec.txt</span>
            </div>
            <p className="text-slate-500 text-xs font-mono mb-3"># Your requirement in plain English</p>
            <p className="text-emerald-400 font-mono text-sm leading-relaxed">
              &quot;Test that a user can log in with valid credentials and reach the secure dashboard&quot;
            </p>
            <div className="mt-6 flex items-center gap-2 text-indigo-400 text-xs">
              <svg className="w-3 h-3 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
              </svg>
              Sending to Claude AI&hellip;
            </div>
          </div>

          {/* Output */}
          <div className="glass-card rounded-2xl p-6 border-indigo-500/20">
            <div className="flex items-center gap-2 mb-5">
              <div className="w-2.5 h-2.5 rounded-full bg-red-500/70" />
              <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/70" />
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/70" />
              <span className="ml-2 text-xs text-slate-500 font-mono">test_login_generated.py</span>
            </div>
            <pre className="text-xs font-mono leading-relaxed overflow-hidden select-none">
              <span className="text-purple-400">@pytest.mark</span><span className="text-slate-300">.ai_generated{"\n"}</span>
              <span className="text-blue-400">def </span><span className="text-yellow-300">test_login_succeeds_valid_creds</span><span className="text-slate-300">(page):{"\n"}</span>
              <span className="text-slate-500">    </span><span className="text-slate-400">&quot;&quot;&quot;AI-generated · 2026-05-13&quot;&quot;&quot;{"\n"}</span>
              <span className="text-slate-500">    </span><span className="text-slate-300">login_page </span><span className="text-slate-500">= </span><span className="text-cyan-400">LoginPage</span><span className="text-slate-300">(page){"\n"}</span>
              <span className="text-slate-500">    </span><span className="text-slate-300">login_page.</span><span className="text-yellow-300">navigate</span><span className="text-slate-300">(BASE_URL){"\n"}</span>
              <span className="text-slate-500">    </span><span className="text-slate-300">login_page.</span><span className="text-yellow-300">login</span><span className="text-slate-300">(USER, PASS){"\n"}</span>
              <span className="text-slate-500">    </span><span className="text-purple-400">assert </span><span className="text-emerald-400">&quot;/secure&quot;</span><span className="text-slate-300"> in page.url</span>
            </pre>
            <div className="mt-4 flex items-center gap-2 text-emerald-400 text-xs">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              8 tests generated &middot; ready to run
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
