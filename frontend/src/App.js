// App.js
import React, { useEffect, useState } from "react";
import CapsuleForm from "./components/CapsuleForm";
import CapsuleList from "./components/CapsuleList";
import AIChat from "./components/AIChat";
import { fetchCapsules } from "./api";
import background from "./assets/background.jpg";

function App() {
  const [capsules, setCapsules] = useState([]);

  const loadCapsules = async () => {
    try {
      const data = await fetchCapsules();
      setCapsules(data);
    } catch (err) {
      console.error("Failed to fetch capsules:", err);
    }
  };

  useEffect(() => {
    loadCapsules();
  }, []);

  return (
    <div
      className="App"
      style={{
        backgroundImage: `url(${background})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        minHeight: "100vh",
      }}
    >
      <h1>TIME CAPSULE</h1>
      <div className="main-content centered-main ai-layout">
        <div className="center-stack">
          <CapsuleForm onSaved={loadCapsules} />
          <h2 className="ivory-heading">Your Capsules</h2>
          <CapsuleList capsules={capsules} onDeleted={loadCapsules} />
        </div>
        <div className="ai-chat-fixed">
          <AIChat capsules={capsules} />
        </div>
      </div>
    </div>
  );
}

export default App;
