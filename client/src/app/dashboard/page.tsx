'use client';
import React, { useEffect } from 'react';
import { useAuthStore } from '@/store/useAuth';
import { useRouter } from 'next/navigation';

function Dashboard() {
  const router = useRouter();

  const user = useAuthStore((state) => state.user);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const checkAuth = useAuthStore((state) => state.checkAuth);

  useEffect(() => {
    const checkUserAuth = async () => {
      if (!isAuthenticated) {
        const token = await checkAuth();
        if (!token) {
          router.push('/login');
        }
      }
    };
    checkUserAuth();
  }, [isAuthenticated, checkAuth, router]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">User Profile</h2>
      <div className="space-y-4">
        <div>
          <label className="text-sm font-medium text-gray-500">Username</label>
          <p className="text-gray-900">{user?.username || 'Not available'}</p>
        </div>
        <div>
          <label className="text-sm font-medium text-gray-500">Email</label>
          <p className="text-gray-900">{user?.email || 'Not available'}</p>
        </div>
        <div>
          <label className="text-sm font-medium text-gray-500">Role</label>
          <p className="text-gray-900">{user?.role || 'Inactive'}</p>
        </div>
        <div>
          <label className="text-sm font-medium text-gray-500">Account Status</label>
          <p className="text-gray-900">{user?.is_active ? 'Active' : 'Inactive'}</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
