import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const RouterLogs = () => {
    const [configs, setConfigs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetch("http://192.168.56.16:8000/getrouter")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch configs");
                }
                return response.json();
            })
            .then((data) => {
                if (data.status === "success") {
                    // Filter configs to only include valid IPv4 addresses
                    const ipv4Regex = /^(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$/;

                    const validConfigs = data.response.filter((config) => ipv4Regex.test(config));
                    setConfigs(validConfigs);
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


    const handleConfigClick = (logfile) => {
        navigate(`/rlogs/${logfile}`);
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
                className="text-xl bg-slate-950 rounded-lg text-white px-4 py-2 hover:bg-gray-700"
                onClick={() => navigate("/")}
            >Back</button>
            <h1 className="text-2xl font-bold mb-4 mt-10">Choose a Router</h1>
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

export default RouterLogs;
