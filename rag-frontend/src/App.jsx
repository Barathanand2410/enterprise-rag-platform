import { useEffect, useState } from "react";
import UploadSection from "./components/UploadSection";
import QuerySection from "./components/QuerySection";
import AnswerSection from "./components/AnswerSection";
import DocumentsSection from "./components/DocumentsSection";
import AuthPage from "./components/AuthPage";
import "./App.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("rag_token"));
  const [result, setResult] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    const storedToken = localStorage.getItem("rag_token");
    if (storedToken) setToken(storedToken);
  }, []);

  const handleUploadSuccess = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  const handleLogout = () => {
    localStorage.removeItem("rag_token");
    setToken(null);
    setResult(null);
  };

  if (!token) {
    return <AuthPage onAuthSuccess={setToken} />;
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Enterprise RAG Platform</h1>
          <p>
            Upload documents, ask questions, and get grounded answers with
            citations.
          </p>
        </div>

        <div className="header-actions">
          <span className="status-badge">AI Knowledge Assistant</span>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <main className="container">
        <section className="grid-two">
          <UploadSection onUploadSuccess={handleUploadSuccess} />
          <DocumentsSection
            refreshTrigger={refreshTrigger}
            documents={documents}
            setDocuments={setDocuments}
          />
        </section>

        <section className="grid-one">
          <QuerySection setResult={setResult} documents={documents} />
        </section>

        <section className="grid-one">
          <AnswerSection result={result} />
        </section>
      </main>
    </div>
  );
}

export default App;