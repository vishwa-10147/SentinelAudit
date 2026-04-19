import { useQuery } from '@tanstack/react-query';
import { fetchDetections } from '../apiReports';

export default function DetectionsTable() {
  const { data, isLoading } = useQuery({
    queryKey: ['detections'],
    queryFn: fetchDetections,
  });

  if (isLoading) return <div>Loading detections...</div>;
  if (!data || data.length === 0) return <div className="text-gray-500">No detections found.</div>;

  return (
    <div className="mt-8">
      <h3 className="text-lg font-bold mb-2">Recent Detections</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white rounded shadow">
          <thead>
            <tr>
              <th className="px-4 py-2">Flow Key</th>
              <th className="px-4 py-2">Risk Score</th>
              <th className="px-4 py-2">MITRE Hits</th>
              <th className="px-4 py-2">Anomaly</th>
              <th className="px-4 py-2">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 10).map((det, idx) => (
              <tr key={idx} className="border-t">
                <td className="px-4 py-2 font-mono">{det.flow_key}</td>
                <td className="px-4 py-2 text-amber-700 font-bold">{det.risk_score}</td>
                <td className="px-4 py-2">{(det.mitre_hits || []).join(', ')}</td>
                <td className="px-4 py-2">{det.anomaly ? 'Yes' : 'No'}</td>
                <td className="px-4 py-2">{det.timestamp ? new Date(det.timestamp).toLocaleString() : '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
