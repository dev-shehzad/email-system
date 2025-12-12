import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Sidebar from "./components/layout/Sidebar/Sidebar";
import Topbar from "./components/layout/Topbar/Topbar";
import ProtectedRoute from "./components/auth/ProtectedRoute";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Contacts from "./pages/Contacts";
import CampaignCreate from "./pages/CampaignCreate";
import CampaignList from "./pages/CampaignList";

function App() {
  const token = localStorage.getItem("token");
  const isAuthenticated = !!token;

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={isAuthenticated ? <Navigate to="/" replace /> : <Login />} />
        
        <Route
          path="/*"
          element={
            <ProtectedRoute>
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />

        <div className="flex-1 flex flex-col overflow-hidden w-full lg:w-auto">
          <Topbar />

          <main className="flex-1 overflow-y-auto pt-14 sm:pt-16 lg:pt-0">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/contacts" element={<Contacts />} />
              <Route path="/campaign/create" element={<CampaignCreate />} />
              <Route path="/campaigns" element={<CampaignList />} />
            </Routes>
          </main>
        </div>
      </div>
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;