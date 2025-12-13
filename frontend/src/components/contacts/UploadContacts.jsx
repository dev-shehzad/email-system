import { useState } from "react";
import api from "../../utils/axios";
import Tooltip from "../common/Tooltip";
import HelpIcon from "../common/HelpIcon";

function UploadContacts() {
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const upload = async () => {
    if (!file) {
      setMsg("Please select a CSV file first");
      return;
    }

    setLoading(true);
    setMsg("");
    setResult(null);

    console.log(`📤 Uploading CSV file: ${file.name}`);
    console.log(`📁 File size: ${(file.size / 1024).toFixed(2)} KB`);

    const fd = new FormData();
    fd.append("file", file);

    try {
      console.log("🔄 Sending request to backend...");
      const res = await api.post(
        "/contacts/upload",
        fd
      );

      console.log("✅ Upload successful!");
      console.log(`   ✓ Inserted: ${res.data.inserted} contacts`);
      console.log(`   ⚠ Skipped: ${res.data.skipped || 0} contacts`);
      console.log(`   📈 Total processed: ${res.data.total || 0} rows`);

      setResult(res.data);
      setMsg(`✅ Uploaded successfully!`);
      setFile(null);
    } catch (error) {
      console.error("❌ Upload failed:", error);
      console.error("Error details:", error.response?.data || error.message);
      setMsg("❌ Upload failed. Please check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto w-full">
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 sm:p-5 md:p-6 lg:p-8">
        <div className="mb-4 sm:mb-6">
          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-gray-800 mb-2">Upload Contacts</h2>
          <p className="text-xs sm:text-sm text-gray-600">Import contacts from a CSV file to build your mailing list</p>
        </div>

        <div className="space-y-4 sm:space-y-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <label className="block text-sm font-semibold text-gray-700">
              Select CSV File
            </label>
              <Tooltip content="CSV file must contain 'email' column. Optional: 'name' column. Maximum file size: 10MB" position="top">
                <HelpIcon />
              </Tooltip>
            </div>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 sm:p-6 text-center hover:border-blue-500 transition-all">
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setFile(e.target.files[0])}
                className="hidden"
                id="file-input"
              />
              <label
                htmlFor="file-input"
                className="cursor-pointer flex flex-col items-center"
              >
                <svg
                  className="w-10 h-10 sm:w-12 sm:h-12 text-gray-400 mb-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
                <span className="text-gray-600 font-medium">
                  {file ? file.name : "Click to select CSV file"}
                </span>
                {file && (
                  <span className="text-sm text-gray-500 mt-1">
                    {(file.size / 1024).toFixed(2)} KB
                  </span>
                )}
              </label>
            </div>
          </div>

          {msg && (
            <div className={`p-4 rounded-lg flex items-start gap-3 animate-in fade-in slide-in-from-top-2 duration-300 ${
              msg.includes("✅") 
                ? "bg-green-50 text-green-800 border border-green-200" 
                : "bg-red-50 text-red-800 border border-red-200"
            }`}>
              <span className="text-lg flex-shrink-0">{msg.includes("✅") ? "✅" : "❌"}</span>
              <p className="flex-1 text-sm sm:text-base">{msg}</p>
            </div>
          )}

          {result && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 sm:p-6 animate-in fade-in slide-in-from-bottom-2 duration-300">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-blue-600 text-lg">📊</span>
                <h3 className="font-semibold text-blue-900 text-sm sm:text-base">Upload Results</h3>
              </div>
              <div className="space-y-2.5 text-sm">
                <div className="flex justify-between items-center p-2 bg-white rounded">
                  <span className="text-blue-700 font-medium">Total Processed:</span>
                  <span className="font-bold text-blue-900">{result.total}</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-green-50 rounded">
                  <span className="text-green-700 font-medium">✓ Successfully Inserted:</span>
                  <span className="font-bold text-green-900">{result.inserted}</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-yellow-50 rounded">
                  <span className="text-yellow-700 font-medium">⚠ Skipped (duplicates/invalid):</span>
                  <span className="font-bold text-yellow-900">{result.skipped || 0}</span>
                </div>
              </div>
            </div>
          )}

          <button
            onClick={upload}
            disabled={!file || loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md text-sm sm:text-base"
          >
            {loading ? "Uploading..." : "Upload CSV"}
          </button>

          <div className="bg-blue-50 border border-blue-100 rounded-lg p-3 sm:p-4">
            <div className="flex items-start gap-2">
              <span className="text-blue-600 text-lg">💡</span>
              <div className="flex-1">
                <p className="text-xs sm:text-sm text-blue-900 font-medium mb-1">CSV Format Requirements:</p>
                <ul className="text-xs sm:text-sm text-blue-800 space-y-1 list-disc list-inside">
                  <li>Required column: <code className="bg-white px-1.5 py-0.5 rounded text-xs font-mono">email</code></li>
                  <li>Optional column: <code className="bg-white px-1.5 py-0.5 rounded text-xs font-mono">name</code></li>
                  <li>First row should contain column headers</li>
                  <li>Email addresses must be valid format</li>
                  <li>Duplicate emails will be automatically skipped</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UploadContacts;
