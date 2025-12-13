import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../utils/axios";
import Tooltip from "../components/common/Tooltip";

export default function CampaignList() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(null);
  const [message, setMessage] = useState("");

  const load = async () => {
    try {
      setLoading(true);
      const res = await api.get("/campaigns/all");
      setItems(res.data);
    } catch (error) {
      setMessage("❌ Failed to load campaigns");
    } finally {
      setLoading(false);
    }
  };

  const sendNow = async (id) => {
    if (!confirm("Are you sure you want to send this campaign to all active contacts?")) {
      return;
    }

    setSending(id);
    setMessage("");
    
    try {
      const res = await api.post("/campaign/send", null, {
        params: { campaign_id: id }
      });
      setMessage(`✅ Campaign sent successfully! Total sent: ${res.data.total_sent}`);
      setTimeout(() => setMessage(""), 5000);
    } catch (error) {
      setMessage("❌ Failed to send campaign");
    } finally {
      setSending(null);
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-10 w-10 border-2 border-blue-200 border-t-blue-600"></div>
          <p className="mt-3 text-sm text-gray-600">Loading campaigns...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-3 sm:p-4 md:p-6 max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4 sm:mb-6">
        <div className="flex-1 min-w-0">
          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-gray-800 mb-1 truncate">All Campaigns</h2>
          <p className="text-xs sm:text-sm text-gray-600 hidden sm:block">Manage and send your email campaigns</p>
        </div>
        <div className="flex gap-2 w-full sm:w-auto">
          <Tooltip content="Reload the campaigns list" position="bottom">
        <button
          onClick={load}
              className="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-all font-medium"
        >
          Refresh
        </button>
          </Tooltip>
          <Link
            to="/campaign/create"
            className="px-3 sm:px-4 py-2 text-xs sm:text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all font-medium whitespace-nowrap flex-1 sm:flex-none text-center"
          >
            + New Campaign
          </Link>
        </div>
      </div>

      {message && (
        <div className={`mb-4 p-4 rounded-lg flex items-start gap-3 animate-in fade-in slide-in-from-top-2 duration-300 ${
          message.includes("✅") 
            ? "bg-green-50 text-green-800 border border-green-200" 
            : "bg-red-50 text-red-800 border border-red-200"
        }`}>
          <span className="text-lg flex-shrink-0">{message.includes("✅") ? "✅" : "❌"}</span>
          <p className="flex-1 text-sm sm:text-base">{message}</p>
        </div>
      )}

      {items.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 sm:p-12 text-center">
          <div className="max-w-md mx-auto">
            <div className="text-6xl mb-4">📧</div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">No Campaigns Yet</h3>
            <p className="text-gray-600 mb-6">Get started by creating your first email campaign to engage with your audience</p>
            <Link
              to="/campaign/create"
              className="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all font-medium"
            >
              Create Your First Campaign
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid gap-3 sm:gap-4">
          {items.map(c => (
            <div
              key={c.id}
              className="bg-white rounded-xl shadow-sm hover:shadow-md transition-all p-4 sm:p-6 border border-gray-100"
            >
              <div className="flex flex-col sm:flex-row justify-between items-start gap-3 sm:gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="inline-block px-2.5 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold">
                      ID: {c.id}
                    </span>
                  </div>
                  <h4 className="text-lg sm:text-xl font-bold text-gray-800 mb-1.5 truncate">{c.subject}</h4>
                  <p className="text-sm text-gray-600 truncate">
                    <span className="font-semibold">From:</span> {c.sender}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">Click 'Send Campaign' to deliver to all active contacts</p>
                </div>
                <Tooltip content="Send this campaign to all active contacts in your database" position="left">
                <button
                  onClick={() => sendNow(c.id)}
                  disabled={sending === c.id}
                    className="w-full sm:w-auto px-5 py-2 text-sm bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md whitespace-nowrap"
                >
                  {sending === c.id ? "Sending..." : "Send Campaign"}
                </button>
                </Tooltip>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

