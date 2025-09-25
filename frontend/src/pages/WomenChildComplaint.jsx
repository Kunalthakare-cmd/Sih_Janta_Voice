// import React, { useState, useRef } from "react";
// import axios from "axios";

// export default function WomenChildComplaint() {
//   const [recording, setRecording] = useState(false);
//   const [complaintText, setComplaintText] = useState("");
//   const [token, setToken] = useState(null);
//   const [isSubmitting, setIsSubmitting] = useState(false);

//   const recognitionRef = useRef(null); // hold Web Speech API instance

//   // 🔤 Function to convert Hindi → Hinglish
//   const transliterateToHinglish = async (text) => {
//     try {
//       const res = await fetch(
//         `https://inputtools.google.com/request?text=${encodeURIComponent(
//           text
//         )}&itc=hi-t-i0-und&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=demopage`
//       );
//       const data = await res.json();
//       if (data[0] === "SUCCESS") {
//         return data[1][0][1][0]; // Hinglish output
//       }
//       return text;
//     } catch (err) {
//       console.error("Transliteration API error:", err);
//       return text;
//     }
//   };

//   // 🎙️ Single Speak button (toggle start/stop)
//   const handleSpeechToText = () => {
//     const SpeechRecognition =
//       window.SpeechRecognition || window.webkitSpeechRecognition;

//     if (!SpeechRecognition) {
//       alert("Speech recognition is not supported in this browser. Please use Chrome.");
//       return;
//     }

//     // If already recording → stop
//     if (recording) {
//       if (recognitionRef.current) {
//         try {
//           recognitionRef.current.stop();
//         } catch (e) {
//           console.warn("Recognition already stopped.");
//         }
//       }
//       setRecording(false);
//       return;
//     }

//     // New instance
//     const recognition = new SpeechRecognition();
//     recognition.lang = "hi-IN";        // Hindi recognition
//     recognition.continuous = true;     // keep listening
//     recognition.interimResults = true; // show interim text

//     recognition.onresult = async (event) => {
//       let transcript = "";
//       for (let i = 0; i < event.results.length; i++) {
//         transcript += event.results[i][0].transcript + " ";
//       }

//       // 🔤 Convert Hindi → Hinglish
//       const hinglish = await transliterateToHinglish(transcript.trim());
//       setComplaintText(hinglish);
//     };

//     recognition.onerror = (err) => {
//       console.error("Speech Recognition Error:", err);
//       if (err.error === "no-speech") {
//         alert("No speech detected. Please try again and speak closer to the mic.");
//       } else if (err.error === "not-allowed") {
//         alert("Microphone permission is blocked. Please allow mic access in your browser settings.");
//       }
//       setRecording(false);
//     };

//     recognition.onend = () => {
//       setRecording(false);
//     };

//     // Start
//     recognition.start();
//     recognitionRef.current = recognition;
//     setRecording(true);
//   };

//   // 📤 Submit Complaint — attaches live location automatically
//   const handleSubmit = async () => {
//     if (!complaintText.trim()) {
//       alert("Please speak or type your complaint.");
//       return;
//     }

//     setIsSubmitting(true);

//     const submitToServer = async (coords) => {
//       try {
//         const formData = new FormData();
//         formData.append("text", complaintText); // This will be mapped to description in backend
//         formData.append("name", "Anonymous"); // Add default name
//         formData.append("location", "Unknown"); // Add default location
//         formData.append("department", "Police"); // Add department
//         formData.append("urgency", "urgent"); // Add urgency
//         formData.append("category", "Emergency");

//         if (coords) {
//           formData.append("latitude", coords.latitude);
//           formData.append("longitude", coords.longitude);
//         }

//         // Use the correct women-child endpoint
//         const res = await axios.post("http://localhost:5000/api/complaint/women-child", formData, {
//           headers: { "Content-Type": "multipart/form-data" },
//         });

//         if (res.data?.success) {
//           setToken(res.data.token);
//           setComplaintText("");
//           alert(`Complaint submitted successfully${coords ? " with location" : ""}!`);
//         } else {
//           alert(res.data?.message || "Failed to submit complaint.");
//         }
//       } catch (err) {
//         console.error(err);
//         alert("Error submitting complaint.");
//       } finally {
//         setIsSubmitting(false);
//       }
//     };

//     if (!navigator.geolocation) {
//       await submitToServer(null);
//       return;
//     }

//     navigator.geolocation.getCurrentPosition(
//       async (position) => {
//         const { latitude, longitude } = position.coords;
//         await submitToServer({ latitude, longitude });
//       },
//       async (error) => {
//         console.warn("Geolocation error:", error);
//         const proceed = window.confirm(
//           "We couldn't access your location. Submit complaint without location?"
//         );
//         if (proceed) {
//           await submitToServer(null);
//         } else {
//           setIsSubmitting(false);
//         }
//       },
//       {
//         enableHighAccuracy: true,
//         timeout: 10000,
//         maximumAge: 0,
//       }
//     );
//   };

