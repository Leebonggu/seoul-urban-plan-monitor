export interface GosiRecord {
  notice_code: string;
  notice_no: string;
  notice_date: string;
  title: string;
  content: string;
  organ_code: string;
  organ_name: string;
  notice_type: string;
  classify_g: string;
  classify_m: string;
  site_code: string;
  site_name: string;
  location: string;
  doc_url: string;
  page_url: string;
  center_grade: string | null;
  center_name: string | null;
  category?: string;
}

export interface Center {
  name: string;
  grade: string;
  lat: number;
  lng: number;
  count: number;
}

export interface AggregatedData {
  totalCount: number;
  centerMatchedCount: number;
  latestDate: string;
  oldestDate: string;
  centerCounts: Record<string, number>;
  monthlyData: { month: string; count: number }[];
  gradeData: { name: string; value: number }[];
  centerRanking: { name: string; count: number; grade: string }[];
}
