// // import React, { useState, useEffect } from 'react';
// // import { useNavigate } from 'react-router-dom';
// // import axios from 'axios';

// // export default function UserDashboard() {
// //   const navigate = useNavigate();

// //   const [user, setUser] = useState(null);
// //   const [userStats, setUserStats] = useState({
// //     totalComplaints: 0,
// //     pending: 0,
// //     resolved: 0,
// //     inProgress: 0
// //   });
// //   const [recentComplaints, setRecentComplaints] = useState([]);
// //   const [activeSection, setActiveSection] = useState('dashboard');
// //   const [sidebarOpen, setSidebarOpen] = useState(false);
// //   const [loading, setLoading] = useState(true);
// //   const [error, setError] = useState('');

// //   // Fetch user data and complaints on component mount
// //   useEffect(() => {
// //     const checkAuthentication = () => {
// //       const token = localStorage.getItem('token') || localStorage.getItem('authToken');
// //       const isUser = localStorage.getItem('isUser');
      
// //       if (!token || !isUser) {
// //         navigate('/login');
// //         return false;
// //       }
// //       return true;
// //     };

// //     if (checkAuthentication()) {
// //       fetchUserData();
// //       fetchUserComplaints();
// //     }
// //   }, [navigate]);

// //   const fetchUserData = async () => {
// //     try {
// //       // Get user data from localStorage first
// //       const storedUserData = localStorage.getItem('userData');
// //       if (storedUserData) {
// //         const userData = JSON.parse(storedUserData);
// //         setUser(userData);
// //         setLoading(false);
// //       }

// //       // Fetch fresh data from API
// //       const token = localStorage.getItem('token') || localStorage.getItem('authToken');
// //       const userId = JSON.parse(storedUserData || '{}').userId;

// //       if (userId && token) {
// //         const response = await axios.get(`http://localhost:5000/api/users/${userId}`, {
// //           headers: {
// //             'Authorization': `Bearer ${token}`,
// //             'Content-Type': 'application/json'
// //           }
// //         });

// //         if (response.data.success) {
// //           const freshUserData = response.data.user;
// //           setUser(freshUserData);
// //           // Update localStorage with fresh data
// //           localStorage.setItem('userData', JSON.stringify(freshUserData));
// //         }
// //       }
// //     } catch (error) {
// //       console.error('Error fetching user data:', error);
// //       // If API fails, continue with localStorage data
// //       const storedUserData = localStorage.getItem('userData');
// //       if (storedUserData) {
// //         setUser(JSON.parse(storedUserData));
// //       } else {
// //         // If no stored data and API fails, redirect to login
// //         handleLogout();
// //       }
// //     } finally {
// //       setLoading(false);
// //     }
// //   };

// //   const fetchUserComplaints = async () => {
// //     try {
// //       const storedUserData = localStorage.getItem('userData');
// //       const userId = JSON.parse(storedUserData || '{}').userId;
// //       const token = localStorage.getItem('token') || localStorage.getItem('authToken');

// //       if (!userId || !token) return;

// //       const response = await axios.get(`http://localhost:5000/api/complaints/user/${userId}`, {
// //         headers: {
// //           'Authorization': `Bearer ${token}`,
// //           'Content-Type': 'application/json'
// //         }
// //       });

// //       if (response.data.success) {
// //         const complaints = response.data.complaints;
        
// //         // Calculate stats
// //         const stats = {
// //           totalComplaints: complaints.length,
// //           pending: complaints.filter(c => c.status === 'Pending').length,
// //           resolved: complaints.filter(c => c.status === 'Resolved').length,
// //           inProgress: complaints.filter(c => c.status === 'In Progress').length
// //         };
        
// //         setUserStats(stats);
        
// //         // Get recent complaints (last 5)
// //         const recent = complaints
// //           .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
// //           .slice(0, 5);
// //         setRecentComplaints(recent);
// //       }
// //     } catch (error) {
// //       console.error('Error fetching complaints:', error);
// //       setError('Failed to load complaint data');
// //     }
// //   };

// //   const handleLogout = () => {
// //     // Clear all stored data
// //     localStorage.removeItem("isUser");
// //     localStorage.removeItem("userData");
// //     localStorage.removeItem("authToken");
// //     localStorage.removeItem("token");
    
// //     // Navigate to login
// //     navigate("/login");
// //   };

// //   const menuItems = [
// //     {
// //       id: 'dashboard',
// //       label: 'Dashboard',
// //       hindiLabel: 'डैशबोर्ड',
// //       icon: '🏠',
// //       path: '/dashboard'
// //     },
// //     {
// //       id: 'voice-complaint',
// //       label: 'Voice Complaint',
// //       hindiLabel: 'आवाज़ शिकायत',
// //       icon: '🎤',
// //       path: '/voice'
// //     },
// //     {
// //       id: 'written-complaint',
// //       label: 'Written Complaint',
// //       hindiLabel: 'लिखित शिकायत',
// //       icon: '📝',
// //       path: '/complaint'
// //     },
// //     {
// //       id: 'track-complaint',
// //       label: 'Track Complaint',
// //       hindiLabel: 'शिकायत ट्रैक करें',
// //       icon: '🔍',
// //       path: '/trackstatus'
// //     },
// //     {
// //       id: 'emergency',
// //       label: 'Emergency Support',
// //       hindiLabel: 'आपातकालीन सहायता',
// //       icon: '🚨',
// //       path: '/women-child-complaint'
// //     },
// //     {
// //       id: 'profile',
// //       label: 'Profile',
// //       hindiLabel: 'प्रोफाइल',
// //       icon: '👤',
// //       path: '/profile'
// //     }
// //   ];

