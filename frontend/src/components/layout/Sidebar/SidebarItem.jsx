const tooltips = {
  "Dashboard": "View analytics and overview of your email marketing performance",
  "Contacts": "Manage your contact list and upload new contacts via CSV",
  "Create Campaign": "Design and create a new email campaign to send to your audience",
  "All Campaigns": "View and manage all your email campaigns"
};

function SidebarItem({ label, icon, active }) {
  return (
    <div
      className={`px-3 py-2.5 rounded-lg cursor-pointer transition-all duration-200 flex items-center gap-2.5 group ${
        active
          ? "bg-blue-600 text-white shadow-md shadow-blue-500/20"
          : "hover:bg-gray-700/50 text-gray-300 hover:text-white"
      }`}
      title={tooltips[label]}
    >
      {icon && <span className="text-base flex-shrink-0">{icon}</span>}
      <span className="font-medium text-sm truncate">{label}</span>
    </div>
  );
}

export default SidebarItem;


