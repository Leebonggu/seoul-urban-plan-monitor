import type { MetadataRoute } from "next";

const BASE_URL = "https://seoul-urban-plan-monitor.2lee.kr";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
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
  ];
}
