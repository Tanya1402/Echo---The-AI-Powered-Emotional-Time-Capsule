// api.js
const API_URL = "http://127.0.0.1:5000/api/capsules";

// Save a new capsule
export async function saveCapsule(data) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error("Failed to save capsule");
  return response.json();
}

// Fetch all capsules
export async function fetchCapsules() {
  const response = await fetch(API_URL);
  if (!response.ok) throw new Error("Failed to fetch capsules");
  return response.json();
}

// Delete capsule by id
export async function deleteCapsule(id) {
  const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
  if (!response.ok) throw new Error("Failed to delete capsule");
  return response.json();
}