//   return (
//     <div className="max-w-xl mx-auto m-10 p-3 bg-white rounded-2xl shadow-lg">
//       <h2 className="text-2xl font-bold mb-4 text-center text-gray-800">
//         🚨 आपातकालीन शिकायत
//       </h2>

//       {/* 🎙️ Speak */}
//       <button
//         onClick={handleSpeechToText}
//         className={`w-full px-4 py-2 rounded-lg mb-3 font-semibold ${
//           recording ? "bg-red-500" : "bg-purple-600"
//         } text-white`}
//       >
//         {recording ? "बोलना रोकें" : "शिकायत बोलें"}
//       </button>

//       {/* 📝 Complaint Box */}
//       <textarea
//         placeholder="यहाँ अपनी शिकायत टाइप करें या बोलें..."
//         value={complaintText}
//         onChange={(e) => setComplaintText(e.target.value)}
//         className="w-full border rounded-lg p-3 mb-3 h-32 focus:ring-2 focus:ring-blue-400"
//       />

//       {/* 📤 Submit */}
//       <button
//         onClick={handleSubmit}
//         disabled={isSubmitting}
//         className={`w-full ${
//           isSubmitting ? "bg-gray-400" : "bg-green-600"
//         } text-white px-4 py-2 rounded-lg font-semibold`}
//       >
//         {isSubmitting ? "शिकायत दर्ज हो रही है..." : " शिकायत दर्ज करें"}
//       </button>

//       {/* 🎫 Token Display */}
//       {token && (
//         <div className="mt-4 p-4 border rounded-lg bg-gray-100 shadow-sm">
//           <p className="font-semibold text-green-700">✅ आपकी शिकायत सफलतापूर्वक दर्ज कर दी गई है।</p>
//           <p className="text-gray-700">
//             Your Token Number:{" "}
//             <span className="font-mono text-lg text-black">{token}</span>
//           </p>
//         </div>
//       )}

//       <p className="text-xs text-gray-500 mt-3">
//         नोट: सबमिट करने पर लोकेशन अपने आप कैप्चर हो जाएगी (यह HTTPS या localhost पर ही काम करता है)।
//       </p>
//     </div>
//   );
// }


