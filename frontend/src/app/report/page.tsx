export const dynamic = "force-dynamic";
"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import {
  Brain,
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
} from "lucide-react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  ResponsiveContainer,
} from "recharts";
import { reportApi } from "@/lib/api";
import { formatScore } from "@/lib/utils";

export default function ReportPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const reportId = Number(searchParams.get("id"));
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!localStorage.getItem("udiap_token")) {
      router.push("/login");
      return;
    }
    if (!reportId) return;
    reportApi
      .get(reportId)
      .then((r) => {
        setReport(r);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [reportId, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-udiap-bg">
        <div className="animate-pulse text-udiap-cyan">Generating intelligence report...</div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-udiap-bg">
        <p className="text-slate-400">Report not found</p>
      </div>
    );
  }

  const dims = report.full_report?.dimensions || {};
  const radarData = [
    { skill: "Critical", value: dims.critical_thinking || 0 },
    { skill: "Risk", value: dims.risk_management || 0 },
    { skill: "Adapt", value: dims.adaptability || 0 },
    { skill: "Technical", value: dims.technical_reasoning || 0 },
    { skill: "Comm", value: dims.communication || 0 },
    { skill: "Reflect", value: dims.reflection || 0 },
  ];

  const overall = report.full_report?.decision_intelligence_score ?? 0;

  return (
    <div className="min-h-screen bg-udiap-bg">
      <header className="border-b border-udiap-border glass sticky top-0 z-40">
        <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 text-sm text-slate-400 hover:text-white transition"
          >
            <ArrowLeft className="w-4 h-4" /> Dashboard
          </Link>
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4 text-udiap-cyan" />
            <span className="text-sm font-medium">AI Decision Report</span>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-10 space-y-8">
        {/* Overall Score */}
        <div className="glass-strong rounded-2xl p-8 text-center">
          <p className="text-sm text-slate-400 mb-2">Decision Intelligence Score</p>
          <div className="text-7xl font-extrabold text-glow text-udiap-cyan">
            {formatScore(overall)}
            <span className="text-3xl text-slate-500">/100</span>
          </div>
          <p className="mt-4 text-slate-300 max-w-2xl mx-auto leading-relaxed">
            {report.summary}
          </p>
        </div>

        {/* Radar + Strengths/Weaknesses */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="glass rounded-2xl p-6">
            <h3 className="text-sm font-medium text-slate-400 mb-4">
              Cognitive Profile
            </h3>
            <ResponsiveContainer width="100%" height={260}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#1E293B" />
                <PolarAngleAxis
                  dataKey="skill"
                  tick={{ fill: "#94A3B8", fontSize: 12 }}
                />
                <Radar
                  dataKey="value"
                  stroke="#00D9FF"
                  fill="#00D9FF"
                  fillOpacity={0.3}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-4">
            <div className="glass rounded-2xl p-5">
              <h3 className="text-sm font-medium text-udiap-success mb-3 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" /> Strengths
              </h3>
              <ul className="space-y-2">
                {(report.strengths || []).map((s: string) => (
                  <li key={s} className="text-sm text-slate-300 flex items-start gap-2">
                    <span className="text-udiap-success mt-0.5">•</span> {s}
                  </li>
                ))}
              </ul>
            </div>
            <div className="glass rounded-2xl p-5">
              <h3 className="text-sm font-medium text-udiap-warning mb-3 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" /> Growth Areas
              </h3>
              <ul className="space-y-2">
                {(report.weaknesses || []).map((w: string) => (
                  <li key={w} className="text-sm text-slate-300 flex items-start gap-2">
                    <span className="text-udiap-warning mt-0.5">•</span> {w}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="glass rounded-2xl p-6">
          <h3 className="text-sm font-medium text-udiap-purple mb-4 flex items-center gap-2">
            <Lightbulb className="w-4 h-4" /> AI Recommendations
          </h3>
          <div className="space-y-3">
            {(report.recommendations || []).map((r: string, i: number) => (
              <div
                key={i}
                className="flex gap-3 p-4 rounded-xl bg-udiap-bg/50 border border-udiap-border"
              >
                <span className="text-udiap-purple font-mono text-sm shrink-0">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <p className="text-sm text-slate-300 leading-relaxed">{r}</p>
              </div>
            ))}
          </div>
        </div>

        {/* HDPM completeness */}
        {report.hdpm_analysis && (
          <div className="glass rounded-2xl p-6">
            <h3 className="text-sm font-medium text-slate-400 mb-3">
              HDPM Process Completeness
            </h3>
            <div className="flex items-center gap-4">
              <div className="text-3xl font-bold text-udiap-cyan">
                {report.hdpm_analysis.completeness}%
              </div>
              <p className="text-sm text-slate-400 flex-1">
                {report.hdpm_analysis.narrative}
              </p>
            </div>
          </div>
        )}

        <div className="flex justify-center gap-4 pt-4">
          <Link
            href="/dashboard"
            className="px-6 py-2.5 rounded-xl border border-udiap-border text-sm hover:border-udiap-cyan/50 transition"
          >
            Back to Dashboard
          </Link>
          <Link
            href="/analytics"
            className="px-6 py-2.5 rounded-xl bg-udiap-cyan text-udiap-bg text-sm font-medium hover:shadow-glow transition"
          >
            View Analytics
          </Link>
        </div>
      </main>
    </div>
  );
}
