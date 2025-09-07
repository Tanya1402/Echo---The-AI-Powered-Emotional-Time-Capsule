import React from "react";

export default function CapsuleView({ capsule }) {
  return (
    <div className={`capsule-card category-${capsule.category.toLowerCase()}`}>
      <h3>{capsule.title}</h3>
      <p>{capsule.message}</p>
      <small>Open on: {capsule.future_date}</small>
      <span className="category">{capsule.category}</span>
    </div>
  );
}
