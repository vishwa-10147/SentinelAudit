// ThreatTable.jsx
// Table of top threats in the report

export default function ThreatTable({ threats = [] }) {
  if (!threats.length) return null;
  return (
    <div className="overflow-x-auto mb-4">
      <table className="min-w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">Threat</th>
            <th className="p-2 border">Severity</th>
            <th className="p-2 border">Count</th>
          </tr>
        </thead>
        <tbody>
          {threats.map((t, i) => (
            <tr key={i} className="hover:bg-gray-50">
              <td className="p-2 border">{t.name || t.id || '-'}</td>
              <td className="p-2 border">{t.severity || '-'}</td>
              <td className="p-2 border">{t.count || 0}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
