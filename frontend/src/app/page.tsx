"use client";
export const dynamic = "force-dynamic";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  Brain,
  Cpu,
  BarChart3,
  FileText,
  ArrowRight,
  Sparkles,
  Shield,
  Zap,
} from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "Cognitive Observer Engine",
    desc: "Silently tracks keystrokes, pauses, revisions and thinking patterns to build a true Decision Genome.",
  },
  {
    icon: Cpu,
    title: "Decision Genome",
    desc: "A multi-dimensional cognitive profile measuring critical thinking, risk, adaptability and more.",
  },
  {
    icon: FileText,
    title: "AI Decision Reports",
    desc: "Personalized intelligence reports with strengths, weaknesses and actionable recommendations.",
  },
  {
    icon: BarChart3,
    title: "Analytics Intelligence",
    desc: "Trend analysis, skill comparison and behavioural heatmaps across assessments.",
  },
];

const hdpmStages = [
  "Event",
  "Perception",
  "Interpretation",
  "Prediction",
  "Decision",
  "Action",
  "Outcome",
  "Reflection",
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-udiap-bg overflow-x-hidden">
      {/* Nav */}
      <nav className="fixed top-0 inset-x-0 z-50 glass-strong">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-udiap-cyan to-udiap-purple flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg tracking-tight">
              UDI<span className="text-udiap-cyan">AP</span>
            </span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm text-slate-300">
            <a href="#features" className="hover:text-udiap-cyan transition">
              Features
            </a>
            <a href="#hdpm" className="hover:text-udiap-cyan transition">
              HDPM
            </a>
            <a href="#coe" className="hover:text-udiap-cyan transition">
              COE
            </a>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="text-sm text-slate-300 hover:text-white transition px-3 py-1.5"
            >
              Sign in
            </Link>
            <Link
              href="/register"
              className="text-sm font-medium bg-udiap-cyan text-udiap-bg px-4 py-2 rounded-lg hover:shadow-glow transition"
            >
              Start Assessment
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative pt-32 pb-24 px-4">
        <div className="absolute inset-0 bg-grid-pattern bg-[size:40px_40px] opacity-40" />
        <div className="absolute top-40 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-udiap-cyan/10 blur-[120px] rounded-full" />
        <div className="absolute top-60 left-1/3 w-[300px] h-[300px] bg-udiap-purple/15 blur-[100px] rounded-full" />

        <div className="relative max-w-5xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-udiap-cyan/30 bg-udiap-cyan/10 text-udiap-cyan text-xs font-medium mb-6">
              <Sparkles className="w-3.5 h-3.5" />
              AI Research Platform
            </div>
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight leading-tight">
              Measure How Humans{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-udiap-cyan to-udiap-purple">
                Think, Decide
              </span>{" "}
              and Adapt.
            </h1>
            <p className="mt-6 text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto">
              UDIAP uses AI to analyze decision processes, cognitive behaviour
              and intelligence patterns — beyond just answers.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/register"
                className="group inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-udiap-cyan text-udiap-bg font-semibold hover:shadow-glow transition"
              >
                Start Assessment
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition" />
              </Link>
              <a
                href="#hdpm"
                className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl border border-slate-600 text-slate-200 hover:border-udiap-cyan/50 hover:text-udiap-cyan transition"
              >
                Explore Research
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold">Core Intelligence Modules</h2>
            <p className="mt-3 text-slate-400">
              Built for scientific rigor and enterprise deployment
            </p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="glass rounded-2xl p-6 hover:border-udiap-cyan/40 transition group"
              >
                <div className="w-11 h-11 rounded-xl bg-udiap-cyan/10 flex items-center justify-center mb-4 group-hover:shadow-glow transition">
                  <f.icon className="w-5 h-5 text-udiap-cyan" />
                </div>
                <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
                <p className="text-sm text-slate-400 leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* HDPM Pipeline */}
      <section id="hdpm" className="py-24 px-4 bg-udiap-card/40">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold">Human Decision Process Model</h2>
            <p className="mt-3 text-slate-400 max-w-xl mx-auto">
              Every response is analyzed across the complete cognitive pipeline
            </p>
          </div>
          <div className="flex flex-wrap justify-center gap-2 md:gap-3">
            {hdpmStages.map((stage, i) => (
              <div key={stage} className="flex items-center gap-2 md:gap-3">
                <div className="glass px-4 py-2.5 rounded-xl text-sm font-medium border border-udiap-purple/30 text-udiap-purple">
                  {stage}
                </div>
                {i < hdpmStages.length - 1 && (
                  <ArrowRight className="w-4 h-4 text-slate-600 hidden sm:block" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* COE */}
      <section id="coe" className="py-24 px-4">
        <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl font-bold mb-4">
              Cognitive Observer Engine
            </h2>
            <p className="text-slate-400 leading-relaxed mb-6">
              While you write, COE silently captures temporal and behavioural
              signals: typing speed, thinking pauses, revision patterns and
              alternative exploration. These process signals are fused with
              content analysis to produce a true Decision Intelligence Score.
            </p>
            <ul className="space-y-3 text-sm text-slate-300">
              <li className="flex items-center gap-2">
                <Zap className="w-4 h-4 text-udiap-cyan" /> Temporal feature
                extraction
              </li>
              <li className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-udiap-cyan" /> Privacy-first,
                non-intrusive tracking
              </li>
              <li className="flex items-center gap-2">
                <Brain className="w-4 h-4 text-udiap-cyan" /> ML-ready feature
                pipeline
              </li>
            </ul>
          </div>
          <div className="glass-strong rounded-2xl p-8 space-y-4">
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Typing Speed</span>
              <span className="text-udiap-cyan font-mono">52 WPM</span>
            </div>
            <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full w-3/5 bg-gradient-to-r from-udiap-cyan to-udiap-purple rounded-full" />
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Thinking Pauses</span>
              <span className="text-udiap-cyan font-mono">7</span>
            </div>
            <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full w-2/5 bg-gradient-to-r from-udiap-cyan to-udiap-purple rounded-full" />
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Revision Quality</span>
              <span className="text-udiap-cyan font-mono">88%</span>
            </div>
            <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full w-4/5 bg-gradient-to-r from-udiap-cyan to-udiap-purple rounded-full" />
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-4">
        <div className="max-w-3xl mx-auto text-center glass-strong rounded-3xl p-12 border border-udiap-cyan/20">
          <h2 className="text-3xl font-bold mb-4">
            Ready to measure decision intelligence?
          </h2>
          <p className="text-slate-400 mb-8">
            Join researchers and organizations using UDIAP to understand how
            humans think under uncertainty.
          </p>
          <Link
            href="/register"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-udiap-cyan text-udiap-bg font-semibold hover:shadow-glow transition"
          >
            Create Free Account
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-udiap-border py-10 px-4">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-500">
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4 text-udiap-cyan" />
            <span>UDIAP © 2026</span>
          </div>
          <p>Universal Decision Intelligence Assessment Platform</p>
        </div>
      </footer>
    </div>
  );
}
