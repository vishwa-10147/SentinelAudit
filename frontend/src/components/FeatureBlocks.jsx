export default function FeatureBlocks() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
      <div className="bg-white rounded-lg shadow p-6 flex flex-col items-center">
        <div className="text-purple-600 text-4xl mb-2">🔍</div>
        <h4 className="font-bold mb-2">Scan</h4>
        <p className="text-gray-600 text-center">Run a lightweight agent to capture and analyze your network traffic for threats.</p>
      </div>
      <div className="bg-white rounded-lg shadow p-6 flex flex-col items-center">
        <div className="text-purple-600 text-4xl mb-2">📄</div>
        <h4 className="font-bold mb-2">Report</h4>
        <p className="text-gray-600 text-center">Get a professional PDF security audit report with risk scores and recommendations.</p>
      </div>
      <div className="bg-white rounded-lg shadow p-6 flex flex-col items-center">
        <div className="text-purple-600 text-4xl mb-2">🛡️</div>
        <h4 className="font-bold mb-2">Action</h4>
        <p className="text-gray-600 text-center">Take action on clear, prioritized recommendations to secure your business.</p>
      </div>
    </div>
  );
}
