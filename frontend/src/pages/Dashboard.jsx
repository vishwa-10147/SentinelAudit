import { useAuth } from '../AuthContext';
import LogoutButton from '../components/LogoutButton';
import DashboardStats from '../components/DashboardStats';
import RecentReports from '../components/RecentReports';
import DetectionsTable from '../components/DetectionsTable';

export default function Dashboard() {
  const { user, loading } = useAuth();
  if (loading) return <div className="p-8">Loading...</div>;
  if (!user) return <div className="p-8">Not authenticated.</div>;
  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <LogoutButton />
      </div>
      <div className="mb-2 text-gray-700">Welcome, <span className="font-semibold">{user.name || user.email}</span></div>
      <DashboardStats />
      <RecentReports />
      <DetectionsTable />
    </div>
  );
}