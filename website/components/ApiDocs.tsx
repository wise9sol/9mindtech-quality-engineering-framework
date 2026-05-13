export default function ApiDocs() {
  return (
    <section id="api-docs" className="py-24 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-zinc-950 via-indigo-950/[0.05] to-zinc-950 pointer-events-none" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="glass-card rounded-3xl p-8 md:p-14 grid md:grid-cols-2 gap-12 items-center">
          {/* Copy */}
          <div>
            <p className="text-indigo-400 text-sm font-semibold uppercase tracking-widest mb-3">
              REST API
            </p>
            <h2 className="text-3xl font-bold text-white mb-4">
              Integrate QualiOps into any pipeline
            </h2>
            <p className="text-slate-400 mb-8 leading-relaxed">
              Full REST API with interactive Swagger documentation. Submit test
              specs programmatically, poll for results, or receive webhook
              callbacks — from any language or CI platform.
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl text-sm text-center transition-colors"
              >
                View Swagger Docs
              </a>
              <a
                href="#contact"
                className="px-6 py-3 glass-card hover:border-white/[0.15] text-white font-semibold rounded-xl text-sm text-center transition-colors"
              >
                Request API Key
              </a>
            </div>
          </div>

          {/* Code snippet */}
          <div className="bg-black/50 rounded-2xl overflow-hidden border border-white/[0.07]">
            <div className="flex items-center gap-2 px-5 py-3.5 border-b border-white/[0.06]">
              <div className="w-2.5 h-2.5 rounded-full bg-red-500/70" />
              <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/70" />
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/70" />
              <span className="ml-2 text-xs text-slate-500 font-mono">POST /run</span>
            </div>
            <pre className="p-5 text-xs font-mono leading-relaxed overflow-x-auto select-none">
              <span className="text-slate-500"># Start an AI test run{"\n"}</span>
              <span className="text-yellow-300">curl</span><span className="text-white"> -X POST </span><span className="text-emerald-400">https://api.qualiops.ai/run</span><span className="text-white"> \{"\n"}</span>
              <span className="text-white">  -H </span><span className="text-orange-300">&quot;Content-Type: application/json&quot;</span><span className="text-white"> \{"\n"}</span>
              <span className="text-white">  -d </span><span className="text-orange-300">&apos;&#123;{"\n"}</span>
              <span className="text-slate-400">    </span><span className="text-cyan-400">&quot;client_id&quot;</span><span className="text-white">: </span><span className="text-emerald-400">&quot;acme-corp&quot;</span><span className="text-white">,{"\n"}</span>
              <span className="text-slate-400">    </span><span className="text-cyan-400">&quot;test_spec&quot;</span><span className="text-white">: </span><span className="text-emerald-400">&quot;Test user login flow&quot;</span><span className="text-white">,{"\n"}</span>
              <span className="text-slate-400">    </span><span className="text-cyan-400">&quot;webhook_url&quot;</span><span className="text-white">: </span><span className="text-emerald-400">&quot;https://your.app/hook&quot;</span><span className="text-white">{"\n"}</span>
              <span className="text-orange-300">  &#125;&apos;{"\n\n"}</span>
              <span className="text-slate-500"># Response{"\n"}</span>
              <span className="text-white">&#123;{"\n"}</span>
              <span className="text-slate-400">  </span><span className="text-cyan-400">&quot;run_id&quot;</span><span className="text-white">: </span><span className="text-emerald-400">&quot;a3f8c1d2&quot;</span><span className="text-white">,{"\n"}</span>
              <span className="text-slate-400">  </span><span className="text-cyan-400">&quot;status&quot;</span><span className="text-white">: </span><span className="text-emerald-400">&quot;queued&quot;</span><span className="text-white">{"\n"}</span>
              <span className="text-white">&#125;</span>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}
