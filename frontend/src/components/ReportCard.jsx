// ReportCard.jsx
// Card view for a single report
import { Link } from 'react-router-dom';

export default function ReportCard({ report }) {
  return (
    <div className="bg-white rounded shadow p-4 flex flex-col gap-2">
      <div className="font-bold text-lg mb-1">{report.name || report.title || report.scan_id || '-'}</div>
      <div className="text-xs text-gray-500 mb-1">ID: {report.scan_id}</div>
      {/* No created_at in backend response, so omit for now */}
      <div className="flex gap-2 mt-2">
        <Link to={`/reports/${report.scan_id}`} className="bg-purple-600 text-white px-3 py-1 rounded text-xs hover:bg-purple-700">View</Link>
        {/* Download PDF not implemented in backend yet */}
      </div>
    </div>
  );
}
