import { useState } from "react";
import api from "../api";

function UploadSection({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a PDF, DOCX, or TXT file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setMessage("");

      const response = await api.post("/ingest/upload", formData);

      setMessage(response.data.message || "File uploaded successfully.");
      setFile(null);

      if (onUploadSuccess) {
        onUploadSuccess();
      }
    } catch (error) {
      console.error("Upload error:", error);
      setMessage(error.response?.data?.detail || error.message || "Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h2>Upload Document</h2>
          <p>Add PDF, DOCX, or TXT files to your knowledge base.</p>
        </div>
      </div>

      <div className="upload-box">
        <input
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={(e) => setFile(e.target.files[0])}
        />

        {file && <p className="file-name">Selected: {file.name}</p>}

        <button className="primary-btn" onClick={handleUpload} disabled={loading}>
          {loading ? "Uploading..." : "Upload & Index"}
        </button>
      </div>

      {message && <p className="info-message">{message}</p>}
    </div>
  );
}

export default UploadSection;