// //   const stats = [
// //     { 
// //       label: 'Total Complaints', 
// //       hindiLabel: 'कुल शिकायतें', 
// //       value: userStats.totalComplaints.toString(), 
// //       color: 'blue' 
// //     },
// //     { 
// //       label: 'Pending', 
// //       hindiLabel: 'लंबित', 
// //       value: userStats.pending.toString(), 
// //       color: 'amber' 
// //     },
// //     { 
// //       label: 'Resolved', 
// //       hindiLabel: 'हल', 
// //       value: userStats.resolved.toString(), 
// //       color: 'green' 
// //     },
// //     { 
// //       label: 'In Progress', 
// //       hindiLabel: 'प्रगति में', 
// //       value: userStats.inProgress.toString(), 
// //       color: 'purple' 
// //     }
// //   ];

// //   const handleMenuClick = (item) => {
// //     setActiveSection(item.id);
// //     if (item.path && item.path !== '/dashboard') {
// //       navigate(item.path);
// //     }
// //     setSidebarOpen(false);
// //   };

// //   const getStatusColor = (status) => {
// //     switch (status.toLowerCase()) {
// //       case 'resolved':
// //         return 'bg-green-100 text-green-700';
// //       case 'in progress':
// //         return 'bg-purple-100 text-purple-700';
// //       case 'pending':
// //         return 'bg-amber-100 text-amber-700';
// //       default:
// //         return 'bg-gray-100 text-gray-700';
// //     }
// //   };

// //   const formatDate = (dateString) => {
// //     return new Date(dateString).toLocaleDateString('en-IN', {
// //       year: 'numeric',
// //       month: 'short',
// //       day: 'numeric'
// //     });
// //   };

// //   const getProfileImage = () => {
// //     if (user?.photo) {
// //       // If photo is a full URL, use it directly
// //       if (user.photo.startsWith('http')) {
// //         return user.photo;
// //       }
// //       // If photo is a relative path, construct full URL
// //       return `http://localhost:5000/${user.photo}`;
// //     }
// //     return null;
// //   };

// //   const getInitials = () => {
// //     if (!user?.name) return 'U';
// //     return user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
// //   };

// //   // Loading state
// //   if (loading) {
// //     return (
// //       <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-100">
// //         <div className="text-center">
// //           <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
// //           <p className="mt-4 text-gray-600 font-medium">Loading your dashboard...</p>
// //           <p className="text-sm text-gray-500">आपका डैशबोर्ड लोड हो रहा है...</p>
// //         </div>
// //       </div>
// //     );
// //   }

// //   // Error state - no user data
// //   if (!user) {
// //     return (
// //       <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-100">
// //         <div className="text-center bg-white rounded-3xl p-8 shadow-xl">
// //           <div className="text-6xl mb-4">⚠️</div>
// //           <h2 className="text-2xl font-bold text-red-600 mb-4">Session Expired</h2>
// //           <p className="text-gray-600 mb-6">Please login again to continue</p>
// //           <button
// //             onClick={() => navigate('/login')}
// //             className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition-colors"
// //           >
// //             Go to Login
// //           </button>
// //         </div>
// //       </div>
// //     );
// //   }

// //   return (
// //     <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex">
// //       {/* Mobile Sidebar Overlay */}
// //       {sidebarOpen && (
// //         <div
// //           className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
// //           onClick={() => setSidebarOpen(false)}
// //         ></div>
// //       )}

// //       {/* Sidebar */}
// //       <div className={`fixed lg:sticky top-0 left-0 h-screen w-80 bg-white/95 backdrop-blur-sm shadow-2xl transform transition-transform duration-300 z-50 ${
// //         sidebarOpen ? 'translate-x-0' : '-translate-x-full'
// //       } lg:translate-x-0 lg:shadow-none border-r border-white/20`}>
        
// //         {/* Sidebar Header */}
// //         <div className="p-6 border-b border-gray-200/50 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
// //           <div className="flex items-center space-x-4">
// //             <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-2xl font-bold backdrop-blur-sm border border-white/30 overflow-hidden">
// //               {getProfileImage() ? (
// //                 <img 
// //                   src={getProfileImage()} 
// //                   alt="Profile" 
// //                   className="w-full h-full rounded-full object-cover"
// //                   onError={(e) => {
// //                     e.target.style.display = 'none';
// //                     e.target.nextSibling.style.display = 'flex';
// //                   }}
// //                 />
// //               ) : null}
// //               <div className={`w-full h-full rounded-full flex items-center justify-center ${getProfileImage() ? 'hidden' : 'flex'}`}>
// //                 {getInitials()}
// //               </div>
// //             </div>
// //             <div className="flex-1 min-w-0">
// //               <h3 className="font-bold text-lg truncate">नमस्ते, {user.name}!</h3>
// //               {/* <p className="text-blue-100 text-sm truncate">ID: {user.userId}</p> */}
// //             </div>
// //           </div>
// //         </div>

