// OrderSummary.jsx
// Simple order summary for Sentinel payment page

export default function OrderSummary({ company, price = 499 }) {
  return (
    <div className="border rounded p-4 bg-gray-50 mb-4">
      <h3 className="font-semibold text-lg mb-2">Order Summary</h3>
      <div className="flex justify-between mb-1">
        <span>Company:</span>
        <span className="font-medium">{company || '-'}</span>
      </div>
      <div className="flex justify-between mb-1">
        <span>Audit Report</span>
        <span>₹{price}</span>
      </div>
      <div className="flex justify-between font-bold border-t pt-2 mt-2">
        <span>Total</span>
        <span>₹{price}</span>
      </div>
    </div>
  );
}
