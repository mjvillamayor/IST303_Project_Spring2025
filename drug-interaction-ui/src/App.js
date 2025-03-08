import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
    const [drugName, setDrugName] = useState("");
    const [interactionData, setInteractionData] = useState(null);
    const [error, setError] = useState(null);

    const checkInteractions = async () => {
        setError(null);
        setInteractionData(null);

        try {
            const response = await fetch("http://127.0.0.1:5000/api/interactions", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ drug_names: [drugName] })
            });

            if (!response.ok) {
                throw new Error("Failed to fetch interactions.");
            }

            const data = await response.json();
            setInteractionData(data);
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="container mt-5">
            <h2 className="mb-4 text-center">Drug Interaction Checker</h2>
            <div className="mb-3">
                <label className="form-label">Enter Drug Name</label>
                <input
                    type="text"
                    className="form-control"
                    value={drugName}
                    onChange={(e) => setDrugName(e.target.value)}
                />
            </div>
            <button className="btn btn-primary" onClick={checkInteractions}>
                Check Interactions
            </button>

            {error && (
                <div className="alert alert-danger mt-3">
                    {error}
                </div>
            )}

            {interactionData && (
                <div className="alert alert-success mt-3">
                    <h5>Drug Interactions:</h5>
                    <pre>{JSON.stringify(interactionData, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}

export default App;