// //         {/* Navigation Menu */}
// //         <nav className="p-4 space-y-2">
// //           {menuItems.map((item) => (
// //             <button
// //               key={item.id}
// //               onClick={() => handleMenuClick(item)}
// //               className={`w-full flex items-center space-x-4 px-4 py-3 rounded-xl text-left transition-all duration-200 ${
// //                 activeSection === item.id
// //                   ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-lg scale-105'
// //                   : 'text-gray-700 hover:bg-gradient-to-r hover:from-gray-100 hover:to-blue-50 hover:text-blue-700'
// //               }`}
// //             >
// //               <span className="text-2xl">{item.icon}</span>
// //               <div className="flex-1">
// //                 <div className="font-medium">{item.label}</div>
// //                 <div className="text-xs opacity-75">{item.hindiLabel}</div>
// //               </div>
// //             </button>
// //           ))}
// //         </nav>

       


// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import axios from 'axios';

// export default function UserDashboard() {
//   const navigate = useNavigate();

//   const [user, setUser] = useState(null);
//   const [userStats, setUserStats] = useState({
//     totalComplaints: 0,
//     pending: 0,
//     resolved: 0,
//     inProgress: 0
//   });
//   const [recentComplaints, setRecentComplaints] = useState([]);
//   const [activeSection, setActiveSection] = useState('dashboard');
//   const [sidebarOpen, setSidebarOpen] = useState(false);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState('');

//   // Fetch user data and complaints on component mount
//   useEffect(() => {
//     const checkAuthentication = () => {
//       const token = localStorage.getItem('token') || localStorage.getItem('authToken');
//       const isUser = localStorage.getItem('isUser');
      
//       if (!token || !isUser) {
//         navigate('/login');
//         return false;
//       }
//       return true;
//     };

//     if (checkAuthentication()) {
//       fetchUserProfile();
//       fetchUserComplaints();
//     }
//   }, [navigate]);

//   // Updated fetchUserData function to use the correct backend endpoint
//   const fetchUserProfile = async () => {
//     try {
//       // Get user data from localStorage first for immediate display
//       const storedUserData = localStorage.getItem('userData');
//       if (storedUserData) {
//         const userData = JSON.parse(storedUserData);
//         setUser(userData);
//         setLoading(false);
//       }

//       // Fetch fresh data from the new backend endpoint
//       const token = localStorage.getItem('token') || localStorage.getItem('authToken');

//       if (token) {
//         const response = await axios.get('http://localhost:5000/api/user/profile', {
//           headers: {
//             'Authorization': `Bearer ${token}`,
//             'Content-Type': 'application/json'
//           }
//         });

//         if (response.data.success) {
//           const freshUserData = response.data.user;
//           setUser(freshUserData);
//           // Update localStorage with fresh data
//           localStorage.setItem('userData', JSON.stringify(freshUserData));
//         }
//       }
//     } catch (error) {
//       console.error('Error fetching user profile:', error);
      
//       // Handle specific error cases
//       if (error.response?.status === 401) {
//         console.error('Authentication failed - redirecting to login');
//         handleLogout();
//         return;
//       }
      
//       // If API fails but we have stored data, continue with that
//       const storedUserData = localStorage.getItem('userData');
//       if (storedUserData) {
//         setUser(JSON.parse(storedUserData));
//       } else {
//         // If no stored data and API fails, redirect to login
//         handleLogout();
//       }
//     } finally {
//       setLoading(false);
//     }
//   };

//   // Updated fetchUserComplaints function with correct endpoint and data mapping
//   const fetchUserComplaints = async () => {
//     try {
//       const token = localStorage.getItem('token') || localStorage.getItem('authToken');

//       if (!token) {
//         console.error('No authentication token found');
//         return;
//       }

//       // Use the correct API endpoint that matches backend
//       const response = await axios.get('http://localhost:5000/api/user/complaints', {
//         headers: {
//           'Authorization': `Bearer ${token}`,
//           'Content-Type': 'application/json'
//         },
//         params: {
//           limit: 50, // Get more complaints for stats calculation
//         }
//       });

//       if (response.data.success) {
//         const complaints = response.data.complaints;
        
//         // Calculate stats using the correct field names from backend
//         const stats = {
//           totalComplaints: complaints.length,
//           pending: complaints.filter(c => c.status === 'Pending').length,
//           resolved: complaints.filter(c => c.status === 'Resolved').length,
//           inProgress: complaints.filter(c => c.status === 'In Progress').length
//         };
        
//         setUserStats(stats);
        
//         // Get recent complaints (last 5) and map the data structure correctly
//         const recent = complaints
//           .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
//           .slice(0, 5)
//           .map(complaint => ({
//             ...complaint,
//             // Map backend fields to frontend expected fields for compatibility
//             complaintId: complaint.id,
//             createdAt: complaint.timestamp,
//             title: complaint.complaint || complaint.description,
//             subject: complaint.complaint || complaint.description,
//             // Use urgency from backend instead of priority
//             priority: complaint.urgency || 'Medium'
//           }));
        
//         setRecentComplaints(recent);
//       }
//     } catch (error) {
//       console.error('Error fetching complaints:', error);
      
//       // More specific error handling
//       if (error.response?.status === 401) {
//         setError('Authentication failed. Please login again.');
//         handleLogout();
//       } else if (error.response?.status === 403) {
//         setError('Access denied. Please check your permissions.');
//       } else {
//         setError('Failed to load complaint data');
//       }
//     }
//   };

