import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../utils/axios";
import Tooltip from "../components/common/Tooltip";
import HelpIcon from "../components/common/HelpIcon";

export default function CampaignCreate() {
  const navigate = useNavigate();
  const [subject, setSubject] = useState("");
  const [sender, setSender] = useState("");
  const [html, setHtml] = useState("");
  const [testEmail, setTestEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [testing, setTesting] = useState(false);
  const [message, setMessage] = useState("");
  const [campaignId, setCampaignId] = useState(null);

  const create = async () => {
    if (!subject || !sender || !html) {
      setMessage("Please fill all fields");
      return;
    }

    setLoading(true);
    setMessage("");
    
    try {
      const res = await api.post("/campaign/create", null, {
        params: { subject, sender, html }
      });

      setMessage(`✅ Campaign Created! ID: ${res.data.id}`);
      setCampaignId(res.data.id);
      // Don't clear fields - allow sending test or editing
    } catch (error) {
      setMessage("❌ Error creating campaign: " + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const sendTest = async () => {
    if (!campaignId) {
      setMessage("Please create the campaign first");
      return;
    }
    
    if (!testEmail) {
      setMessage("Please enter a test email address");
      return;
    }

    setTesting(true);
    setMessage("");
    
    try {
      const res = await api.post("/campaign/test", null, {
        params: { campaign_id: campaignId, test_email: testEmail }
      });

      setMessage(`✅ Test email sent to ${testEmail}!`);
    } catch (error) {
      setMessage("❌ Error sending test email: " + (error.response?.data?.detail || error.message));
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="p-3 sm:p-4 md:p-6 max-w-2xl mx-auto">
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-5 md:p-6 lg:p-8">
        <div className="mb-4 sm:mb-6">
          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-gray-800 mb-2">Create New Campaign</h2>
          <p className="text-xs sm:text-sm text-gray-600">Design and configure your email campaign to send to your audience</p>
        </div>

        <div className="space-y-4 sm:space-y-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <label className="block text-sm font-semibold text-gray-700">
              Subject Line
            </label>
              <Tooltip content="This is what recipients will see in their inbox. Keep it concise and compelling!" position="top">
                <HelpIcon />
              </Tooltip>
            </div>
            <input
              type="text"
              placeholder="e.g., Special Offer: 50% Off This Week!"
              value={subject}
              onChange={e => setSubject(e.target.value)}
              className="w-full px-3 py-2.5 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              maxLength={100}
            />
            <p className="text-xs text-gray-500 mt-1">{subject.length}/100 characters</p>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-2">
              <label className="block text-sm font-semibold text-gray-700">
              Sender Email
            </label>
              <Tooltip content="Must be from your verified domain. Recipients will see this as the 'From' address" position="top">
                <HelpIcon />
              </Tooltip>
            </div>
            <input
              type="email"
              placeholder="noreply@yourdomain.com"
              value={sender}
              onChange={e => setSender(e.target.value)}
              className="w-full px-3 py-2.5 text-sm sm:text-base border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
            />
            <p className="text-xs text-gray-500 mt-1">Use an email from your verified domain (e.g., yourdomain.com)</p>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-2">
              <label className="block text-sm font-semibold text-gray-700">
              HTML Content
            </label>
              <Tooltip content="Write your email content in HTML. You can include links, images, and styled content" position="top">
                <HelpIcon />
              </Tooltip>
            </div>
            <textarea
              placeholder="<h1>Welcome!</h1><p>Your email content here...</p>"
              rows={12}
              value={html}
              onChange={e => setHtml(e.target.value)}
              className="w-full px-3 py-2.5 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all font-mono"
            />
            <p className="text-xs text-gray-500 mt-1">Tip: Use HTML tags for formatting. Links should use full URLs (https://...)</p>
          </div>

          {campaignId && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-start gap-2 mb-3">
                <span className="text-blue-600 text-lg">✅</span>
                <div>
                  <h4 className="text-sm font-semibold text-blue-900 mb-1">Campaign Created Successfully!</h4>
                  <p className="text-xs text-blue-700">Campaign ID: {campaignId}. Send a test email to preview before sending to all contacts.</p>
                </div>
              </div>
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <label className="block text-sm font-semibold text-gray-700">
                    Send Test Email
                  </label>
                    <Tooltip content="Send a test email to yourself to preview how it will look to recipients" position="top">
                      <HelpIcon />
                    </Tooltip>
                  </div>
                  <input
                    type="email"
                    placeholder="your-email@example.com"
                    value={testEmail}
                    onChange={e => setTestEmail(e.target.value)}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                  />
                </div>
                <Tooltip content="Preview your campaign by sending it to your test email" position="top">
                <button
                  onClick={sendTest}
                  disabled={testing || !testEmail}
                    className="px-5 py-2 text-sm bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md whitespace-nowrap sm:mt-6"
                >
                  {testing ? "Sending..." : "Send Test"}
                </button>
                </Tooltip>
              </div>
            </div>
          )}

          {message && (
            <div className={`p-4 rounded-lg flex items-start gap-3 animate-in fade-in slide-in-from-top-2 duration-300 ${
              message.includes("✅") 
                ? "bg-green-50 text-green-800 border border-green-200" 
                : "bg-red-50 text-red-800 border border-red-200"
            }`}>
              <span className="text-lg flex-shrink-0">{message.includes("✅") ? "✅" : "❌"}</span>
              <p className="flex-1 text-sm sm:text-base">{message}</p>
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
            <button
              onClick={create}
              disabled={loading}
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md text-sm sm:text-base"
            >
              {loading ? "Creating..." : campaignId ? "Update Campaign" : "Create Campaign"}
            </button>
            {campaignId && (
              <button
                onClick={() => navigate("/campaigns")}
                className="px-6 bg-gray-600 hover:bg-gray-700 text-white font-medium py-2.5 rounded-lg transition-all duration-200 shadow-sm hover:shadow-md text-sm sm:text-base"
              >
                View Campaigns
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

