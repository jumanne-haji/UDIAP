"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Clock, Save, Send, Loader2, Brain } from "lucide-react";
import { assessmentApi, behaviourApi, reportApi } from "@/lib/api";

export default function AssessmentWorkspace() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const assessmentId = Number(searchParams.get("id") || 1);

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [assessment, setAssessment] = useState<any>(null);
  const [question, setQuestion] = useState<any>(null);
  const [answer, setAnswer] = useState("");
  const [seconds, setSeconds] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [saved, setSaved] = useState(false);

  // Cognitive tracking state
  const keystrokes = useRef(0);
  const revisions = useRef(0);
  const deletedChars = useRef(0);
  const lastKeyTime = useRef(Date.now());
  const pauseAccum = useRef(0);
  const thinkingPauses = useRef(0);
  const startTime = useRef(Date.now());

  // Timer
  useEffect(() => {
    const t = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, []);

  // Start session
  useEffect(() => {
    const token = localStorage.getItem("udiap_token");
    if (!token) {
      router.push("/login");
      return;
    }
    assessmentApi
      .start(assessmentId)
      .then((res: any) => {
        setSessionId(res.session_id);
        setAssessment(res.assessment);
        const q = res.assessment?.questions?.[0];
        setQuestion(q);
      })
      .catch(() => router.push("/dashboard"));
  }, [assessmentId, router]);

  // Auto-save every 30s
  useEffect(() => {
    if (!sessionId || !answer) return;
    const interval = setInterval(() => {
      setSaved(true);
      setTimeout(() => setSaved(false), 1500);
    }, 30000);
    return () => clearInterval(interval);
  }, [sessionId, answer]);

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      const newVal = e.target.value;
      const now = Date.now();
      const delta = now - lastKeyTime.current;

      if (delta > 2000) {
        pauseAccum.current += delta;
        thinkingPauses.current += 1;
      }
      lastKeyTime.current = now;

      if (newVal.length < answer.length) {
        deletedChars.current += answer.length - newVal.length;
        revisions.current += 1;
      } else {
        keystrokes.current += 1;
      }
      setAnswer(newVal);
    },
    [answer]
  );

  async function handleSubmit() {
    if (!sessionId || !question || answer.trim().length < 20) return;
    setSubmitting(true);

    const totalMs = Date.now() - startTime.current;
    const words = answer.trim().split(/\s+/).filter(Boolean).length;
    const wpm =
      totalMs > 0 ? (keystrokes.current / 5) / (totalMs / 60000) : 0;

    try {
      // Log behaviour
      await behaviourApi.log({
        session_id: sessionId,
        keystrokes: keystrokes.current,
        typing_speed_wpm: Math.round(wpm * 10) / 10,
        pause_time_ms: pauseAccum.current,
        total_time_ms: totalMs,
        thinking_pause_count: thinkingPauses.current,
        revision_count: revisions.current,
        deleted_chars: deletedChars.current,
        sentence_restructures: 0,
        alternative_explorations: 0,
      });

      // Submit answer
      await assessmentApi.submit({
        session_id: sessionId,
        question_id: question.id,
        answer_text: answer,
        time_spent_seconds: Math.round(totalMs / 1000),
        word_count: words,
      });

      // Generate report
      const report: any = await reportApi.generate(sessionId);
      router.push(`/report?id=${report.id}`);
    } catch (err: any) {
      alert(err.message || "Submission failed");
      setSubmitting(false);
    }
  }

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m.toString().padStart(2, "0")}:${sec.toString().padStart(2, "0")}`;
  };

  const wordCount = answer.trim() ? answer.trim().split(/\s+/).length : 0;

  if (!assessment || !question) {
    return (
      <div className="min-h-screen flex items-center justify-center assessment-workspace">
        <Loader2 className="w-6 h-6 animate-spin text-udiap-cyan" />
      </div>
    );
  }

  return (
    <div className="min-h-screen assessment-workspace">
      {/* Minimal top bar */}
      <header className="border-b border-udiap-border/50 px-4 h-12 flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <Brain className="w-4 h-4 text-udiap-cyan" />
          <span className="hidden sm:inline">{assessment.title}</span>
        </div>
        <div className="flex items-center gap-4 text-sm">
          {saved && (
            <span className="text-udiap-success flex items-center gap-1">
              <Save className="w-3.5 h-3.5" /> Saved
            </span>
          )}
          <span className="flex items-center gap-1.5 text-slate-400 font-mono">
            <Clock className="w-3.5 h-3.5" />
            {formatTime(seconds)}
          </span>
          <span className="text-slate-500">{wordCount} words</span>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        {/* Scenario Card */}
        <div className="glass-strong rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-semibold text-udiap-cyan">Scenario</h2>
          <p className="text-slate-200 leading-relaxed whitespace-pre-wrap">
            {question.question_text}
          </p>
          {question.context && (
            <div className="pt-3 border-t border-udiap-border">
              <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">
                Context
              </p>
              <p className="text-sm text-slate-400">{question.context}</p>
            </div>
          )}
          {question.constraints && (
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">
                Constraints
              </p>
              <p className="text-sm text-slate-400">{question.constraints}</p>
            </div>
          )}
        </div>

        {/* Response Editor */}
        <div className="glass rounded-2xl p-1">
          <textarea
            value={answer}
            onChange={handleChange}
            placeholder="Write your structured decision analysis here. Demonstrate your reasoning process..."
            className="w-full min-h-[320px] bg-transparent px-5 py-4 text-slate-100 placeholder:text-slate-600 focus:outline-none resize-y leading-relaxed"
            autoFocus
          />
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleSubmit}
            disabled={submitting || wordCount < 20}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-udiap-cyan text-udiap-bg font-semibold hover:shadow-glow transition disabled:opacity-50"
          >
            {submitting ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            Submit & Generate Report
          </button>
        </div>
      </div>
    </div>
  );
}
