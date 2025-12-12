import { useNavigate } from "react-router-dom";
import Tooltip from "../../common/Tooltip";

function Topbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="w-full bg-white shadow-sm border-b border-gray-200 px-3 sm:px-4 py-2.5 sm:py-3 flex justify-between items-center">
      <div className="flex-1 min-w-0 ml-10 lg:ml-0">
        <h1 className="text-base sm:text-lg font-bold text-gray-800 truncate">Email Marketing Dashboard</h1>
        <p className="text-xs text-gray-500 hidden sm:block truncate">Manage your email campaigns and track performance</p>
      </div>
      <div className="flex items-center gap-1.5 sm:gap-3 ml-2 sm:ml-4 flex-shrink-0">
        <div className="text-right hidden md:block">
          <p className="text-sm font-semibold text-gray-800 truncate">Admin User</p>
          <p className="text-xs text-gray-500 truncate max-w-[120px]">admin@example.com</p>
        </div>
        <Tooltip content="Sign out of your account" position="bottom">
        <button
          onClick={handleLogout}
            className="px-2.5 sm:px-3 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-all font-medium whitespace-nowrap"
        >
          Logout
        </button>
        </Tooltip>
        <Tooltip content="Admin User Account" position="bottom">
          <div className="w-8 h-8 sm:w-10 sm:h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold text-sm sm:text-base flex-shrink-0 cursor-pointer hover:bg-blue-700 transition-colors">
          A
        </div>
        </Tooltip>
      </div>
    </div>
  );
}

export default Topbar;


