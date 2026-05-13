import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "QualiOps AI — Autonomous Quality Engineering Platform",
  description:
    "Convert natural language test specs into automated Playwright tests using Claude AI. 8+ test scenarios from one sentence, executed in seconds.",
  keywords:
    "test automation, AI testing, Playwright, natural language, QA automation, pytest, CI/CD",
  icons: {
    icon: "/qualiaps-logo-transparent.png",
    apple: "/qualiaps-logo-transparent.png",
  },
  openGraph: {
    title: "QualiOps AI — Autonomous Quality Engineering Platform",
    description:
      "Convert natural language test specs into automated Playwright tests using Claude AI.",
    type: "website",
    siteName: "QualiOps AI",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
