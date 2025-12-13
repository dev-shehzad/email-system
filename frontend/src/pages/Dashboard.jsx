import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../utils/axios";
import StatsCard from "../components/dashboard/StatsCard";
import Tooltip from "../components/common/Tooltip";

function Dashboard() {
  const [stats, setStats] = useState({
    campaigns: 0,
    contacts: 0,
    active_contacts: 0,
    sent: 0,
    delivered: 0,
    opens: 0,
    clicks: 0,
    open_rate: 0,
    click_rate: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        // backend routes are registered under the /api prefix (see backend/main.py)
        const statsRes = await api.get("/stats/dashboard");
        setStats(statsRes.data);
      } catch (error) {
        console.error("Failed to load stats:", error);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-10 w-10 border-2 border-blue-200 border-t-blue-600"></div>
          <p className="mt-3 text-sm text-gray-600">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-3 sm:p-4 md:p-6">
      <div className="mb-4 sm:mb-6">
        <h1 className="text-xl sm:text-2xl md:text-3xl font-bold text-gray-800 mb-1">Dashboard</h1>
        <p className="text-xs sm:text-sm text-gray-600">Welcome to your Email Marketing System</p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-3 md:gap-4 mb-6">
        <StatsCard
          title="Total Campaigns"
          value={stats.campaigns}
          description="Email campaigns created"
          icon="📬"
          tooltip="Total number of email campaigns you've created in the system"
        />
        <StatsCard
          title="Total Contacts"
          value={stats.contacts}
          description="All contacts in database"
          icon="👥"
          tooltip="Total number of contacts stored in your database, including unsubscribed"
        />
        <StatsCard
          title="Active Contacts"
          value={stats.active_contacts}
          description="Not unsubscribed"
          icon="✓"
          tooltip="Contacts who are active and can receive emails (excluding unsubscribed)"
        />
        <StatsCard
          title="Emails Sent"
          value={stats.sent}
          description="Total emails sent"
          icon="✉️"
          tooltip="Total number of emails sent across all campaigns"
        />
        <StatsCard
          title="Delivered"
          value={stats.delivered}
          description="Successfully delivered"
          icon="📨"
          tooltip="Number of emails successfully delivered to recipients' mailboxes"
        />
        <StatsCard
          title="Opens"
          value={stats.opens}
          description={`Open rate: ${stats.open_rate}%`}
          icon="👁️"
          tooltip={`Total email opens. Current open rate: ${stats.open_rate}%`}
        />
        <StatsCard
          title="Clicks"
          value={stats.clicks}
          description={`Click rate: ${stats.click_rate}%`}
          icon="🖱️"
          tooltip={`Total link clicks. Current click rate: ${stats.click_rate}%`}
        />
        <StatsCard
          title="Open Rate"
          value={`${stats.open_rate}%`}
          description="Percentage of opens"
          icon="📊"
          tooltip="Percentage of delivered emails that were opened by recipients"
        />
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 sm:p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-gray-800">Quick Actions</h2>
            <p className="text-xs text-gray-500 mt-1">Get started with common tasks</p>
          </div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
          <div className="p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-md transition-all group">
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-base font-semibold text-gray-800">Create Campaign</h3>
              <span className="text-lg">📧</span>
            </div>
            <p className="text-sm text-gray-600 mb-3">Design and send personalized email campaigns to your audience</p>
            <Link
              to="/campaign/create"
              className="inline-flex items-center gap-1 px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all font-medium group-hover:gap-2"
            >
              Create Now <span>→</span>
            </Link>
          </div>
          <div className="p-4 border border-gray-200 rounded-lg hover:border-green-500 hover:shadow-md transition-all group">
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-base font-semibold text-gray-800">Upload Contacts</h3>
              <span className="text-lg">📥</span>
            </div>
            <p className="text-sm text-gray-600 mb-3">Import contacts from a CSV file to build your mailing list</p>
            <Link
              to="/contacts"
              className="inline-flex items-center gap-1 px-4 py-2 text-sm bg-green-600 hover:bg-green-700 text-white rounded-lg transition-all font-medium group-hover:gap-2"
            >
              Upload Now <span>→</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;


