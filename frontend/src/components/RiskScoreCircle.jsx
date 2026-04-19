// RiskScoreCircle.jsx
// Circular progress indicator for risk score

export default function RiskScoreCircle({ score = 0, max = 100 }) {
  const percent = Math.round((score / max) * 100);
  const color = percent < 40 ? '#22c55e' : percent < 70 ? '#facc15' : '#ef4444';
  const radius = 40;
  const stroke = 8;
  const normalizedRadius = radius - stroke / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const offset = circumference - (percent / 100) * circumference;
  return (
    <div className="flex flex-col items-center">
      <svg height={radius * 2} width={radius * 2}>
        <circle
          stroke="#e5e7eb"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke={color}
          fill="transparent"
          strokeWidth={stroke}
          strokeDasharray={circumference + ' ' + circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
      </svg>
      <div className="text-xl font-bold mt-2" style={{ color }}>{score}</div>
      <div className="text-xs text-gray-500">Risk Score</div>
    </div>
  );
}