//   const handleLogout = () => {
//     // Clear all stored data
//     localStorage.removeItem("isUser");
//     localStorage.removeItem("userData");
//     localStorage.removeItem("authToken");
//     localStorage.removeItem("token");
    
//     // Navigate to login
//     navigate("/login");
//   };

//   const menuItems = [
//     {
//       id: 'dashboard',
//       label: 'Dashboard',
//       hindiLabel: 'डैशबोर्ड',
//       icon: '🏠',
//       path: '/dashboard'
//     },
//     {
//       id: 'voice-complaint',
//       label: 'Voice Complaint',
//       hindiLabel: 'आवाज़ शिकायत',
//       icon: '🎤',
//       path: '/voice'
//     },
//     {
//       id: 'written-complaint',
//       label: 'Written Complaint',
//       hindiLabel: 'लिखित शिकायत',
//       icon: '📝',
//       path: '/complaint'
//     },
//     {
//       id: 'track-complaint',
//       label: 'Track Complaint',
//       hindiLabel: 'शिकायत ट्रैक करें',
//       icon: '🔍',
//       path: '/trackstatus'
//     },
//     {
//       id: 'emergency',
//       label: 'Emergency Support',
//       hindiLabel: 'आपातकालीन सहायता',
//       icon: '🚨',
//       path: '/women-child-complaint'
//     },
//     {
//       id: 'profile',
//       label: 'Profile',
//       hindiLabel: 'प्रोफाइल',
//       icon: '👤',
//       path: '/profile'
//     }
//   ];

//   const stats = [
//     { 
//       label: 'Total Complaints', 
//       hindiLabel: 'कुल शिकायतें', 
//       value: userStats.totalComplaints.toString(), 
//       color: 'blue' 
//     },
//     { 
//       label: 'Pending', 
//       hindiLabel: 'लंबित', 
//       value: userStats.pending.toString(), 
//       color: 'amber' 
//     },
//     { 
//       label: 'Resolved', 
//       hindiLabel: 'हल', 
//       value: userStats.resolved.toString(), 
//       color: 'green' 
//     },
//     { 
//       label: 'In Progress', 
//       hindiLabel: 'प्रगति में', 
//       value: userStats.inProgress.toString(), 
//       color: 'purple' 
//     }
//   ];

//   const handleMenuClick = (item) => {
//     setActiveSection(item.id);
//     if (item.path && item.path !== '/dashboard') {
//       navigate(item.path);
//     }
//     setSidebarOpen(false);
//   };

//   const getStatusColor = (status) => {
//     switch (status.toLowerCase()) {
//       case 'resolved':
//         return 'bg-green-100 text-green-700';
//       case 'in progress':
//         return 'bg-purple-100 text-purple-700';
//       case 'pending':
//         return 'bg-amber-100 text-amber-700';
//       default:
//         return 'bg-gray-100 text-gray-700';
//     }
//   };

//   const formatDate = (dateString) => {
//     if (!dateString) return 'N/A';
//     return new Date(dateString).toLocaleDateString('en-IN', {
//       year: 'numeric',
//       month: 'short',
//       day: 'numeric'
//     });
//   };

//   const getProfileImage = () => {
//     if (user?.photo) {
//       // If photo is a full URL, use it directly
//       if (user.photo.startsWith('http')) {
//         return user.photo;
//       }
//       // If photo is a relative path, construct full URL
//       return `http://localhost:5000/${user.photo}`;
//     }
//     return null;
//   };

//   const getInitials = () => {
//     if (!user?.name) return 'U';
//     return user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
//   };

//   // Function to get priority color
//   const getPriorityColor = (priority) => {
//     switch (priority.toLowerCase()) {
//       case 'high':
//         return 'text-red-600';
//       case 'medium':
//         return 'text-yellow-600';
//       case 'low':
//         return 'text-green-600';
//       default:
//         return 'text-gray-600';
//     }
//   };

//   // Loading state
//   if (loading) {
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-100">
//         <div className="text-center">
//           <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
//           <p className="mt-4 text-gray-600 font-medium">Loading your dashboard...</p>
//           <p className="text-sm text-gray-500">आपका डैशबोर्ड लोड हो रहा है...</p>
//         </div>
//       </div>
//     );
//   }

//   // Error state - no user data
//   if (!user) {
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-100">
//         <div className="text-center bg-white rounded-3xl p-8 shadow-xl">
//           <div className="text-6xl mb-4">⚠️</div>
//           <h2 className="text-2xl font-bold text-red-600 mb-4">Session Expired</h2>
//           <p className="text-gray-600 mb-6">Please login again to continue</p>
//           <button
//             onClick={() => navigate('/login')}
//             className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition-colors"
//           >
//             Go to Login
//           </button>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex">
//       {/* Mobile Sidebar Overlay */}
//       {sidebarOpen && (
//         <div
//           className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
//           onClick={() => setSidebarOpen(false)}
//         ></div>
//       )}

//       {/* Sidebar */}
//       <div className={`fixed lg:sticky top-0 left-0 h-screen w-80 bg-white/95 backdrop-blur-sm shadow-2xl transform transition-transform duration-300 z-50 ${
//         sidebarOpen ? 'translate-x-0' : '-translate-x-full'
//       } lg:translate-x-0 lg:shadow-none border-r border-white/20`}>
        
