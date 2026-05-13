"use client";

const PLANS = [
  {
    name: "Growth",
    price: "$2,000",
    period: "/month",
    description: "For teams starting their automation journey",
    features: [
      "50 AI-generated test scenarios/month",
      "Daily scheduled runs",
      "REST API access",
      "Allure report dashboard",
      "Email support",
      "14-day free trial",
    ],
    cta: "Start Free Trial",
    highlighted: false,
  },
  {
    name: "Professional",
    price: "$4,000",
    period: "/month",
    description: "For scaling teams with CI/CD pipelines",
    badge: "Most Popular",
    features: [
      "200 AI-generated test scenarios/month",
      "CI/CD pipeline integration",
      "Webhook callbacks on completion",
      "Self-healing tests",
      "Priority execution queue",
      "Slack & email support",
      "14-day free trial",
    ],
    cta: "Start Free Trial",
    highlighted: true,
  },
  {
    name: "Enterprise",
    price: "$8,000",
    period: "/month",
    description: "For large organisations with compliance needs",
    features: [
      "Unlimited test scenarios",
      "99.9% uptime SLA",
      "Dedicated QA engineer",
      "On-premise deployment",
      "SSO / SAML",
      "Custom integrations",
      "Quarterly strategy reviews",
    ],
    cta: "Talk to Sales",
    highlighted: false,
  },
] as const;

export default function Pricing() {
  return (
    <section id="pricing" className="py-24 bg-zinc-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <p className="text-indigo-400 text-sm font-semibold uppercase tracking-widest mb-3">
            Pricing
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Simple, transparent pricing
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto">
            All plans include a 14-day free trial. No credit card required.
            Cancel anytime.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 items-center">
          {PLANS.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl p-8 flex flex-col transition-all ${
                plan.highlighted
                  ? "bg-indigo-600 shadow-2xl shadow-indigo-500/30 md:scale-105 z-10"
                  : "glass-card hover:border-white/[0.14]"
              }`}
            >
              {"badge" in plan && plan.badge && (
                <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
                  <span className="px-3 py-1 bg-white text-indigo-700 text-xs font-bold rounded-full shadow-lg">
                    {plan.badge}
                  </span>
                </div>
              )}

              <div className="mb-8">
                <h3 className="text-lg font-semibold text-white mb-1">{plan.name}</h3>
                <p className={`text-sm mb-6 ${plan.highlighted ? "text-indigo-200" : "text-slate-400"}`}>
                  {plan.description}
                </p>
                <div className="flex items-end gap-1">
                  <span className="text-4xl font-bold text-white">{plan.price}</span>
                  <span className={`text-sm mb-1 ${plan.highlighted ? "text-indigo-200" : "text-slate-400"}`}>
                    {plan.period}
                  </span>
                </div>
              </div>

              <ul className="space-y-3.5 flex-1 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3">
                    <svg
                      className={`w-4 h-4 mt-0.5 flex-shrink-0 ${plan.highlighted ? "text-white" : "text-indigo-400"}`}
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className={`text-sm ${plan.highlighted ? "text-indigo-100" : "text-slate-300"}`}>
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>

              <a
                href="https://calendly.com/9mindtech_qa-automation-call"
                target="_blank"
                rel="noopener noreferrer"
                className={`w-full py-3.5 rounded-xl text-sm font-semibold text-center transition-all ${
                  plan.highlighted
                    ? "bg-white text-indigo-700 hover:bg-indigo-50"
                    : "bg-indigo-600 hover:bg-indigo-500 text-white"
                }`}
              >
                {plan.cta}
              </a>
            </div>
          ))}
        </div>

        <p className="text-center text-slate-500 text-sm mt-10">
          Need a custom plan?{" "}
          <a href="#contact" className="text-indigo-400 hover:text-indigo-300 transition-colors underline-offset-2 hover:underline">
            Get in touch
          </a>{" "}
          and we&apos;ll build one around your team.
        </p>
      </div>
    </section>
  );
}
