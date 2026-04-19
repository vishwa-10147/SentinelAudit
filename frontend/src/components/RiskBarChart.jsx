// RiskBarChart.jsx
// Simple bar chart for risk distribution using Recharts
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function RiskBarChart({ data = [] }) {
  if (!data.length) return null;
  return (
    <div className="bg-white rounded shadow p-4 mb-4">
      <div className="font-semibold mb-2">Risk Distribution</div>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#7c3aed" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
