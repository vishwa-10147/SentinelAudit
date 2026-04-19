import PricingCards from '../components/PricingCards';
import FeatureBlocks from '../components/FeatureBlocks';

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 to-white dark:from-gray-900 dark:to-gray-800">
      <header className="py-8 flex flex-col items-center">
        <h1 className="text-5xl font-extrabold text-purple-900 mb-4 tracking-tight">Know your network.<br className="md:hidden" /> Before attackers do.</h1>
        <p className="mb-6 text-lg text-gray-700 dark:text-gray-200 max-w-xl text-center">
          AI-powered network security audit SaaS for Indian SMEs. Get a professional security report in 10 minutes — no security team required.
        </p>
        <div className="flex gap-4">
          <a href="/register" className="px-8 py-3 bg-purple-600 text-white rounded-lg text-lg font-semibold shadow hover:bg-purple-700">Get Your Free Sample Report</a>
          <a href="/login" className="px-8 py-3 border border-purple-600 text-purple-700 rounded-lg text-lg font-semibold hover:bg-purple-50">Login</a>
        </div>
      </header>
      <FeatureBlocks />
      <section className="max-w-5xl mx-auto mt-16 mb-12 px-4">
        <h2 className="text-3xl font-bold text-center mb-4">Pricing</h2>
        <PricingCards />
      </section>
    </div>
  );
}