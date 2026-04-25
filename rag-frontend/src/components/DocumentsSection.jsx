import { useEffect, useState } from "react";
import api from "../api";

function DocumentsSection({ refreshTrigger, documents, setDocuments }) {
  const [totalChunks, setTotalChunks] = useState(0);
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await api.get("/admin/documents");
      setDocuments(response.data.documents || []);
      setTotalChunks(response.data.total_chunks || 0);
    } catch (error) {
      console.error("Failed to fetch documents:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (source) => {
    const confirmDelete = window.confirm(`Delete "${source}" from vector DB?`);
    if (!confirmDelete) return;

    try {
      await api.delete(`/admin/documents?source=${encodeURIComponent(source)}`);
      fetchDocuments();
    } catch (error) {
      console.error("Delete failed:", error);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [refreshTrigger]);

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h2>Indexed Documents</h2>
          <p>Manage documents stored in Chroma vector database.</p>
        </div>
        <span className="pill">{totalChunks} chunks</span>
      </div>

      {loading && <p className="muted">Loading documents...</p>}

      {!loading && documents.length === 0 && (
        <div className="empty-state">
          <p>No documents indexed yet.</p>
        </div>
      )}

      <div className="doc-list">
        {documents.map((doc, index) => (
          <div className="doc-item" key={index}>
            <div>
              <p className="doc-title">{doc.source}</p>
              <p className="doc-meta">{doc.chunk_count} chunks indexed</p>
            </div>

            <button className="danger-btn" onClick={() => handleDelete(doc.source)}>
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DocumentsSection;