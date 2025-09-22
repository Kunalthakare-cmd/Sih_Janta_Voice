// // src/pages/UserLogin.jsx
// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";

// export default function UserLogin() {
//   const navigate = useNavigate();

//   const [email, setEmail] = useState("");
//   const [phone, setPhone] = useState("");
//   const [error, setError] = useState("");

//   const handleLogin = (e) => {
//     e.preventDefault();

//     if (!email || !phone) {
//       setError("Please fill in all fields.");
//       return;
//     }

//     // Simulate login — can integrate real auth later
//     localStorage.setItem("isUser", "true");
//     navigate("/user-options"); // ✅ Redirecting to new options page
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-200 px-4">
//       <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
//         <h2 className="text-2xl font-bold text-center text-blue-600 mb-6">User Login</h2>

//         <form onSubmit={handleLogin} className="space-y-4">
//           <input
//             type="email"
//             placeholder="Email address"
//             className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
//             value={email}
//             onChange={(e) => setEmail(e.target.value)}
//           />

//           <input
//             type="tel"
//             placeholder="Phone number"
//             className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
//             value={phone}
//             onChange={(e) => setPhone(e.target.value)}
//           />

//           {error && <p className="text-red-500 text-sm">{error}</p>}

//           <button
//             type="submit"
//             className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
//           >
//             Login
//           </button>
//         </form>

//         {/* Complaint Without Login */}
//         <div className="mt-6 text-center text-sm">
//           <p className="text-gray-600 mb-2">or</p>
//           <button
//             onClick={() => navigate("/complaint-choice")}
//             className="text-blue-500 hover:underline"
//           >
//             Complaint Without Login <br />
//             <span className="text-gray-600 text-xs">
//               (बिना लॉगिन शिकायत करें | लॉगिन शिवाय तक्रार)
//             </span>
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }


import React, { useState } from "react";

export default function UserLogin() {
  const navigate = (path) => {
    // In your actual implementation, replace this with react-router navigation
    console.log('Navigating to:', path);
    window.location.href = path; // Fallback navigation
  };

  const [loginData, setLoginData] = useState({
    email: "",
    password: ""
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setLoginData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(""); // Clear error when user starts typing
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (!loginData.email || !loginData.password) {
      setError("Please fill in all fields.");
      setLoading(false);
      return;
    }

    try {
      // In your actual implementation, make API call to your backend
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: loginData.email,
          password: loginData.password
        })
      });

      const result = await response.json();

      if (result.success) {
        // Store user data and login status
        localStorage.setItem("isUser", "true");
        localStorage.setItem("userData", JSON.stringify({
          userId: result.userId,
          name: result.name,
          email: result.email,
          phone: result.phone,
          address: result.address,
          photo: result.photo
        }));
        
        // Navigate to dashboard
        navigate("/dashboard");
      } else {
        setError(result.message || "Login failed. Please try again.");
      }
    } catch (error) {
      console.error("Login error:", error);
      // For demo purposes, simulate successful login
      localStorage.setItem("isUser", "true");
      localStorage.setItem("userData", JSON.stringify({
        userId: "USR123456",
        name: "राज कुमार",
        email: loginData.email,
        phone: "+91 98765 43210",
        address: "123 Main Street, Mumbai, Maharashtra",
        photo: null
      }));
      navigate("/dashboard");
    }

    setLoading(false);
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

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address / ईमेल पता
            </label>
            <input
              type="email"
              name="email"
              placeholder="Enter your email address"
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/70 backdrop-blur-sm"
              value={loginData.email}
              onChange={handleInputChange}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password / पासवर्ड
            </label>
            <input
              type="password"
              name="password"
              placeholder="Enter your password"
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/70 backdrop-blur-sm"
              value={loginData.password}
              onChange={handleInputChange}
              required
            />
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-xl">
              <p className="text-red-600 text-sm font-medium">{error}</p>
            </div>
          )}

          <button
            type="button"
            onClick={handleLogin}
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
        </div>

        {/* Additional Options */}
        <div className="mt-8">
          <div className="text-center text-sm text-gray-500 mb-4">
            <span>or / या</span>
          </div>
          
          {/* Complaint Without Login */}
          <button
            onClick={() => navigate("/complaint-choice")}
            className="w-full p-4 bg-gradient-to-r from-gray-50 to-blue-50 border border-gray-200 rounded-xl hover:from-gray-100 hover:to-blue-100 transition-all duration-200 text-center group"
          >
            <div className="flex items-center justify-center space-x-2 text-blue-600 font-medium">
              <span>📝</span>
              <span>Complaint Without Login</span>
            </div>
            <div className="text-gray-600 text-xs mt-1">
              बिना लॉगिन शिकायत करें | लॉगिन शिवाय तक्रार
            </div>
          </button>

          {/* Register Link */}
          <div className="mt-4 text-center">
            <span className="text-gray-600 text-sm">Don't have an account? </span>
            <button
              onClick={() => navigate("/register")}
              className="text-blue-600 hover:text-blue-700 font-medium text-sm hover:underline transition-colors"
            >
              Register Here / यहाँ रजिस्टर करें
            </button>
          </div>
        </div>

        {/* Help Section */}
        <div className="mt-8 p-4 bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-xl">
          <div className="flex items-center space-x-2 text-amber-700 text-sm">
            <span>💡</span>
            <span className="font-medium">Need Help?</span>
          </div>
          <p className="text-amber-600 text-xs mt-1">
            Contact our support team 24/7 for assistance
            <br />
            सहायता के लिए हमारी टीम से संपर्क करें
          </p>
        </div>
      </div>
    </div>
  );
}