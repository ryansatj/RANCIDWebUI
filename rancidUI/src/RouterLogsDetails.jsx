import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const RouterLogsDetails = () => {
    const { logname } = useParams();
    const [configDetail, setConfigDetail] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [r1, setR1] = useState("");
    const [r2, setR2] = useState("");
    const [diffResult, setDiffResult] = useState(null);
    const [diffError, setDiffError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        let isMounted = true;
        setLoading(true);
        setError(null);

        const fetchLogDetails = async () => {
            try {
                const response = await fetch(`http://192.168.56.16:8000/rlog/${logname}`);
                if (!response.ok) throw new Error("Failed to fetch log details");
                
                const data = await response.json();
                console.log("Log API Response:", data); // Debugging

                if (isMounted) {
                    if (data.status === "success" && data.response) {
                        setConfigDetail(data.response);
                    } else {
                        throw new Error("Failed to load log details");
                    }
                    setLoading(false);
                }
            } catch (err) {
                if (isMounted) {
                    setError(err.message);
                    setLoading(false);
                }
            }
        };

        fetchLogDetails();
        return () => {
            isMounted = false;
        };
    }, [logname]);

    const handleCompare = async () => {
        setDiffResult(null);
        setDiffError(null);

        try {
            const response = await fetch(`http://192.168.56.16:8000/diff/${logname}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ r1, r2 }),
            });

            if (!response.ok) throw new Error("Failed to fetch diff result");
            
            const data = await response.json();

            if (data.status === "success" && data.output) {
                setDiffResult(data.output);
            } else {
                throw new Error(data.output || "No differences found.");
            }
        } catch (err) {
            setDiffError(err.message);
        }
    };

    if (loading) return <div className="text-center p-4">Loading...</div>;
    if (error) return <div className="text-center p-4 text-red-500">Error: {error}</div>;

    return (
        <div className="p-4">
            <button
                className="text-xl bg-slate-950 rounded-lg text-white px-4 py-2 mb-4 hover:bg-gray-700"
                onClick={() => navigate("/rlogs")}
            >
                Back
            </button>

            <h1 className="text-2xl font-bold mb-4">{logname} Log Details</h1>
            <pre className="whitespace-pre-wrap border border-gray-300 rounded-lg p-4 bg-gray-50">
                {configDetail}
            </pre>

            <div className="mt-6 p-4 border-t">
                <h2 className="text-xl font-semibold mb-2">Compare Log Versions</h2>
                <div className="flex gap-2">
                    <input
                        type="text"
                        placeholder="Version 1 (r1)"
                        value={r1}
                        onChange={(e) => setR1(e.target.value)}
                        className="border p-2 rounded w-1/2"
                    />
                    <input
                        type="text"
                        placeholder="Version 2 (r2)"
                        value={r2}
                        onChange={(e) => setR2(e.target.value)}
                        className="border p-2 rounded w-1/2"
                    />
                    <button
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        onClick={handleCompare}
                    >
                        Compare
                    </button>
                </div>
            </div>

            {diffError && <div className="text-red-500 mt-4">{diffError}</div>}
            {diffResult !== null && (
                <div className="mt-4 p-4 border border-gray-300 rounded-lg bg-gray-100">
                    <h2 className="text-lg font-semibold mb-2">Comparison Result</h2>
                    <pre className="whitespace-pre-wrap">{diffResult}</pre>
                </div>
            )}
        </div>
    );
};

export default RouterLogsDetails;
