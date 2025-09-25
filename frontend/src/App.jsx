import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext"; // Create this context
import UserLogin from "./pages/UserLogin";
import Navbar from "./components/Navbar";
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
    <AuthProvider>
      <Router>
        <div className="bg-gray-50 min-h-screen font-sans">
          <Navbar />
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/schemes" element={<Schemes />} />
            <Route path="/acts" element={<Acts />} />
            <Route path="/policies" element={<Policies />} />
            <Route path="/help" element={<Help />} />
            
            {/* Authentication Routes */}
            <Route path="/signup" element={<SignupForm />} />
            <Route path="/login" element={<LoginForm />} />
            <Route path="/user-login" element={<UserLogin />} />
            <Route path="/admin-login" element={<AdminLogin />} />

            {/* Protected User Routes */}
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
            
            <Route path="/complaint-choice" element={
              <ProtectedRoute>
                <ComplaintChoice />
              </ProtectedRoute>
            } />
            
            <Route path="/complaint" element={
              <ProtectedRoute>
                <ComplaintForm />
              </ProtectedRoute>
            } />
            
            <Route path="/voice" element={
              <ProtectedRoute>
                <VoiceComplaint />
              </ProtectedRoute>
            } />
            
            <Route path="/trackstatus" element={
              <ProtectedRoute>
                <TrackStatus />
              </ProtectedRoute>
            } />
            
            <Route path="/women-child-complaint" element={
              <ProtectedRoute>
                <WomenChildComplaint />
              </ProtectedRoute>
            } />

            {/* Admin Protected Routes */}
            <Route path="/admin" element={
              <ProtectedRoute requireAdmin={true}>
                <AdminDashboard />
              </ProtectedRoute>
            } />
            
            <Route path="/analytics" element={
              <ProtectedRoute requireAdmin={true}>
                <Analytics />
              </ProtectedRoute>
            } />

            {/* 404 Route */}
            <Route path="*" element={
              <div className="text-center mt-20">
                <h2 className="text-2xl font-bold text-red-500 mb-4">404: Page not found</h2>
                <p className="text-gray-600">The page you're looking for doesn't exist.</p>
              </div>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}