import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const LogsPage = () => {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [logsPerPage, setLogsPerPage] = useState(10); // Default 10 logs per page
    const navigate = useNavigate();

    useEffect(() => {
        fetch("http://192.168.56.16:8000/checklogs")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch logs");
                }
                return response.json();
            })
            .then((data) => {
                if (data.status === "success") {
                    // Sort logs by date (latest first)
                    const sortedLogs = data.response.sort((a, b) =>
                        new Date(b.date) - new Date(a.date)
                    );
                    setLogs(sortedLogs);
                } else {
                    throw new Error("Failed to load logs");
                }
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    const handleLogClick = (logFile) => {
        navigate(`/log/${logFile}`);
    };

    const handleDelete = (logFile) => {
        if (!window.confirm(`Are you sure you want to delete ${logFile}?`)) return;

        fetch(`http://192.168.56.16:8000/delog/${logFile}`, { method: "DELETE" })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    setLogs((prevLogs) => prevLogs.filter((log) => log.name !== logFile));
                } else {
                    throw new Error(data.response || "Failed to delete log");
                }
            })
            .catch((err) => {
                alert(`Error: ${err.message}`);
            });
    };

    // Pagination Logic
    const indexOfLastLog = currentPage * logsPerPage;
    const indexOfFirstLog = indexOfLastLog - logsPerPage;
    const currentLogs = logs.slice(indexOfFirstLog, indexOfLastLog);
    const totalPages = Math.ceil(logs.length / logsPerPage);

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
            <h1 className="text-2xl font-bold mb-4">RANCID Logs</h1>

            {/* Dropdown for logs per page */}
            <div className="mb-4 flex items-center gap-2">
                <label className="font-medium">Show: </label>
                <select
                    className="border rounded px-2 py-1"
                    value={logsPerPage}
                    onChange={(e) => {
                        setLogsPerPage(Number(e.target.value));
                        setCurrentPage(1); // Reset to first page on change
                    }}
                >
                    <option value="10">10</option>
                    <option value="25">25</option>
                    <option value="100">100</option>
                </select>
            </div>

            {/* Logs List */}
            <ul className="border border-gray-300 rounded-lg shadow-md p-4">
                {currentLogs.map((log, index) => (
                    <li
                        key={index}
                        className="flex justify-between items-center p-2 border-b border-gray-200 last:border-none"
                    >
                        <span
                            className="font-medium cursor-pointer hover:text-blue-500"
                            onClick={() => handleLogClick(log.name)}
                        >
                            {log.name}
                        </span>
                        <div className="flex items-center gap-4">
                            <span className="text-gray-500 text-sm">Log on: {log.date}</span>
                            <button
                                className="bg-red-600 text-white px-3 py-1 rounded-md hover:bg-red-700"
                                onClick={() => handleDelete(log.name)}
                            >
                                Delete
                            </button>
                        </div>
                    </li>
                ))}
            </ul>

            {/* Pagination Controls */}
            <div className="flex justify-center items-center mt-4 gap-2">
                <button
                    className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:bg-gray-200"
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                >
                    Previous
                </button>
                <span className="font-medium">
                    Page {currentPage} of {totalPages}
                </span>
                <button
                    className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:bg-gray-200"
                    disabled={currentPage === totalPages}
                    onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                >
                    Next
                </button>
            </div>
        </div>
    );
};

export default LogsPage;
