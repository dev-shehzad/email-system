import { useState, useEffect } from "react";
import SidebarItem from "./SidebarItem";
import { Link, useLocation } from "react-router-dom";

function Sidebar() {
  const location = useLocation();
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  // Close mobile menu on route change
  useEffect(() => {
    setIsMobileOpen(false);
  }, [location.pathname]);

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setIsMobileOpen(!isMobileOpen)}
        className="lg:hidden fixed top-3 left-3 z-50 p-2 bg-gray-900 hover:bg-gray-800 text-white rounded-lg shadow-lg transition-colors"
        aria-label="Toggle menu"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      {/* Mobile overlay */}
      {isMobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed lg:static inset-y-0 left-0 w-56 sm:w-64 bg-gradient-to-b from-gray-900 to-gray-800 text-white flex flex-col shadow-xl z-40 transform transition-transform duration-300 ease-in-out ${
          isMobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        <div className="p-4 border-b border-gray-700 flex items-center justify-between">
          <div className="flex-1 min-w-0">
            <h2 className="text-lg sm:text-xl font-bold mb-0.5 truncate">Email System</h2>
            <p className="text-gray-400 text-xs truncate">Marketing Platform</p>
          </div>
          {/* Close button for mobile */}
          <button
            onClick={() => setIsMobileOpen(false)}
            className="lg:hidden ml-2 p-1.5 hover:bg-gray-700 rounded transition-colors flex-shrink-0"
            aria-label="Close menu"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
      </div>

        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <Link to="/">
          <SidebarItem label="Dashboard" icon="📊" active={location.pathname === "/"} />
        </Link>

        <Link to="/contacts">
          <SidebarItem label="Contacts" icon="👥" active={location.pathname === "/contacts"} />
        </Link>

        <Link to="/campaign/create">
          <SidebarItem label="Create Campaign" icon="✏️" active={location.pathname === "/campaign/create"} />
        </Link>

        <Link to="/campaigns">
          <SidebarItem label="All Campaigns" icon="📬" active={location.pathname === "/campaigns"} />
        </Link>
      </nav>

        <div className="p-3 border-t border-gray-700">
          <p className="text-xs text-gray-500 text-center">© {new Date().getFullYear()}</p>
      </div>
    </div>
    </>
  );
}

export default Sidebar;


