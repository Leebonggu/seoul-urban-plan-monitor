const STORAGE_KEY = "gosi_posted";

export interface PostedInfo {
  posted_at: string;
  blog_url: string;
}

function getAll(): Record<string, PostedInfo> {
  if (typeof window === "undefined") return {};
  const raw = localStorage.getItem(STORAGE_KEY);
  return raw ? JSON.parse(raw) : {};
}

function saveAll(data: Record<string, PostedInfo>) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

export function isPosted(noticeCode: string): boolean {
  return noticeCode in getAll();
}

export function getPostedInfo(noticeCode: string): PostedInfo | null {
  return getAll()[noticeCode] || null;
}

export function markAsPosted(noticeCode: string, blogUrl = "") {
  const all = getAll();
  all[noticeCode] = {
    posted_at: new Date().toISOString(),
    blog_url: blogUrl,
  };
  saveAll(all);
}

export function unmarkPosted(noticeCode: string) {
  const all = getAll();
  delete all[noticeCode];
  saveAll(all);
}

export function getPostedCount(): number {
  return Object.keys(getAll()).length;
}

export function exportPosted(): string {
  return JSON.stringify(getAll(), null, 2);
}