//         {/* Sidebar Header */}
//         <div className="p-6 border-b border-gray-200/50 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
//           <div className="flex items-center space-x-4">
//             <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-2xl font-bold backdrop-blur-sm border border-white/30 overflow-hidden">
//               {getProfileImage() ? (
//                 <img 
//                   src={getProfileImage()} 
//                   alt="Profile" 
//                   className="w-full h-full rounded-full object-cover"
//                   onError={(e) => {
//                     e.target.style.display = 'none';
//                     e.target.nextSibling.style.display = 'flex';
//                   }}
//                 />
//               ) : null}
//               <div className={`w-full h-full rounded-full flex items-center justify-center ${getProfileImage() ? 'hidden' : 'flex'}`}>
//                 {getInitials()}
//               </div>
//             </div>
//             <div className="flex-1 min-w-0">
//               <h3 className="font-bold text-lg truncate">नमस्ते, {user.name}!</h3>
//             </div>
//           </div>
//         </div>

//         {/* Navigation Menu */}
//         <nav className="p-4 space-y-2">
//           {menuItems.map((item) => (
//             <button
//               key={item.id}
//               onClick={() => handleMenuClick(item)}
//               className={`w-full flex items-center space-x-4 px-4 py-3 rounded-xl text-left transition-all duration-200 ${
//                 activeSection === item.id
//                   ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-lg scale-105'
//                   : 'text-gray-700 hover:bg-gradient-to-r hover:from-gray-100 hover:to-blue-50 hover:text-blue-700'
//               }`}
//             >
//               <span className="text-2xl">{item.icon}</span>
//               <div className="flex-1">
//                 <div className="font-medium">{item.label}</div>
//                 <div className="text-xs opacity-75">{item.hindiLabel}</div>
//               </div>
//             </button>
//           ))}
//         </nav>

//         {/* Logout Button */}
//         <div className="absolute bottom-6 left-4 right-4">
//           <button
//             onClick={handleLogout}
//             className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 transition-all duration-200 shadow-lg hover:shadow-xl"
//           >
//             <span>🚪</span>
//             <span className="font-medium">Logout / लॉगआउट</span>
//           </button>
//         </div>
//       </div>

//       {/* Main Content */}
//       <div className="flex-1 min-h-screen">
//         {/* Top Bar */}
//         <header className="bg-white/80 backdrop-blur-sm shadow-lg border-b border-white/20 sticky top-0 z-30">
//           <div className="flex items-center justify-between px-6 py-4">
//             <div className="flex items-center space-x-4">
//               <button
//                 onClick={() => setSidebarOpen(true)}
//                 className="lg:hidden p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
//               >
//                 <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
//                 </svg>
//               </button>
//               <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
//                 शिकायत पोर्टल डैशबोर्ड
//               </h1>
//             </div>
            
//             {/* User Info in Top Bar */}
//             <div className="flex items-center space-x-4">
//               <div className="hidden md:block text-right">
//                 <div className="font-medium text-gray-900">{user.name}</div>
//                 <div className="text-sm text-gray-600">{user.email}</div>
//               </div>
//               <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold shadow-lg overflow-hidden">
//                 {getProfileImage() ? (
//                   <img 
//                     src={getProfileImage()} 
//                     alt="Profile" 
//                     className="w-full h-full rounded-full object-cover"
//                     onError={(e) => {
//                       e.target.style.display = 'none';
//                       e.target.nextSibling.style.display = 'flex';
//                     }}
//                   />
//                 ) : null}
//                 <div className={`w-full h-full rounded-full flex items-center justify-center ${getProfileImage() ? 'hidden' : 'flex'}`}>
//                   {getInitials()}
//                 </div>
//               </div>
//             </div>
//           </div>
//         </header>

//         {/* Dashboard Content */}
//         <main className="p-6">  

//           {/* Stats Cards */}
//           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
//             {stats.map((stat, index) => (
//               <div key={index} className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 hover:shadow-xl transition-all duration-300 hover:scale-105">
//                 <div className="flex items-center justify-between mb-4">
//                   <div className={`w-12 h-12 bg-gradient-to-br from-${stat.color}-500 to-${stat.color}-600 rounded-xl flex items-center justify-center text-white text-xl font-bold shadow-lg`}>
//                     {stat.value}
//                   </div>
//                 </div>
//                 <h3 className="font-bold text-gray-900 text-lg">{stat.label}</h3>
//                 <p className="text-gray-600 text-sm">{stat.hindiLabel}</p>
//               </div>
//             ))}
//           </div>

       
//           <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">


