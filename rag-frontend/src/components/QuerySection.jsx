import { useState } from "react";
import api from "../api";

function QuerySection({ setResult, documents }) {
  const [question, setQuestion] = useState("");
  const [source, setSource] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) {
      setResult({
        error: "Please enter a question.",
      });
      return;
    }

    try {
      setLoading(true);
      setResult(null);

      const payload = {
        question: question.trim(),
        top_k: 3,
        source: source || null,
        history: [],
      };

      const response = await api.post("/query/ask", payload);
      setResult(response.data);
    } catch (error) {
      console.error("Query error:", error);
      setResult({
        error: error.response?.data?.detail || error.message || "Query failed.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card query-card">
      <div className="card-header">
        <div>
          <h2>Ask a Question</h2>
          <p>Ask anything from your uploaded documents.</p>
        </div>
      </div>

      <textarea
        className="question-input"
        rows="5"
        placeholder="Example: What work was done on Day 27?"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <div className="query-controls">
        <select
          className="source-select"
          value={source}
          onChange={(e) => setSource(e.target.value)}
        >
          <option value="">All documents</option>
          {documents.map((doc, index) => (
            <option key={index} value={doc.source}>
              {doc.source}
            </option>
          ))}
        </select>

        <button className="primary-btn" onClick={handleAsk} disabled={loading}>
          {loading ? "Generating..." : "Ask"}
        </button>
      </div>
    </div>
  );
}

export default QuerySection;