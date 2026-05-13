"use client";

import { useState } from "react";

type FormState = {
  name: string;
  company: string;
  email: string;
  message: string;
};

export default function Contact() {
  const [form, setForm] = useState<FormState>({
    name: "",
    company: "",
    email: "",
    message: "",
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const update = (field: keyof FormState) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Connect to Resend, Formspree, or your own API endpoint here
    await new Promise((r) => setTimeout(r, 900));
    setLoading(false);
    setSubmitted(true);
  };

  const INPUT_CLASS =
    "w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-4 py-3 text-white text-sm placeholder-slate-600 focus:outline-none focus:border-indigo-500/70 transition-colors";

  return (
    <section id="contact" className="py-24 bg-zinc-950">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <p className="text-indigo-400 text-sm font-semibold uppercase tracking-widest mb-3">
            Contact
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to ship with confidence?
          </h2>
          <p className="text-slate-400">
            Tell us about your testing challenges and we&apos;ll show you how
            QualiOps solves them — usually within one business day.
          </p>
        </div>

        {submitted ? (
          <div className="glass-card rounded-2xl p-14 text-center">
            <div className="w-16 h-16 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mx-auto mb-5">
              <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Message received</h3>
            <p className="text-slate-400">We&apos;ll be in touch within one business day.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="glass-card rounded-2xl p-8 space-y-5">
            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm text-slate-300 mb-2">Name</label>
                <input
                  type="text"
                  required
                  value={form.name}
                  onChange={update("name")}
                  className={INPUT_CLASS}
                  placeholder="Your name"
                />
              </div>
              <div>
                <label className="block text-sm text-slate-300 mb-2">Company</label>
                <input
                  type="text"
                  value={form.company}
                  onChange={update("company")}
                  className={INPUT_CLASS}
                  placeholder="Your company"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm text-slate-300 mb-2">Work Email</label>
              <input
                type="email"
                required
                value={form.email}
                onChange={update("email")}
                className={INPUT_CLASS}
                placeholder="you@company.com"
              />
            </div>

            <div>
              <label className="block text-sm text-slate-300 mb-2">Message</label>
              <textarea
                required
                rows={4}
                value={form.message}
                onChange={update("message")}
                className={`${INPUT_CLASS} resize-none`}
                placeholder="Describe your testing challenges or what you'd like to automate..."
              />
            </div>

            <div className="flex flex-col sm:flex-row gap-3 pt-1">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 py-3.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-xl text-sm transition-colors"
              >
                {loading ? "Sending…" : "Send Message"}
              </button>
              <a
                href="https://calendly.com/9mindtech_qa-automation-call"
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 py-3.5 glass-card hover:border-white/[0.16] text-white font-semibold rounded-xl text-sm text-center transition-colors"
              >
                Book a Demo Instead
              </a>
            </div>
          </form>
        )}

        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-6 text-sm text-slate-500">
          <a
            href="mailto:wise9mind.solutions@gmail.com"
            className="flex items-center gap-2 hover:text-slate-300 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            wise9mind.solutions@gmail.com
          </a>
          <a
            href="https://calendly.com/9mindtech_qa-automation-call"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 hover:text-slate-300 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Book a free 30-min audit
          </a>
        </div>
      </div>
    </section>
  );
}
