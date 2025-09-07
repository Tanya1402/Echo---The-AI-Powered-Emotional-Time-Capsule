// components/CapsuleForm.js
import React, { useState } from "react";
import { saveCapsule } from "../api";

export default function CapsuleForm({ onSaved }) {
  const [title, setTitle] = useState("");
  const [message, setMessage] = useState("");
  const [futureDate, setFutureDate] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await saveCapsule({ title, message, future_date: futureDate });
      setTitle("");
      setMessage("");
      setFutureDate("");
      if (onSaved) onSaved();
    } catch (err) {
      console.error(err);
      alert("Failed to save capsule");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="capsule-form">
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <textarea
        placeholder="Message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        required
      ></textarea>
      <input
        type="date"
        value={futureDate}
        onChange={(e) => setFutureDate(e.target.value)}
        required
      />
      <button type="submit">Save Capsule</button>
    </form>
  );
}
