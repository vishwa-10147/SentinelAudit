import { useQuery } from '@tanstack/react-query';
import { fetchReports } from '../apiReports';
import { Link } from 'react-router-dom';

export default function RecentReports() {
  const { data, isLoading } = useQuery({
    queryKey: ['reports'],
    queryFn: fetchReports,
  });

  if (isLoading) return <div>Loading recent reports...</div>;
  if (!data || data.length === 0) return <div className="text-gray-500">No reports found.</div>;

  return (
    <div className="mt-6">
      <h3 className="text-lg font-bold mb-2">Recent Reports</h3>
      <ul className="divide-y">
        {data.slice(0, 5).map((report) => (
          <li key={report.id} className="py-2 flex items-center justify-between">
            <div>
              <span className="font-semibold">{report.name || report.title || 'Report'}</span>
              <span className="ml-2 text-gray-500 text-sm">{report.created_at ? new Date(report.created_at).toLocaleString() : '-'}</span>
            </div>
            <Link to={`/reports/${report.id}`} className="text-purple-600 hover:underline">View</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
