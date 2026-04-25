import { useState } from "react";
import api from "../api";

function AuthPage({ onAuthSuccess }) {
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("Barath");
  const [email, setEmail] = useState("barath@test.com");
  const [password, setPassword] = useState("123456");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setMessage("");

      if (mode === "register") {
        const response = await api.post("/auth/register", {
          username,
          email,
          password,
        });

        setMessage(response.data.message || "Registered successfully. Please login.");
        setMode("login");
        return;
      }

      const response = await api.post("/auth/login", {
        email,
        password,
      });

      localStorage.setItem("rag_token", response.data.access_token);
      onAuthSuccess(response.data.access_token);
    } catch (error) {
      setMessage(error.response?.data?.detail || error.message || "Authentication failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Enterprise RAG Platform</h1>
        <p>Login to access your AI document assistant.</p>

        <div className="auth-tabs">
          <button
            className={mode === "login" ? "active-tab" : ""}
            onClick={() => setMode("login")}
          >
            Login
          </button>
          <button
            className={mode === "register" ? "active-tab" : ""}
            onClick={() => setMode("register")}
          >
            Register
          </button>
        </div>

        {mode === "register" && (
          <input
            className="auth-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        )}

        <input
          className="auth-input"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="auth-input"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="primary-btn auth-btn" onClick={handleSubmit} disabled={loading}>
          {loading ? "Please wait..." : mode === "login" ? "Login" : "Register"}
        </button>

        {message && <p className="info-message">{message}</p>}
      </div>
    </div>
  );
}

export default AuthPage;