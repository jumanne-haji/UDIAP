"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Brain, Loader2 } from "lucide-react";
import { authApi } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res: any = await authApi.login({ email, password });
      localStorage.setItem("udiap_token", res.access_token);
      localStorage.setItem("udiap_user", JSON.stringify(res.user));
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-udiap-bg">
      <div className="absolute inset-0 bg-grid-pattern bg-[size:40px_40px] opacity-30" />
      <div className="relative w-full max-w-md glass-strong rounded-2xl p-8">
        <div className="flex items-center gap-2 mb-8 justify-center">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-udiap-cyan to-udiap-purple flex items-center justify-center">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-xl">
            UDI<span className="text-udiap-cyan">AP</span>
          </span>
        </div>
        <h1 className="text-2xl font-bold text-center mb-2">Welcome back</h1>
        <p className="text-slate-400 text-center text-sm mb-8">
          Sign in to continue your decision intelligence journey
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-slate-400 mb-1.5">Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg bg-udiap-bg border border-udiap-border focus:border-udiap-cyan focus:outline-none focus:ring-1 focus:ring-udiap-cyan/50 transition"
              placeholder="you@company.com"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-400 mb-1.5">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg bg-udiap-bg border border-udiap-border focus:border-udiap-cyan focus:outline-none focus:ring-1 focus:ring-udiap-cyan/50 transition"
              placeholder="••••••••"
            />
          </div>
          {error && (
            <p className="text-udiap-danger text-sm text-center">{error}</p>
          )}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-udiap-cyan text-udiap-bg font-semibold hover:shadow-glow transition disabled:opacity-60 flex items-center justify-center gap-2"
          >
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            Sign in
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-400">
          No account?{" "}
          <Link href="/register" className="text-udiap-cyan hover:underline">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
