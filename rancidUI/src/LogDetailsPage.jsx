import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";


const LogDetailsPage = () => {
    const { logName } = useParams();
    const [configDetail, setConfigDetail] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetch(`http://192.168.56.16:8000/log/${logName}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch config detail");
                }
                return response.json();
            })
            .then((data) => {
                if (data.status === "success") {
                    setConfigDetail(data.response);
                } else {
                    throw new Error("Failed to load config detail");
                }
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [logName]);

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
            >Back</button>
            <h1 className="text-2xl font-bold mb-4">Config Detail: {logName}</h1>
            <pre className="whitespace-pre-wrap border border-gray-300 rounded-lg p-4 bg-gray-50">
                {configDetail}
            </pre>
        </div>
    );
};

export default LogDetailsPage;
