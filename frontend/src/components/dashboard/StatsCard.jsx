import Tooltip from "../common/Tooltip";

function StatsCard({ title, value, description, icon, tooltip }) {
  return (
    <div className="p-4 bg-white rounded-xl border border-gray-100 hover:shadow-lg hover:border-blue-200 transition-all duration-200 group">
      <div className="flex items-center justify-between mb-3">
        <Tooltip content={tooltip || description} position="top">
          <h3 className="text-xs font-semibold text-gray-600 uppercase tracking-wide cursor-help">{title}</h3>
        </Tooltip>
        {icon && (
          <Tooltip content={tooltip || description} position="top">
            <span className="text-xl cursor-help">{icon}</span>
          </Tooltip>
        )}
      </div>
      <p className="text-3xl font-bold text-gray-800 mb-1">{value}</p>
      {description && (
        <p className="text-xs text-gray-500">{description}</p>
      )}
    </div>
  );
}

export default StatsCard;


