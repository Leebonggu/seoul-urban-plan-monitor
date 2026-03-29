import type { MetadataRoute } from "next";
import { loadAllData } from "@/lib/data";

const BASE_URL = "https://seoul-urban-plan-monitor.2lee.kr";

export default function sitemap(): MetadataRoute.Sitemap {
  const records = loadAllData();

  const staticPages: MetadataRoute.Sitemap = [
    {
      url: BASE_URL,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1,
    },
    {
      url: `${BASE_URL}/plan`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/gangbuk`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/southwest`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "monthly",
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/privacy`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "yearly",
      priority: 0.3,
    },
    {
      url: `${BASE_URL}/terms`,
      lastModified: new Date("2026-03-22"),
      changeFrequency: "yearly",
      priority: 0.3,
    },
  ];

  const gosiPages: MetadataRoute.Sitemap = records.map((r) => ({
    url: `${BASE_URL}/gosi/${r.notice_code}`,
    lastModified: new Date(r.notice_date),
    changeFrequency: "never" as const,
    priority: 0.6,
  }));

  return [...staticPages, ...gosiPages];
}
