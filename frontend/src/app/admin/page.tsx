"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Brain, ArrowLeft, Users, Activity, Shield } from "lucide-react";
import { api } from "@/lib/api";

export default function AdminPage() {
  const router = useRouter();
  const [users, setUsers] = useState<any[]>([]);
  const [monitoring, setMonitoring] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!localStorage.getItem("udiap_token")) {
      router.push("/login");
      return;
    }
    Promise.all([
      api("/admin/users").catch((e) => {
        setError(e.message);
        return [];
      }),
      api("/admin/monitoring").catch(() => null),
    ]).then(([u, m]) => {
      setUsers(u as any[]);
      setMonitoring(m);
    });
  }, [router]);

  return (
    <div className="min-h-screen bg-udiap-bg">
      <header className="border-b border-udiap-border glass sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center gap-2 text-sm text-slate-400 hover:text-white">
            <ArrowLeft className="w-4 h-4" /> Dashboard
          </Link>
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4 text-udiap-purple" />
            <span className="text-sm font-medium">Admin Panel</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
        <h1 className="text-2xl font-bold">Enterprise Administration</h1>

        {error && (
          <div className="glass border border-udiap-warning/40 rounded-xl p-4 text-sm text-udiap-warning">
            {error} — Admin role required. Use admin@udiap.ai account.
          </div>
        )}

        {/* Monitoring */}
        {monitoring && (
          <div className="grid sm:grid-cols-4 gap-4">
            {[
              { label: "Model Accuracy", value: `${(monitoring.model_accuracy * 100).toFixed(1)}%`, icon: Activity },
              { label: "Avg Processing", value: `${monitoring.avg_processing_time_ms}ms`, icon: Activity },
              { label: "Error Rate", value: `${(monitoring.error_rate * 100).toFixed(2)}%`, icon: Activity },
              { label: "Status", value: monitoring.status, icon: Brain },
            ].map((m) => (
              <div key={m.label} className="glass rounded-xl p-4">
                <p className="text-xs text-slate-500">{m.label}</p>
                <p className="text-xl font-semibold text-udiap-cyan mt-1">{m.value}</p>
              </div>
            ))}
          </div>
        )}

        {/* Users */}
        <div className="glass rounded-2xl p-6">
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            <Users className="w-4 h-4 text-udiap-cyan" /> User Management
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-slate-500 border-b border-udiap-border">
                  <th className="pb-3 font-medium">Name</th>
                  <th className="pb-3 font-medium">Email</th>
                  <th className="pb-3 font-medium">Role</th>
                  <th className="pb-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id} className="border-b border-udiap-border/50">
                    <td className="py-3">{u.name}</td>
                    <td className="py-3 text-slate-400">{u.email}</td>
                    <td className="py-3">
                      <span className="px-2 py-0.5 rounded text-xs bg-udiap-purple/20 text-udiap-purple">
                        {u.role}
                      </span>
                    </td>
                    <td className="py-3">
                      <span className={u.is_active ? "text-udiap-success" : "text-udiap-danger"}>
                        {u.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                  </tr>
                ))}
                {users.length === 0 && (
                  <tr>
                    <td colSpan={4} className="py-6 text-center text-slate-500">
                      No users loaded
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
