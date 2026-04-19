// StatCards.jsx
// Displays key stats for a report

export default function StatCards({ stats = {} }) {
  const items = [
    { label: 'Devices', value: stats.devices || 0 },
    { label: 'Alerts', value: stats.alerts || 0 },
    { label: 'Critical', value: stats.critical || 0 },
    { label: 'High', value: stats.high || 0 },
    { label: 'Medium', value: stats.medium || 0 },
    { label: 'Low', value: stats.low || 0 },
  ];
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-4">
      {items.map((item) => (
        <div key={item.label} className="bg-white rounded shadow p-4 flex flex-col items-center">
          <div className="text-lg font-bold">{item.value}</div>
          <div className="text-xs text-gray-500">{item.label}</div>
        </div>
      ))}
    </div>
  );
}
