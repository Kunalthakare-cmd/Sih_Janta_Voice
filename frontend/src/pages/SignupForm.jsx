import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function SignupForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    phone: "",
    address: "",
  });
  const [photo, setPhoto] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handlePhotoChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setPhoto(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      Object.keys(form).forEach((key) => formData.append(key, form[key]));
      if (photo) formData.append("photo", photo);

      await axios.post("http://localhost:5000/api/auth/register", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("Signup successful! Please login now.");
      setForm({ name: "", email: "", password: "", phone: "", address: "" });
      setPhoto(null);
      navigate("/login"); // redirect to login page after signup
    } catch (err) {
      alert(err.response?.data?.error || "Signup failed");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-semibold mb-4">Signup</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="name" value={form.name} onChange={handleChange} placeholder="Full Name" required className="w-full border px-3 py-2 rounded" />
        <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="Email" required className="w-full border px-3 py-2 rounded" />
        <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="Password" required className="w-full border px-3 py-2 rounded" />
        <input name="phone" value={form.phone} onChange={handleChange} placeholder="Phone Number" required className="w-full border px-3 py-2 rounded" />
        <textarea name="address" value={form.address} onChange={handleChange} placeholder="Full Address" required className="w-full border px-3 py-2 rounded" />
        <input type="file" accept="image/*" onChange={handlePhotoChange} className="w-full border px-3 py-2 rounded" />
        <button type="submit" className="w-full bg-blue-600 text-white px-4 py-2 rounded">Signup</button>
      </form>

      <p className="mt-4 text-center text-gray-600">
        Already have an account?{" "}
        <span
          onClick={() => navigate("/login")}
          className="text-blue-600 underline cursor-pointer"
        >
          Login here
        </span>
      </p>
    </div>
  );
}
