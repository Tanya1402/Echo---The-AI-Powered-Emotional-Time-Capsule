// components/CapsuleList.js
import React from "react";
import { deleteCapsule } from "../api";

export default function CapsuleList({ capsules, onDeleted }) {
  const handleDelete = async (idx) => {
    if (window.confirm("Are you sure you want to delete this capsule?")) {
      try {
        await deleteCapsule(idx); // pass the array index, not id
        if (onDeleted) onDeleted(); // refresh capsule list
      } catch (err) {
        console.error(err);
        alert("Failed to delete capsule");
      }
    }
  };

  if (!capsules.length) return <p className="no-capsules">No capsules yet.</p>;

  // ...existing code...
  return (
    <div className="capsule-list">
      {capsules.map((c, idx) => (
        <div key={idx} className="capsule-card capsule-hover-card">
          <div className="capsule-card-title">{c.title}</div>
          <div className="capsule-card-hover-content">
            <div className="capsule-card-message">{c.message}</div>
            <div className="capsule-card-meta">
              <span><strong>Future Date:</strong> {c.future_date}</span><br />
              <span><em>Category: {c.category}</em></span>
            </div>
            <button className="capsule-card-delete" onClick={e => { e.stopPropagation(); handleDelete(idx); }}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}
