import { useAuth } from '../AuthContext';

export default function LogoutButton() {
  const { logout, user } = useAuth();
  if (!user) return null;
  return (
    <button
      className="ml-4 px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
      onClick={logout}
    >
      Logout
    </button>
  );
}
