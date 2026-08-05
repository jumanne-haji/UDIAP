"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Brain, ArrowLeft } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";
import { analyticsApi } from "@/lib/api";

export default function AnalyticsPage() {
  const router = useRouter();
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    if (!localStorage.getItem("udiap_token")) {
      router.push("/login");
      return;
    }
    analyticsApi.dashboard().then(setData).catch(() => {});
  }, [router]);

  const trend = (data?.score_trend || []).map((t: any) => ({
    date: new Date(t.date).toLocaleDateString("en", { month: "short", day: "numeric" }),
    score: t.score,
  }));

  const skills = data?.latest_genome
    ? [
        { name: "Critical", score: data.latest_genome.critical_thinking },
        { name: "Risk", score: data.latest_genome.risk_management },
        { name: "Adapt", score: data.latest_genome.adaptability },
        { name: "Technical", score: data.latest_genome.technical_reasoning },
        { name: "Comm", score: data.latest_genome.communication },
        { name: "Reflect", score: data.latest_genome.reflection },
      ]
    : [];

  return (
    <div className="min-h-screen bg-udiap-bg">
      <header className="border-b border-udiap-border glass sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-2 text-sm text-slate-400 hover:text-white">
            <ArrowLeft className="w-4 h-4" /> Dashboard
          </Link>
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4 text-udiap-cyan" />
            <span className="text-sm font-medium">Analytics Intelligence</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
        <h1 className="text-2xl font-bold">Performance Analytics</h1>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="glass rounded-2xl p-6">
            <h3 className="text-sm text-slate-400 mb-4">Decision Score Trend</h3>
            {trend.length > 0 ? (
              <ResponsiveContainer width="100%" height={240}>
                <LineChart data={trend}>
                  <CartesianGrid stroke="#1E293B" strokeDasharray="3 3" />
                  <XAxis dataKey="date" tick={{ fill: "#64748B", fontSize: 11 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: "#64748B", fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ background: "#111827", border: "1px solid #1E293B" }}
                  />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#00D9FF"
                    strokeWidth={2}
                    dot={{ fill: "#00D9FF" }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[240px] flex items-center justify-center text-slate-500 text-sm">
                Complete assessments to see trends
              </div>
            )}
          </div>

          <div className="glass rounded-2xl p-6">
            <h3 className="text-sm text-slate-400 mb-4">Skill Comparison</h3>
            {skills.length > 0 ? (
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={skills}>
                  <CartesianGrid stroke="#1E293B" strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fill: "#64748B", fontSize: 11 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: "#64748B", fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ background: "#111827", border: "1px solid #1E293B" }}
                  />
                  <Bar dataKey="score" fill="#7C3AED" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[240px] flex items-center justify-center text-slate-500 text-sm">
                No skill data yet
              </div>
            )}
          </div>
        </div>

        <div className="glass rounded-2xl p-6">
          <h3 className="text-sm text-slate-400 mb-2">Summary</h3>
          <p className="text-slate-300">
            Total assessments:{" "}
            <span className="text-udiap-cyan font-semibold">
              {data?.total_assessments ?? 0}
            </span>
            {" · "}
            Latest DI Score:{" "}
            <span className="text-udiap-cyan font-semibold">
              {data?.decision_intelligence_score ?? "—"}
            </span>
          </p>
        </div>
      </main>
    </div>
  );
}
