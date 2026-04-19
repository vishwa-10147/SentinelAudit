
import { useQuery } from '@tanstack/react-query';
import { fetchReports } from '../apiReports';
import ReportCard from '../components/ReportCard';

export default function ReportsList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['reports'],
    queryFn: fetchReports,
  });

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-4">Reports</h2>
      {isLoading && <div>Loading...</div>}
      {error && <div className="text-red-600">Failed to load reports.</div>}
      {data && data.length === 0 && <div className="text-gray-500">No reports found.</div>}
      {data && data.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-4">
          {data.map((report) => (
            <ReportCard key={report.scan_id} report={report} />
          ))}
        </div>
      )}
    </div>
  );
}