import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UserLogin from "./pages/UserLogin";
import Navbar from "./components/Navbar"; // ✅ Make sure filename is Navbar.jsx, not NavBar.jsx
import Home from "./pages/Home";
import UserOptions from "./pages/UserOptions";
import Schemes from "./pages/Schemes";
import Acts from "./pages/Acts";
import Policies from "./pages/Policies";
import ComplaintForm from "./pages/ComplaintForm";
import AdminDashboard from "./pages/AdminDashboard";
import Analytics from "./pages/Analytics";
import TrackStatus from "./pages/Trackstatus";
import VoiceComplaint from "./pages/VoiceComplaint";
import AdminLogin from "./pages/AdminLogin";
import ProtectedRoute from "./components/ProtectedRoute";
import ComplaintChoice from './pages/ComplaintChoice';
import Help from "./pages/Help";
import WomenChildComplaint from "./pages/WomenChildComplaint";
import SignupForm from "./pages/SignupForm";
import LoginForm from "./pages/LoginForm";
import UserDashboard from './pages/UserDashboard';



export default function App() {
  return (
    <Router>
      <div className="bg-gray-50 min-h-screen font-sans">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/user-options" element={<UserOptions />} />
          <Route path="/user-login" element={<UserLogin />} />
          <Route path="/complaint" element={<ComplaintForm />} />
          <Route path="/complaint-choice" element={<ComplaintChoice />} />
          <Route path="/voice" element={<VoiceComplaint />} />
          <Route path="/admin-login" element={<AdminLogin />} />
          <Route path="/analytics" element={<Analytics />} />
          {/* <Route path="/track" element={<Trackstatus />} /> */}
          <Route path="/trackstatus" element={<TrackStatus />} />
          <Route path="/dashboard" element={<UserDashboard />} />
          <Route path="/schemes" element={<Schemes />} />
          <Route path="/acts" element={<Acts />} />
          <Route path="/policies" element={<Policies />} />
          <Route path="/help" element={<Help />} />
          <Route path="/women-child-complaint" element={<WomenChildComplaint />} />
          <Route path="/signup" element={<SignupForm />} />
          <Route path="/login" element={<LoginForm />} />

          {/* ✅ Protected Route */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />

          <Route path="/dashboard" element={
          <ProtectedRoute>
            <UserDashboard />
          </ProtectedRoute>
        } />
        
        <Route path="/user-options" element={
          <ProtectedRoute>
            <UserOptions />
          </ProtectedRoute>
        } />
        
        <Route path="/voice" element={
          <ProtectedRoute>
            <VoiceComplaint />
          </ProtectedRoute>
        } />
        
        <Route path="/complaint" element={
          <ProtectedRoute>
            <ComplaintForm />
          </ProtectedRoute>
        } />
        
        <Route path="/trackstatus" element={
          <ProtectedRoute>
            <TrackStatus />
          </ProtectedRoute>
        } />
        
        {/* <Route path="/women-child-complaint" element={
          <ProtectedRoute>
            <EmergencyComplaint />
          </ProtectedRoute>
        } />
        
        <Route path="/profile" element={
          <ProtectedRoute>
            <UserProfile />
          </ProtectedRoute>
        } />
        
        <Route path="/help" element={
          <ProtectedRoute>
            <HelpSupport />
          </ProtectedRoute>
        } /> */}

          {/* Optional: Fallback 404 */}
          <Route path="*" element={<h2 className="text-center text-red-500 mt-10">404: Page not found</h2>} />
        
        </Routes>
      </div>
    </Router>
  );
}


  //  Default redirect
  //       <Route path="/" element={<Navigate to="/login" replace />} />
        
  //       {/* 404 Route */}
  //       <Route path="*" element={<Navigate to="/login" replace />} />