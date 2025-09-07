// components/AIChat.js
import React, { useState, useRef, useEffect } from "react";

export default function AIChat({ capsules }) {
  const [prompt, setPrompt] = useState("");
  const [responses, setResponses] = useState([]);
  const chatEndRef = useRef(null);

  const handleSend = async () => {
    if (!prompt.trim()) return;
    try {
      const res = await fetch("http://127.0.0.1:5000/api/ai-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, capsules }),
      });
      const data = await res.json();
      if (data.response) {
        setResponses([...responses, { user: prompt, bot: data.response }]);
        setPrompt("");
      }
    } catch (err) {
      console.error(err);
      alert("AI chat failed. Try again.");
    }
  };

  const handleClear = () => {
    setResponses([]);
    setPrompt("");
  };

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [responses]);

  return (
    <div className="ai-chat">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
  <h2 className="echo-heading" style={{ margin: 0 }}>Echo</h2>
        <button className="clear-chat-btn" onClick={handleClear} title="Clear chat" style={{ marginLeft: 8 }}>New Chat</button>
      </div>
      <div className="chat-window fixed-chat-window">
        {responses.map((r, idx) => (
          <div key={idx} className="chat-message">
            <p className="user-msg"><strong>You:</strong> {r.user}</p>
            <p className="bot-msg"><strong>Shadow:</strong> {r.bot}</p>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <textarea
        className="ivory-textarea"
        placeholder="How are you feeling today?"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
