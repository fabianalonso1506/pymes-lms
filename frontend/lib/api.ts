const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export const login = async (email: string, password: string) => {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error('Login failed');
  const data = await res.json();
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', data.access_token);
  }
  return data;
};

export const register = async (name: string, email: string, password: string) => {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password }),
  });
  if (!res.ok) throw new Error('Registro fallido');
  return res.json();
};

const authHeaders = (): Record<string, string> => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const apiFetch = async (path: string, options: RequestInit = {}) => {
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...authHeaders() };
  if (options.headers) Object.assign(headers, options.headers as any);
  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    throw new Error(await res.text());
  }
  return res.json();
};

export const getCourses = () => apiFetch('/crud/courses');
export const getModules = () => apiFetch('/crud/modules');
export const getModule = (id: string) => apiFetch(`/crud/modules/${id}`);
export const submitAttempt = (assessmentId: number, answers: Record<string, string>) =>
  apiFetch(`/assessments/${assessmentId}/attempts`, { method: 'POST', body: JSON.stringify({ answers }) });
export const postDnc = (positionId: number, competencyLevels: Record<number, number>) =>
  apiFetch('/dnc', { method: 'POST', body: JSON.stringify({ position_id: positionId, competency_levels: competencyLevels }) });
export const awardAction = (action: string) =>
  apiFetch('/gamification/award', { method: 'POST', body: JSON.stringify({ action }) });
export const getPoints = () => apiFetch('/gamification/points');
export const getRanking = () => apiFetch('/gamification/ranking');
export const getRewards = () => apiFetch('/gamification/rewards');
export const redeemReward = (id: number) => apiFetch(`/gamification/redeem/${id}`, { method: 'POST' });
export const getRedemptions = () => apiFetch('/gamification/redemptions');
export const pendingRedemptions = () => apiFetch('/gamification/redemptions/pending');
export const updateRedemption = (id: number, status: string) =>
  apiFetch(`/gamification/redemptions/${id}`, { method: 'PUT', body: JSON.stringify({ status }) });
export const issueCertificate = (userId: number, courseId: number, type = 'internal') =>
  apiFetch('/certificates/issue', { method: 'POST', body: JSON.stringify({ user_id: userId, course_id: courseId, type }) });
export const myCertificates = () => apiFetch('/certificates/my');
export const downloadCertificate = async (id: number) => {
  const res = await fetch(`${API_URL}/certificates/${id}/download`, { headers: authHeaders() });
  if (!res.ok) throw new Error('Download failed');
  return res.text();
};
