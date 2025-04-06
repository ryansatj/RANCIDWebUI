import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuthRedirect from "./Auth/useAuthRedirect";

const ConfigsPage = () => {
    useAuthRedirect();
    const [configs, setConfigs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    
    // Get user from local storage
    const user = JSON.parse(localStorage.getItem("user")) || { name: "Guest" };

    useEffect(() => {
        fetch("http://192.168.56.16:8000/getconfigs")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch configs");
                }
                return response.text();
            })
            .then((rawText) => {
                console.log("Raw Response:", rawText);
                try {
                    const data = JSON.parse(rawText);
                    if (data.status === "success" && data.response.data) {
                        const ipv4Regex = /^(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$/;
                        
                        const validConfigs = data.response.data.filter((config) =>
                            ipv4Regex.test(config.name)
                        );

                        setConfigs(validConfigs);
                    } else {
                        throw new Error("Invalid response format");
                    }
                } catch (jsonError) {
                    throw new Error("Invalid JSON format: " + jsonError.message);
                }

                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    const handleConfigClick = (configName) => {
        navigate(`/config/${configName}`);
    };

    const handleSignOut = () => {
        localStorage.removeItem("user");
        navigate("/");
    };

    if (loading) {
        return <div className="text-center p-4">Loading...</div>;
    }

    if (error) {
        return <div className="text-center p-4 text-red-500">Error: {error}</div>;
    }

    return (
        <div className="p-4">
            {/* Header Section */}
            <div className="flex justify-between items-center">
                <div>
                    <span className="text-3xl font-bold mb-4 rounded-lg bg-black text-white px-2 mr-2">
                        RANCID Web UI
                    </span>
                    <span className="text-xl font-bold mb-4">by Ryan</span>
                </div>
                <div className="flex items-center gap-4">
                    <span className="text-lg font-semibold">Hi, {user.name}!</span>
                    <button
                        onClick={handleSignOut}
                        className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
                    >
                        Sign Out
                    </button>
                </div>
            </div>

            {/* Configurations Section */}
            <h1 className="text-2xl font-bold mb-4 mt-10">
                All Router Backup Configuration
            </h1>
            <ul className="border border-gray-300 rounded-lg shadow-md p-4">
                {configs.map((config, index) => (
                    <li
                        key={index}
                        className="p-3 border-b border-gray-200 last:border-none cursor-pointer hover:bg-gray-100 flex justify-between"
                        onClick={() => handleConfigClick(config.name)}
                    >
                        <span className="font-semibold">
                            {config.hostname} ({config.name})
                        </span>
                        <span className="text-gray-500 text-sm">
                            Last Backup on {config.date}
                        </span>
                    </li>
                ))}
            </ul>

            {/* Navigation Buttons */}
            <div className="mt-4 flex gap-4">
                <button
                    className="text-xl bg-slate-950 rounded-lg text-white px-4 py-2 hover:bg-gray-700"
                    onClick={() => navigate("/logs")}
                >
                    Run Logs
                </button>
                <button
                    className="text-xl bg-slate-950 rounded-lg text-white px-4 py-2 hover:bg-gray-700"
                    onClick={() => navigate("/rlogs")}
                >
                    Router Logs
                </button>
            </div>
        </div>
    );
};

export default ConfigsPage;
