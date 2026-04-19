export default function PricingCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
      <div className="border rounded-lg p-6 flex flex-col items-center shadow">
        <h3 className="text-xl font-bold mb-2">One-time Report</h3>
        <div className="text-3xl font-bold text-purple-700 mb-2">₹9,999</div>
        <ul className="mb-4 text-gray-600 text-sm">
          <li>Single scan</li>
          <li>PDF report emailed</li>
        </ul>
        <a href="/register" className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">Get Started</a>
      </div>
      <div className="border-2 border-purple-600 rounded-lg p-6 flex flex-col items-center shadow bg-purple-50">
        <h3 className="text-xl font-bold mb-2">Monthly</h3>
        <div className="text-3xl font-bold text-purple-700 mb-2">₹14,999<span className="text-base font-normal">/mo</span></div>
        <ul className="mb-4 text-gray-600 text-sm">
          <li>Automated monthly reports</li>
          <li>Priority support</li>
        </ul>
        <a href="/register" className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">Start Free Trial</a>
      </div>
      <div className="border rounded-lg p-6 flex flex-col items-center shadow">
        <h3 className="text-xl font-bold mb-2">Annual</h3>
        <div className="text-3xl font-bold text-purple-700 mb-2">₹1,29,999<span className="text-base font-normal">/yr</span></div>
        <ul className="mb-4 text-gray-600 text-sm">
          <li>Monthly reports</li>
          <li>28% saving</li>
        </ul>
        <a href="/register" className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">Start Free Trial</a>
      </div>
    </div>
  );
}
