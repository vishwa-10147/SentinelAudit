import { useQuery } from '@tanstack/react-query';
import { fetchReports } from '../apiReports';

export default function DashboardStats() {
  const { data, isLoading } = useQuery({
    queryKey: ['reports'],
    queryFn: fetchReports,
  });

  if (isLoading) return <div className="mb-6">Loading stats...</div>;
  if (!data) return null;

  const totalReports = data.length;
  const avgRisk = data.length
    ? Math.round(
        data.reduce((sum, r) => sum + (r.overall_risk_score || 0), 0) / data.length
      )
    : 0;
  const lastReport = data[0];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div className="bg-white rounded-lg shadow p-6 flex flex-col items-center">
        <div className="text-2xl font-bold text-purple-700 mb-1">{totalReports}</div>
        <div className="text-gray-600">Total Reports</div>
      </div>
      <div className="bg-white rounded-lg shadow p-6 flex flex-col items-center">
        <div className="text-2xl font-bold text-amber-600 mb-1">{avgRisk}</div>
        <div className="text-gray-600">Avg Risk Score</div>
      </div>
      <div className="bg-white rounded-lg shadow p-6 flex flex-col items-center">
        <div className="text-2xl font-bold text-gray-700 mb-1">{lastReport?.created_at ? new Date(lastReport.created_at).toLocaleDateString() : '-'}</div>
        <div className="text-gray-600">Last Report</div>
      </div>
    </div>
  );
}