//             <div className="bg-white/80 backdrop-blur-sm rounded-3xl p-8 shadow-lg border border-white/20">
//               <h3 className="text-2xl font-bold text-gray-900 mb-6">Recent Complaints / हाल की शिकायतें</h3>
//               <div className="space-y-4">
//                 {recentComplaints.length > 0 ? (
//                   recentComplaints.map((complaint) => (
//                     <div key={complaint.id || complaint.complaintId} className="p-4 bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl border border-gray-200/50 hover:shadow-md transition-all duration-300">
//                       <div className="flex items-center justify-between mb-2">
//                         <span className="font-bold text-blue-600">{complaint.complaintId || complaint.id}</span>
//                         <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(complaint.status)}`}>
//                           {complaint.status}
//                         </span>
//                       </div>
//                       <h4 className="font-medium text-gray-900">{complaint.title || complaint.subject}</h4>
//                       <p className="text-sm text-gray-600 line-clamp-2">{complaint.description}</p>
//                       <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
//                         <span>{formatDate(complaint.createdAt || complaint.date)}</span>
//                         <span className="font-medium">{complaint.priority || 'Medium'} Priority</span>
//                       </div>
//                     </div>
//                   ))
//                 ) : (
//                   <div className="text-center py-8">
//                     <div className="text-4xl mb-4">📝</div>
//                     <p className="text-gray-600 font-medium">No complaints found</p>
//                     <p className="text-sm text-gray-500">कोई शिकायत नहीं मिली</p>
//                     <button
//                       onClick={() => handleMenuClick(menuItems[2])}
//                       className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
//                     >
//                       File New Complaint
//                     </button>
//                   </div>
//                 )}
//               </div>
//             </div>
//           </div>

