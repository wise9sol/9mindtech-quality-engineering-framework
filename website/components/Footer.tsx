import BrandLogo from "@/components/BrandLogo";

const PRODUCT_LINKS = [
  { label: "Features", href: "#features" },
  { label: "How it Works", href: "#how-it-works" },
  { label: "Pricing", href: "#pricing" },
  { label: "API Docs", href: "#api-docs" },
];

const COMPANY_LINKS = [
  { label: "9MindTech", href: "http://www.9mindtech.com", external: true },
  { label: "Book a Demo", href: "https://calendly.com/9mindtech_qa-automation-call", external: true },
  { label: "GitHub", href: "https://github.com/wise9sol", external: true },
  { label: "Contact", href: "#contact", external: false },
];

export default function Footer() {
  return (
    <footer className="border-t border-white/[0.06] bg-zinc-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-10 mb-14">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="text-xl font-bold gradient-text mb-3">QualiOps AI</div>
            <p className="text-slate-400 text-sm leading-relaxed max-w-xs mb-4">
              Autonomous quality engineering platform. Convert natural language specs into production-grade Playwright tests — powered by Claude AI.
            </p>
            <BrandLogo height={30} className="opacity-60" />
          </div>

          {/* Product */}
          <div>
            <p className="text-white text-sm font-semibold mb-5">Product</p>
            <ul className="space-y-3">
              {PRODUCT_LINKS.map((l) => (
                <li key={l.label}>
                  <a
                    href={l.href}
                    className="text-slate-400 hover:text-white text-sm transition-colors"
                  >
                    {l.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <p className="text-white text-sm font-semibold mb-5">Company</p>
            <ul className="space-y-3">
              {COMPANY_LINKS.map((l) => (
                <li key={l.label}>
                  <a
                    href={l.href}
                    target={l.external ? "_blank" : undefined}
                    rel={l.external ? "noopener noreferrer" : undefined}
                    className="text-slate-400 hover:text-white text-sm transition-colors"
                  >
                    {l.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="border-t border-white/[0.06] pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-slate-600 text-sm">
            &copy; {new Date().getFullYear()} 9MindTech. All rights reserved.
          </p>
          <div className="flex items-center gap-4 text-slate-600 text-sm">
            <span>MIT License</span>
            <span>&middot;</span>
            <a
              href="mailto:wise9mind.solutions@gmail.com"
              className="hover:text-slate-300 transition-colors"
            >
              wise9mind.solutions@gmail.com
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
