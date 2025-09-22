// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import axios from "axios";

// export default function LoginForm() {
//   const navigate = useNavigate();
//   const [form, setForm] = useState({ email: "", password: "" });

//   const handleChange = (e) => {
//     setForm({ ...form, [e.target.name]: e.target.value });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       const res = await axios.post("http://localhost:5000/api/auth/login", form);
//       localStorage.setItem("token", res.data.token);
//       navigate("/user-options"); // login success
//     } catch (err) {
//       alert(err.response?.data?.error || "Login failed");
//     }
//   };

//   return (
//     <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
//       <h2 className="text-2xl font-semibold mb-4">Login</h2>
//       <form onSubmit={handleSubmit} className="space-y-4">
//         <input
//           type="text"
//           name="email"
//           value={form.email}
//           onChange={handleChange}
//           placeholder="Email or Phone"
//           required
//           className="w-full border px-3 py-2 rounded"
//         />
//         <input
//           type="password"
//           name="password"
//           value={form.password}
//           onChange={handleChange}
//           placeholder="Password"
//           required
//           className="w-full border px-3 py-2 rounded"
//         />
//         <button type="submit" className="w-full bg-blue-600 text-white px-4 py-2 rounded">
//           Login
//         </button>
//       </form>

//       <p className="mt-4 text-center text-gray-600">
//         New user?{" "}
//         <span
//           onClick={() => navigate("/signup")}
//           className="text-blue-600 underline cursor-pointer"
//         >
//           Signup here
//         </span>
//       </p>
//     </div>
//   );
// }


import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function LoginForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError(""); // Clear error when user starts typing
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await axios.post("http://localhost:5000/api/auth/login", form);
      
      if (res.data.success) {
        // Store authentication token
        localStorage.setItem("token", res.data.token);
        localStorage.setItem("authToken", res.data.token); // For consistency with dashboard
        localStorage.setItem("isUser", "true");
        
        // Store user data for dashboard
        const userData = {
          userId: res.data.userId,
          name: res.data.name,
          email: res.data.email,
          phone: res.data.phone,
          address: res.data.address,
          photo: res.data.photo
        };
        localStorage.setItem("userData", JSON.stringify(userData));
        
        // Navigate to dashboard instead of user-options
        navigate("/dashboard");
      } else {
        setError(res.data.message || "Login failed");
      }
    } catch (err) {
      console.error("Login error:", err);
      setError(err.response?.data?.message || err.response?.data?.error || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 px-4 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-indigo-600/5"></div>
      <div className="absolute top-20 left-10 w-72 h-72 bg-blue-400/10 rounded-full blur-3xl"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-indigo-400/10 rounded-full blur-3xl"></div>

      <div className="relative z-10 bg-white/80 backdrop-blur-sm shadow-2xl rounded-3xl w-full max-w-md p-8 border border-white/20">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center text-3xl shadow-lg">
            👤
          </div>
          <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2">
            User Login
          </h2>
          <p className="text-gray-600">उपयोगकर्ता लॉगिन | वापरकर्ता लॉगिन</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email or Phone / ईमेल या फ़ोन
            </label>
            <input
              type="text"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="Enter your email or phone"
              required
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/70 backdrop-blur-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password / पासवर्ड
            </label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/70 backdrop-blur-sm"
            />
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl">
              <p className="text-red-600 text-sm font-medium">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 px-6 rounded-xl font-medium hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Logging in...</span>
              </div>
            ) : (
              "Login / लॉगिन"
            )}
          </button>
        </form>

        {/* Additional Options */}
        <div className="mt-8">
          
          {/* Register Link */}
          <div className="mt-4 text-center">
            <span className="text-gray-600 text-sm">New user? </span>
            <span
              onClick={() => navigate("/signup")}
              className="text-blue-600 hover:text-blue-700 font-medium text-sm hover:underline transition-colors cursor-pointer"
            >
              Signup here / यहाँ रजिस्टर करें
            </span>
          </div>
        </div>
        
      </div>
    </div>
  );
}