import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const LogsPage = () => {
    const [configs, setConfigs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetch("http://192.168.56.16:8000/checklogs")
          .then((response) => {
            if (!response.ok) {
              throw new Error("Failed to fetch configs");
            }
            return response.json();
          })
          .then((data) => {
            if (data.status === "success") {
              // Assuming data.response is an array of log names
              const sortedLogs = data.response.sort((a, b) => a.localeCompare(b)); // Sort alphabetically
              setConfigs(sortedLogs);
            } else {
              throw new Error("Failed to load configs");
            }
            setLoading(false);
          })
          .catch((err) => {
            setError(err.message);
            setLoading(false);
          });
      }, []);
      

    const handleConfigClick = (logFile) => {
        navigate(`/log/${logFile}`);
    };

    if (loading) {
        return <div className="text-center p-4">Loading...</div>;
    }

    if (error) {
        return <div className="text-center p-4 text-red-500">Error: {error}</div>;
    }

    return (
        <div className="p-4">
            <button
                className="text-xl bg-slate-950 rounded-lg text-white px-4 py-2 m-2 hover:bg-gray-700"
                onClick={() => navigate("/")}
            >
                Back
            </button>
            <h1 className="text-2xl font-bold mb-4">rancid-run Logs</h1>
            <ul className="border border-gray-300 rounded-lg shadow-md p-4">
                {configs.map((config, index) => (
                    <li
                        key={index}
                        className="p-2 border-b border-gray-200 last:border-none cursor-pointer hover:bg-gray-100"
                        onClick={() => handleConfigClick(config)}
                    >
                        {config}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default LogsPage;
