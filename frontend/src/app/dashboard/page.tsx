"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Brain,
  BarChart3,
  FileText,
  Play,
  LogOut,
  TrendingUp,
  Activity,
} from "lucide-react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  ResponsiveContainer,
} from "recharts";
import { analyticsApi, assessmentApi } from "@/lib/api";
import { formatScore } from "@/lib/utils";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [data, setData] = useState<any>(null);
  const [assessments, setAssessments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("udiap_token");
    const u = localStorage.getItem("udiap_user");
    if (!token) {
      router.push("/login");
      return;
    }
    if (u) setUser(JSON.parse(u));

    Promise.all([
      analyticsApi.dashboard().catch(() => null),
      assessmentApi.list().catch(() => []),
    ]).then(([dash, list]) => {
      setData(dash);
      setAssessments(list as any[]);
      setLoading(false);
    });
  }, [router]);

  function logout() {
    localStorage.removeItem("udiap_token");
    localStorage.removeItem("udiap_user");
    router.push("/");
  }

  const radarData = data?.latest_genome
    ? [
        { skill: "Critical", value: data.latest_genome.critical_thinking },
        { skill: "Risk", value: data.latest_genome.risk_management },
        { skill: "Adapt", value: data.latest_genome.adaptability },
        { skill: "Technical", value: data.latest_genome.technical_reasoning },
        { skill: "Comm", value: data.latest_genome.communication },
        { skill: "Reflect", value: data.latest_genome.reflection },
      ]
    : [];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-udiap-bg">
        <div className="animate-pulse text-udiap-cyan">Loading intelligence...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-udiap-bg">
      {/* Top bar */}
      <header className="border-b border-udiap-border glass sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-udiap-cyan" />
            <span className="font-semibold">
              UDI<span className="text-udiap-cyan">AP</span>
            </span>
          </div>
          <nav className="hidden sm:flex items-center gap-6 text-sm text-slate-400">
            <Link href="/dashboard" className="text-udiap-cyan">
              Dashboard
            </Link>
            <Link href="/analytics" className="hover:text-white transition">
              Analytics
            </Link>
            <Link href="/admin" className="hover:text-white transition">
              Admin
            </Link>
          </nav>
          <div className="flex items-center gap-3">
            <span className="text-sm text-slate-400 hidden sm:block">
              {user?.name}
            </span>
            <button
              onClick={logout}
              className="p-2 rounded-lg hover:bg-slate-800 transition"
              title="Logout"
            >
              <LogOut className="w-4 h-4 text-slate-400" />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Score card */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-1 glass-strong rounded-2xl p-6 flex flex-col items-center justify-center">
            <p className="text-sm text-slate-400 mb-2">Decision Intelligence Score</p>
            <div className="text-6xl font-extrabold text-glow text-udiap-cyan">
              {formatScore(data?.decision_intelligence_score)}
              <span className="text-2xl text-slate-500">/100</span>
            </div>
            <p className="mt-3 text-xs text-slate-500">
              {data?.total_assessments || 0} assessments completed
            </p>
          </div>

          <div className="md:col-span-2 glass rounded-2xl p-6">
            <h3 className="text-sm font-medium text-slate-400 mb-4 flex items-center gap-2">
              <Activity className="w-4 h-4" /> Cognitive Metrics
            </h3>
            {radarData.length > 0 ? (
              <ResponsiveContainer width="100%" height={220}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#1E293B" />
                  <PolarAngleAxis
                    dataKey="skill"
                    tick={{ fill: "#94A3B8", fontSize: 12 }}
                  />
                  <Radar
                    name="Score"
                    dataKey="value"
                    stroke="#00D9FF"
                    fill="#00D9FF"
                    fillOpacity={0.25}
                  />
                </RadarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[220px] flex items-center justify-center text-slate-500 text-sm">
                Complete an assessment to see your cognitive profile
              </div>
            )}
          </div>
        </div>

        {/* Quick actions + Assessments */}
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 glass rounded-2xl p-6">
            <div className="flex items-center justify-between mb-5">
              <h3 className="font-semibold flex items-center gap-2">
                <FileText className="w-4 h-4 text-udiap-cyan" />
                Available Assessments
              </h3>
            </div>
            <div className="space-y-3">
              {assessments.length === 0 && (
                <p className="text-sm text-slate-500">
                  No assessments yet. Seed the database or create via Admin.
                </p>
              )}
              {assessments.map((a) => (
                <div
                  key={a.id}
                  className="flex items-center justify-between p-4 rounded-xl bg-udiap-bg/60 border border-udiap-border hover:border-udiap-cyan/30 transition"
                >
                  <div>
                    <p className="font-medium">{a.title}</p>
                    <p className="text-xs text-slate-500 mt-0.5">
                      {a.category} · {a.difficulty} · ~{a.estimated_minutes} min
                    </p>
                  </div>
                  <Link
                    href={`/assessment?id=${a.id}`}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-udiap-cyan/10 text-udiap-cyan text-sm hover:bg-udiap-cyan/20 transition"
                  >
                    <Play className="w-3.5 h-3.5" /> Start
                  </Link>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-4">
            <Link
              href="/analytics"
              className="block glass rounded-2xl p-5 hover:border-udiap-cyan/40 transition group"
            >
              <BarChart3 className="w-6 h-6 text-udiap-purple mb-3" />
              <p className="font-medium group-hover:text-udiap-cyan transition">
                Analytics
              </p>
              <p className="text-xs text-slate-500 mt-1">
                Trends, heatmaps & skill comparison
              </p>
            </Link>
            <div className="glass rounded-2xl p-5">
              <TrendingUp className="w-6 h-6 text-udiap-success mb-3" />
              <p className="font-medium">Score Trend</p>
              <p className="text-xs text-slate-500 mt-1">
                {data?.score_trend?.length || 0} data points recorded
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
