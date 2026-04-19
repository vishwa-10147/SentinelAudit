// Leaderboard.jsx
// Shows top risky devices/users

export default function Leaderboard({ items = [], label = 'Device' }) {
  if (!items.length) return null;
  return (
    <div className="mb-4">
      <div className="font-semibold mb-2">Top {label}s</div>
      <ul className="divide-y divide-gray-200 bg-white rounded shadow">
        {items.map((item, i) => (
          <li key={i} className="flex justify-between px-4 py-2">
            <span>{item.name || item.id || '-'}</span>
            <span className="font-bold text-red-600">{item.risk || item.score || 0}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