import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const NearbyComplaints = () => {
  const navigate = useNavigate();
  
  const [complaints, setComplaints] = useState([]);
  const [userLocation, setUserLocation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [voting, setVoting] = useState({});
  const [communityStats, setCommunityStats] = useState(null);
  
  // Filter states
  const [filters, setFilters] = useState({
    radius: 400,
    status: 'all',
    department: 'all',
    urgency: 'all'
  });
  
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    totalPages: 0
  });

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('token') || localStorage.getItem('authToken');
      const isUser = localStorage.getItem('isUser');
      
      if (!token || !isUser) {
        navigate('/login');
        return false;
      }
      return true;
    };

    if (checkAuth()) {
      fetchNearbyComplaints();
      fetchCommunityStats();
    }
  }, [navigate, filters, pagination.page]);

  const fetchNearbyComplaints = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token') || localStorage.getItem('authToken');

      const response = await axios.get('http://localhost:5000/api/user/nearby-complaints', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        params: {
          ...filters,
          page: pagination.page,
          limit: pagination.limit
        }
      });

      if (response.data.success) {
        setComplaints(response.data.complaints);
        setUserLocation(response.data.user_location);
        setPagination(prev => ({
          ...prev,
          totalPages: response.data.pagination.total_pages
        }));
        setError('');
      } else {
        setError(response.data.message || 'Failed to fetch nearby complaints');
      }
    } catch (error) {
      console.error('Error fetching nearby complaints:', error);
      if (error.response?.status === 401) {
        navigate('/login');
      } else if (error.response?.data?.error_code === 'NO_USER_LOCATION') {
        setError('Please update your profile with location information to see nearby complaints.');
      } else {
        setError('Failed to load nearby complaints');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchCommunityStats = async () => {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('authToken');

      const response = await axios.get('http://localhost:5000/api/user/community-stats', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        params: {
          radius: filters.radius
        }
      });

      if (response.data.success) {
        setCommunityStats(response.data.stats);
      }
    } catch (error) {
      console.error('Error fetching community stats:', error);
    }
  };

  const handleVote = async (complaintId, voteType) => {
    try {
      setVoting(prev => ({ ...prev, [complaintId]: true }));
      
      const token = localStorage.getItem('token') || localStorage.getItem('authToken');

      const response = await axios.post(`http://localhost:5000/api/complaint/${complaintId}/vote`, {
        vote_type: voteType
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.data.success) {
        // Update the complaint in the list
        setComplaints(prevComplaints => 
          prevComplaints.map(complaint => {
            if (complaint.id === complaintId) {
              return {
                ...complaint,
                upvote_count: response.data.vote_counts.upvotes,
                downvote_count: response.data.vote_counts.downvotes,
                vote_score: response.data.vote_counts.score,
                user_voted: response.data.user_vote
              };
            }
            return complaint;
          })
        );
      }
    } catch (error) {
      console.error('Error voting on complaint:', error);
      setError('Failed to vote on complaint');
    } finally {
      setVoting(prev => ({ ...prev, [complaintId]: false }));
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setPagination(prev => ({ ...prev, page: 1 })); // Reset to first page
  };

  const handlePageChange = (page) => {
    setPagination(prev => ({ ...prev, page }));
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
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

  const getUrgencyColor = (urgency) => {
    switch (urgency?.toLowerCase()) {
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

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading && complaints.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 font-medium">Finding nearby complaints...</p>
          <p className="text-sm text-gray-500">आसपास की शिकायतें खोजी जा रही हैं...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm shadow-lg border-b border-white/20 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
              </button>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  Nearby Complaints
                </h1>
                <p className="text-sm text-gray-600">आसपास की शिकायतें</p>
              </div>
            </div>
            
            {userLocation && (
              <div className="text-right text-sm text-gray-600">
                <div>📍 Your Location</div>
                <div>{userLocation.latitude.toFixed(6)}, {userLocation.longitude.toFixed(6)}</div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Community Stats */}
        {communityStats && (
          <div className="mb-6 bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Community Overview / समुदायिक अवलोकन</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{communityStats.total_complaints}</div>
                <div className="text-sm text-gray-600">Total Complaints</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">{communityStats.total_community_votes}</div>
                <div className="text-sm text-gray-600">Community Votes</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{filters.radius}m</div>
                <div className="text-sm text-gray-600">Search Radius</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-amber-600">{communityStats.most_common_department}</div>
                <div className="text-sm text-gray-600">Top Department</div>
              </div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="mb-6 bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Filters / फिल्टर</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Radius / त्रिज्या
              </label>
              <select
                value={filters.radius}
                onChange={(e) => handleFilterChange('radius', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
              >
                <option value={200}>200m</option>
                <option value={400}>400m</option>
                <option value={800}>800m</option>
                <option value={1500}>1.5km</option>
                <option value={2000}>2km</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status / स्थिति
              </label>
              <select
                value={filters.status}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Statuses</option>
                <option value="Pending">Pending</option>
                <option value="In Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Department / विभाग
              </label>
              <select
                value={filters.department}
                onChange={(e) => handleFilterChange('department', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Departments</option>
                <option value="सड़क विभाग">सड़क विभाग</option>
                <option value="जल विभाग">जल विभाग</option>
                <option value="बिजली विभाग">बिजली विभाग</option>
                <option value="सफाई विभाग">सफाई विभाग</option>
                <option value="स्वास्थ्य विभाग">स्वास्थ्य विभाग</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Urgency / अत्यावश्यकता
              </label>
              <select
                value={filters.urgency}
                onChange={(e) => handleFilterChange('urgency', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Urgencies</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Complaints List */}
        <div className="space-y-4">
          {complaints.length === 0 && !loading ? (
            <div className="text-center bg-white/80 backdrop-blur-sm rounded-2xl p-12 shadow-lg border border-white/20">
              <div className="text-6xl mb-4">🏘️</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">No Nearby Complaints Found</h3>
              <p className="text-gray-600 mb-2">आसपास कोई शिकायत नहीं मिली</p>
              <p className="text-sm text-gray-500">Try increasing the search radius or check back later</p>
              <button
                onClick={() => handleFilterChange('radius', Math.min(filters.radius + 400, 2000))}
                className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
              >
                Increase Search Radius
              </button>
            </div>
          ) : (
            complaints.map((complaint) => (
              <div key={complaint.id} className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 hover:shadow-xl transition-all duration-300">
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className="font-bold text-blue-600">#{complaint.id}</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(complaint.status)}`}>
                        {complaint.status}
                      </span>
                      <span className={`text-sm font-medium ${getUrgencyColor(complaint.urgency)}`}>
                        {complaint.urgency} Priority
                      </span>
                    </div>
                    <h4 className="font-bold text-lg text-gray-900 mb-1">{complaint.department}</h4>
                    <p className="text-sm text-gray-600 mb-2">
                      📍 {complaint.distance_text} • By {complaint.name} • {formatDate(complaint.timestamp)}
                    </p>
                  </div>
                </div>

                {/* Complaint Description */}
                <div className="mb-4">
                  <p className="text-gray-800 leading-relaxed">
                    {complaint.complaint || complaint.description}
                  </p>
                  {complaint.location && (
                    <p className="text-sm text-gray-600 mt-2">
                      📍 Location: {complaint.location}
                    </p>
                  )}
                </div>

                {/* Photo if available */}
                {complaint.photoUrl && (
                  <div className="mb-4">
                    <img
                      src={`http://localhost:5000${complaint.photoUrl}`}
                      alt="Complaint"
                      className="rounded-lg max-h-48 w-auto object-cover cursor-pointer hover:opacity-90 transition-opacity"
                      onClick={() => window.open(`http://localhost:5000${complaint.photoUrl}`, '_blank')}
                    />
                  </div>
                )}

                {/* Voting Section */}
                <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                  <div className="flex items-center space-x-4">
                    {/* Upvote Button */}
                    <button
                      onClick={() => handleVote(complaint.id, complaint.user_voted?.upvoted ? 'remove' : 'upvote')}
                      disabled={voting[complaint.id]}
                      className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                        complaint.user_voted?.upvoted
                          ? 'bg-green-100 text-green-700 hover:bg-green-200'
                          : 'bg-gray-100 text-gray-600 hover:bg-green-100 hover:text-green-700'
                      } ${voting[complaint.id] ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
                      </svg>
                      <span className="font-medium">{complaint.upvote_count}</span>
                    </button>

                    {/* Downvote Button */}
                    <button
                      onClick={() => handleVote(complaint.id, complaint.user_voted?.downvoted ? 'remove' : 'downvote')}
                      disabled={voting[complaint.id]}
                      className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                        complaint.user_voted?.downvoted
                          ? 'bg-red-100 text-red-700 hover:bg-red-200'
                          : 'bg-gray-100 text-gray-600 hover:bg-red-100 hover:text-red-700'
                      } ${voting[complaint.id] ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 10.293a1 1 0 010 1.414l-6 6a1 1 0 01-1.414 0l-6-6a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l4.293-4.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      <span className="font-medium">{complaint.downvote_count}</span>
                    </button>

                    {/* Vote Score */}
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-500">Score:</span>
                      <span className={`font-bold ${
                        complaint.vote_score > 0 ? 'text-green-600' : 
                        complaint.vote_score < 0 ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        {complaint.vote_score > 0 ? '+' : ''}{complaint.vote_score}
                      </span>
                    </div>
                  </div>

                  <div className="text-sm text-gray-500">
                    Distance: {complaint.distance}m
                  </div>
                </div>

                {/* Voting Status */}
                {(complaint.user_voted?.upvoted || complaint.user_voted?.downvoted) && (
                  <div className="mt-2 text-center">
                    <span className={`text-xs px-3 py-1 rounded-full ${
                      complaint.user_voted?.upvoted
                        ? 'bg-green-100 text-green-700'
                        : 'bg-red-100 text-red-700'
                    }`}>
                      You {complaint.user_voted?.upvoted ? 'upvoted' : 'downvoted'} this complaint
                    </span>
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Pagination */}
        {pagination.totalPages > 1 && (
          <div className="mt-8 flex items-center justify-center space-x-2">
            <button
              onClick={() => handlePageChange(pagination.page - 1)}
              disabled={pagination.page === 1}
              className="px-4 py-2 bg-white rounded-lg shadow border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            <div className="flex items-center space-x-1">
              {[...Array(pagination.totalPages)].map((_, index) => {
                const page = index + 1;
                return (
                  <button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    className={`px-3 py-2 rounded-lg ${
                      pagination.page === page
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-gray-600 hover:bg-gray-50'
                    } border border-gray-200`}
                  >
                    {page}
                  </button>
                );
              })}
            </div>
            
            <button
              onClick={() => handlePageChange(pagination.page + 1)}
              disabled={pagination.page === pagination.totalPages}
              className="px-4 py-2 bg-white rounded-lg shadow border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        )}

        {/* Loading indicator for pagination */}
        {loading && complaints.length > 0 && (
          <div className="mt-4 text-center">
            <div className="inline-flex items-center space-x-2 text-gray-600">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <span>Loading...</span>
            </div>
          </div>
        )}

        {/* Help Text */}
        <div className="mt-8 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl p-6 text-white">
          <div className="flex items-start space-x-4">
            <div className="text-3xl">💡</div>
            <div>
              <h3 className="text-lg font-bold mb-2">How Community Voting Works</h3>
              <p className="text-blue-100 text-sm mb-2">
                समुदायिक मतदान कैसे काम करता है
              </p>
              <ul className="text-sm text-blue-100 space-y-1">
                <li>• Upvote complaints that affect you or your area</li>
                <li>• Downvote spam or irrelevant complaints</li>
                <li>• Higher voted complaints get more attention from authorities</li>
                <li>• You can change or remove your vote at any time</li>
                <li>• Only complaints within your area are shown</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NearbyComplaints;