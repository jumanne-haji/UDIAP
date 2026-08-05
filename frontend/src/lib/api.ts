const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("udiap_token");
}

export async function api<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export const authApi = {
  register: (data: { name: string; email: string; password: string }) =>
    api("/auth/register", { method: "POST", body: JSON.stringify(data) }),
  login: (data: { email: string; password: string }) =>
    api("/auth/login", { method: "POST", body: JSON.stringify(data) }),
  me: () => api("/auth/me"),
};

export const assessmentApi = {
  list: () => api("/assessments/"),
  get: (id: number) => api(`/assessments/${id}`),
  start: (assessment_id: number) =>
    api("/assessments/start", {
      method: "POST",
      body: JSON.stringify({ assessment_id }),
    }),
  submit: (data: {
    session_id: string;
    question_id: number;
    answer_text: string;
    time_spent_seconds: number;
    word_count: number;
  }) =>
    api("/assessments/submit", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

export const reportApi = {
  generate: (session_id: string) =>
    api("/report/generate", {
      method: "POST",
      body: JSON.stringify({ session_id }),
    }),
  get: (id: number) => api(`/report/${id}`),
  list: () => api("/report/"),
};

export const analyticsApi = {
  dashboard: () => api("/analytics/dashboard"),
};

export const behaviourApi = {
  log: (data: Record<string, unknown>) =>
    api("/behavior/log", { method: "POST", body: JSON.stringify(data) }),
};