//           {/* Help Section */}
//           <div className="bg-gradient-to-r from-amber-500 to-orange-500 rounded-3xl p-8 text-white shadow-2xl">
//             <div className="flex items-center space-x-4">
//               <div className="text-4xl">💡</div>
//               <div>
//                 <h3 className="text-2xl font-bold mb-2">Need Help? / मदद चाहिए?</h3>
//                 <p className="text-amber-100 mb-4">
//                   Our support team is available 24/7 to assist you with your complaints and queries.
//                   <br />
//                   <span className="text-sm">हमारी सहायता टीम आपकी शिकायतों में 24/7 मदद के लिए उपलब्ध है।</span>
//                 </p>
//                 <button 
//                   onClick={() => handleMenuClick(menuItems.find(item => item.id === 'help'))}
//                   className="bg-white text-amber-600 px-6 py-3 rounded-xl font-medium hover:bg-amber-50 transition-colors shadow-lg"
//                 >
//                   Contact Support / संपर्क करें
//                 </button>
//               </div>
//             </div>
//           </div>
//         </main>
//       </div>
//     </div>
//   );
// }

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function UserDashboard() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [userStats, setUserStats] = useState({
    totalComplaints: 0,
    pending: 0,
    resolved: 0,
    inProgress: 0
  });
  const [recentComplaints, setRecentComplaints] = useState([]);
  const [activeSection, setActiveSection] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch user data and complaints on component mount
  useEffect(() => {
    const checkAuthentication = () => {
      const token = localStorage.getItem('token') || localStorage.getItem('authToken');
      const isUser = localStorage.getItem('isUser');
      
      if (!token || !isUser) {
        navigate('/login');
        return false;
      }
      return true;
    };

    if (checkAuthentication()) {
      fetchUserProfile();
      fetchUserComplaints();
    }
  }, [navigate]);

  // Updated fetchUserData function to use the correct backend endpoint
  const fetchUserProfile = async () => {
    try {
      // Get user data from localStorage first for immediate display
      const storedUserData = localStorage.getItem('userData');
      if (storedUserData) {
        const userData = JSON.parse(storedUserData);
        setUser(userData);
        setLoading(false);
      }
      

      // Fetch fresh data from the new backend endpoint
      const token = localStorage.getItem('token') || localStorage.getItem('authToken');

      if (token) {
        const response = await axios.get('http://localhost:5000/api/user/profile', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.data.success) {
          const freshUserData = response.data.user;
          setUser(freshUserData);
          // Update localStorage with fresh data
          localStorage.setItem('userData', JSON.stringify(freshUserData));
        }
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      
      // Handle specific error cases
      if (error.response?.status === 401) {
        console.error('Authentication failed - redirecting to login');
        handleLogout();
        return;
      }
      
      // If API fails but we have stored data, continue with that
      const storedUserData = localStorage.getItem('userData');
      if (storedUserData) {
        setUser(JSON.parse(storedUserData));
      } else {
        // If no stored data and API fails, redirect to login
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  };

  // Updated fetchUserComplaints function with correct endpoint and data mapping
  const fetchUserComplaints = async () => {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('authToken');

      if (!token) {
        console.error('No authentication token found');
        return;
      }

      // Use the correct API endpoint that matches backend
      const response = await axios.get('http://localhost:5000/api/user/complaints', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        params: {
          limit: 50, // Get more complaints for stats calculation
        }
      });

      if (response.data.success) {
        const complaints = response.data.complaints;
        
        // Calculate stats using the correct field names from backend
        const stats = {
          totalComplaints: complaints.length,
          pending: complaints.filter(c => c.status === 'Pending').length,
          resolved: complaints.filter(c => c.status === 'Resolved').length,
          inProgress: complaints.filter(c => c.status === 'In Progress').length
        };
        
        setUserStats(stats);
        
        // Get recent complaints (last 5) and map the data structure correctly
        const recent = complaints
          .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
          .slice(0, 5)
          .map(complaint => ({
            ...complaint,
            // Map backend fields to frontend expected fields for compatibility
            complaintId: complaint.id,
            createdAt: complaint.timestamp,
            title: complaint.complaint || complaint.description,
            subject: complaint.complaint || complaint.description,
            // Use urgency from backend instead of priority
            priority: complaint.urgency || 'Medium'
          }));
        
        setRecentComplaints(recent);
      }
    } catch (error) {
      console.error('Error fetching complaints:', error);
      
      // More specific error handling
      if (error.response?.status === 401) {
        setError('Authentication failed. Please login again.');
        handleLogout();
      } else if (error.response?.status === 403) {
        setError('Access denied. Please check your permissions.');
      } else {
        setError('Failed to load complaint data');
      }
    }
  };

  const handleLogout = () => {
    // Clear all stored data
    localStorage.removeItem("isUser");
    localStorage.removeItem("userData");
    localStorage.removeItem("authToken");
    localStorage.removeItem("token");
    
    // Navigate to login
    navigate("/login");
  };

  // Updated menu items with the new nearby complaints option
  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      hindiLabel: 'डैशबोर्ड',
      icon: '🏠',
      path: '/dashboard'
    },
   
    {
      id: 'voice-complaint',
      label: 'Voice Complaint',
      hindiLabel: 'आवाज़ शिकायत',
      icon: '🎤',
      path: '/voice'
    },
    {
      id: 'written-complaint',
      label: 'Written Complaint',
      hindiLabel: 'लिखित शिकायत',
      icon: '📝',
      path: '/complaint'
    },
    {
      id: 'track-complaint',
      label: 'Track Complaint',
      hindiLabel: 'शिकायत ट्रैक करें',
      icon: '🔍',
      path: '/trackstatus'
    },
     {
      id: 'nearby-complaints',
      label: 'Nearby Complaints',
      hindiLabel: 'आसपास की शिकायतें',
      icon: '🏘️',
      path: '/women-child-complaint'
    },
   
    {
      id: 'profile',
      label: 'Profile',
      hindiLabel: 'प्रोफाइल',
      icon: '👤',
      path: '/profile'
    }
  ];

  const stats = [
    { 
      label: 'Total Complaints', 
      hindiLabel: 'कुल शिकायतें', 
      value: userStats.totalComplaints.toString(), 
      color: 'blue' 
    },
    { 
      label: 'Pending', 
      hindiLabel: 'लंबित', 
      value: userStats.pending.toString(), 
      color: 'amber' 
    },
    { 
      label: 'Resolved', 
      hindiLabel: 'हल', 
      value: userStats.resolved.toString(), 
      color: 'green' 
    },
    { 
      label: 'In Progress', 
      hindiLabel: 'प्रगति में', 
      value: userStats.inProgress.toString(), 
      color: 'purple' 
    }
  ];

  const handleMenuClick = (item) => {
    setActiveSection(item.id);
    if (item.path && item.path !== '/dashboard') {
      navigate(item.path);
    }
    setSidebarOpen(false);
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'resolved':
        return 'bg-green-100 text-green-700';
      case 'in progress':
        return 'bg-purple-100 text-purple-700';
      case 'pending':
        return 'bg-amber-100 text-amber-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getProfileImage = () => {
    if (user?.photo) {
      // If photo is a full URL, use it directly
      if (user.photo.startsWith('http')) {
        return user.photo;
      }
      // If photo is a relative path, construct full URL
      return `http://localhost:5000/${user.photo}`;
    }
    return null;
  };

  const getInitials = () => {
    if (!user?.name) return 'U';
    return user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  };

  // Function to get priority color
  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'text-red-600';
      case 'medium':
        return 'text-yellow-600';
      case 'low':
        return 'text-green-600';
      default:
        return 'text-gray-600';
    }
  };

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 font-medium">Loading your dashboard...</p>
          <p className="text-sm text-gray-500">आपका डैशबोर्ड लोड हो रहा है...</p>
        </div>
      </div>
    );
  }

  // Error state - no user data
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-100">
        <div className="text-center bg-white rounded-3xl p-8 shadow-xl">
          <div className="text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-red-600 mb-4">Session Expired</h2>
          <p className="text-gray-600 mb-6">Please login again to continue</p>
          <button
            onClick={() => navigate('/login')}
            className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        ></div>
      )}

      {/* Sidebar */}
      <div className={`fixed lg:sticky top-0 left-0 h-screen w-80 bg-white/95 backdrop-blur-sm shadow-2xl transform transition-transform duration-300 z-50 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } lg:translate-x-0 lg:shadow-none border-r border-white/20`}>
        
        {/* Sidebar Header */}
        <div className="p-6 border-b border-gray-200/50 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-2xl font-bold backdrop-blur-sm border border-white/30 overflow-hidden">
              {getProfileImage() ? (
                <img 
                  src={getProfileImage()} 
                  alt="Profile" 
                  className="w-full h-full rounded-full object-cover"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'flex';
                  }}
                />
              ) : null}
              <div className={`w-full h-full rounded-full flex items-center justify-center ${getProfileImage() ? 'hidden' : 'flex'}`}>
                {getInitials()}
              </div>
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-bold text-lg truncate">नमस्ते, {user.name}!</h3>
            </div>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="p-4 space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => handleMenuClick(item)}
              className={`w-full flex items-center space-x-4 px-4 py-3 rounded-xl text-left transition-all duration-200 ${
                activeSection === item.id
                  ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-lg scale-105'
                  : 'text-gray-700 hover:bg-gradient-to-r hover:from-gray-100 hover:to-blue-50 hover:text-blue-700'
              }`}
            >
              <span className="text-2xl">{item.icon}</span>
              <div className="flex-1">
                <div className="font-medium">{item.label}</div>
                <div className="text-xs opacity-75">{item.hindiLabel}</div>
              </div>
            </button>
          ))}
        </nav>

        {/* Logout Button */}
        <div className="absolute bottom-6 left-4 right-4">
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            <span>🚪</span>
            <span className="font-medium">Logout / लॉगआउट</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 min-h-screen">
        {/* Top Bar */}
        <header className="bg-white/80 backdrop-blur-sm shadow-lg border-b border-white/20 sticky top-0 z-30">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                शिकायत पोर्टल डैशबोर्ड
              </h1>
            </div>
            
            {/* User Info in Top Bar */}
            <div className="flex items-center space-x-4">
              <div className="hidden md:block text-right">
                <div className="font-medium text-gray-900">{user.name}</div>
                <div className="text-sm text-gray-600">{user.email}</div>
              </div>
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-bold shadow-lg overflow-hidden">
                {getProfileImage() ? (
                  <img 
                    src={getProfileImage()} 
                    alt="Profile" 
                    className="w-full h-full rounded-full object-cover"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                ) : null}
                <div className={`w-full h-full rounded-full flex items-center justify-center ${getProfileImage() ? 'hidden' : 'flex'}`}>
                  {getInitials()}
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="p-6">  

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => (
              <div key={index} className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 hover:shadow-xl transition-all duration-300 hover:scale-105">
                <div className="flex items-center justify-between mb-4">
                  <div className={`w-12 h-12 bg-gradient-to-br from-${stat.color}-500 to-${stat.color}-600 rounded-xl flex items-center justify-center text-white text-xl font-bold shadow-lg`}>
                    {stat.value}
                  </div>
                </div>
                <h3 className="font-bold text-gray-900 text-lg">{stat.label}</h3>
                <p className="text-gray-600 text-sm">{stat.hindiLabel}</p>
              </div>
            ))}
          </div>

      {/* Recent Complaints and Community Engagement */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <div className="bg-white/80 backdrop-blur-sm rounded-3xl p-8 shadow-lg border border-white/20">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Recent Complaints / हाल की शिकायतें</h3>
              <div className="space-y-4">
                {recentComplaints.length > 0 ? (
                  recentComplaints.map((complaint) => (
                    <div key={complaint.id || complaint.complaintId} className="p-4 bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl border border-gray-200/50 hover:shadow-md transition-all duration-300">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-bold text-blue-600">{complaint.complaintId || complaint.id}</span>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(complaint.status)}`}>
                          {complaint.status}
                        </span>
                      </div>
                      <h4 className="font-medium text-gray-900">{complaint.title || complaint.subject}</h4>
                      <p className="text-sm text-gray-600 line-clamp-2">{complaint.description}</p>
                      <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
                        <span>{formatDate(complaint.createdAt || complaint.date)}</span>
                        <span className="font-medium">{complaint.priority || 'Medium'} Priority</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8">
                    <div className="text-4xl mb-4">📝</div>
                    <p className="text-gray-600 font-medium">No complaints found</p>
                    <p className="text-sm text-gray-500">कोई शिकायत नहीं मिली</p>
                    <button
                      onClick={() => handleMenuClick(menuItems[3])}
                      className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
                    >
                      File New Complaint
                    </button>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-3xl p-8 shadow-lg border border-white/20">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Community Engagement / सामुदायिक सहभागिता</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-2xl">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white">
                      🏘️
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">View Nearby Issues</div>
                      <div className="text-sm text-gray-600">See complaints in your area</div>
                    </div>
                  </div>
                  <button
                    onClick={() => handleMenuClick(menuItems[1])}
                    className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors text-sm font-medium"
                  >
                    Explore
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center text-white">
                      👍
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">Vote on Issues</div>
                      <div className="text-sm text-gray-600">Support community complaints</div>
                    </div>
                  </div>
                  <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                    New Feature
                  </span>
                </div>

                <div className="p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-2xl">
                  <div className="flex items-center space-x-3 mb-2">
                    <div className="w-8 h-8 bg-amber-500 rounded-full flex items-center justify-center text-white text-sm">
                      💡
                    </div>
                    <div className="font-medium text-gray-900">Pro Tip</div>
                  </div>
                  <p className="text-sm text-gray-600">
                    Upvote nearby complaints that affect you to help prioritize community issues and get faster resolution.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Help Section */}
          <div className="bg-gradient-to-r from-amber-500 to-orange-500 rounded-3xl p-8 text-white shadow-2xl">
            <div className="flex items-center space-x-4">
              <div className="text-4xl">💡</div>
              <div>
                <h3 className="text-2xl font-bold mb-2">Need Help? / मदद चाहिए?</h3>
                <p className="text-amber-100 mb-4">
                  Our support team is available 24/7 to assist you with your complaints and queries.
                  <br />
                  <span className="text-sm">हमारी सहायता टीम आपकी शिकायतों में 24/7 मदद के लिए उपलब्ध है।</span>
                </p>
                <button 
                  onClick={() => handleMenuClick(menuItems.find(item => item.id === 'help'))}
                  className="bg-white text-amber-600 px-6 py-3 rounded-xl font-medium hover:bg-amber-50 transition-colors shadow-lg"
                >
                  Contact Support / संपर्क करें
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}