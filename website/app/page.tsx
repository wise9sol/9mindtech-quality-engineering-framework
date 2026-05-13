import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Demo from "@/components/Demo";
import HowItWorks from "@/components/HowItWorks";
import Features from "@/components/Features";
import CaseStudy from "@/components/CaseStudy";
import Pricing from "@/components/Pricing";
import ApiDocs from "@/components/ApiDocs";
import Contact from "@/components/Contact";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="bg-zinc-950">
      <Navbar />
      <Hero />
      <Demo />
      <HowItWorks />
      <Features />
      <CaseStudy />
      <Pricing />
      <ApiDocs />
      <Contact />
      <Footer />
    </main>
  );
}
