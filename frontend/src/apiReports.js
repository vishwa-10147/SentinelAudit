import { api } from './api';


export async function fetchReports() {
  const res = await api.get('/api/reports');
  // Backend returns { reports: [...] }
  return res.data.reports || [];
}

export async function fetchReportDetail(scan_id) {
  const res = await api.get(`/api/reports/${scan_id}`);
  // Backend returns { scan_id, results }
  return res.data;
}

export async function fetchDetections() {
  const res = await api.get('/api/detections');
  // Backend returns { detections: [...] }
  return res.data.detections || [];
}
