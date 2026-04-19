
import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import OrderSummary from '../components/OrderSummary';

// Razorpay script loader
function loadRazorpayScript(src) {
  return new Promise((resolve) => {
    const script = document.createElement('script');
    script.src = src;
    script.onload = () => resolve(true);
    script.onerror = () => resolve(false);
    document.body.appendChild(script);
  });
}

export default function Payment() {
  const navigate = useNavigate();
  const location = useLocation();
  // Assume company name is passed from upload page via state
  const company = location.state?.company || '';
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const price = 499; // INR, static for now

  const handlePay = async () => {
    setError('');
    setLoading(true);
    const res = await loadRazorpayScript('https://checkout.razorpay.com/v1/checkout.js');
    if (!res) {
      setError('Failed to load Razorpay SDK.');
      setLoading(false);
      return;
    }
    try {
      // TODO: Replace with actual backend call to create Razorpay order
      // const { orderId } = await api.post('/api/payments/create-order', { amount: price, company });
      const orderId = 'order_DUMMY123'; // Placeholder
      const options = {
        key: 'rzp_test_1234567890abcdef', // TODO: Replace with your Razorpay key
        amount: price * 100,
        currency: 'INR',
        name: 'Sentinel Audit',
        description: 'Network Security Audit',
        order_id: orderId,
        handler: function (response) {
          // TODO: Verify payment on backend
          navigate('/dashboard');
        },
        prefill: {
          name: company,
        },
        theme: {
          color: '#7c3aed',
        },
      };
      // eslint-disable-next-line no-undef
      const rzp = new window.Razorpay(options);
      rzp.open();
    } catch (err) {
      setError('Payment initiation failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-lg mx-auto">
      <h2 className="text-2xl font-bold mb-4">Payment</h2>
      <OrderSummary company={company} price={price} />
      <button
        className="bg-purple-600 text-white py-2 px-6 rounded hover:bg-purple-700 disabled:opacity-50 w-full mb-2"
        onClick={handlePay}
        disabled={loading}
      >
        {loading ? 'Processing...' : 'Pay with Razorpay'}
      </button>
      {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
    </div>
  );
}