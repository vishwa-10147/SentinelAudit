
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { fetchReportDetail } from '../apiReports';
import RiskScoreCircle from '../components/RiskScoreCircle';
import StatCards from '../components/StatCards';
import ThreatTable from '../components/ThreatTable';
import Leaderboard from '../components/Leaderboard';
import RiskBarChart from '../components/RiskBarChart';

export default function ReportDetail() {
  const { id } = useParams();
  const { data, isLoading, error } = useQuery({
    queryKey: ['report', id],
    queryFn: () => fetchReportDetail(id),
    enabled: !!id,
  });


  // No PDF download implemented in backend yet


  // For MVP, just show raw results
  const results = data?.results || [];

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Report Detail</h2>
      {isLoading && <div>Loading...</div>}
      {error && <div className="text-red-600">Failed to load report.</div>}
      {data && (
        <div className="space-y-6">
          <div className="mb-2"><span className="font-semibold">Scan ID:</span> {data.scan_id}</div>
          <div>
            <span className="font-semibold">Results (raw):</span>
            <pre className="bg-gray-100 p-2 rounded mt-1 overflow-x-auto text-sm">{JSON.stringify(results, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}