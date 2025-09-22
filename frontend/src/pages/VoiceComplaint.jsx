// // import React, { useState } from "react";
// // import axios from "axios";

// // export default function VoiceComplaint() {
// //   const [logs, setLogs] = useState([]);
// //   const [loading, setLoading] = useState(false);
// //   const [complaintId, setComplaintId] = useState(null);
// //   const [submitted, setSubmitted] = useState(false);

// //   const appendLog = (line) => {
// //     setLogs((prev) => [...prev, line]);
// //   };

// //   const handleVoiceComplaint = async () => {
// //     setLoading(true);
// //     setLogs(["🎙️ Voice complaint started..."]);
// //     setSubmitted(false);
// //     setComplaintId(null);

// //     try {
// //       // 1. Trigger the Python voice bot and get structured data
// //       const voiceRes = await axios.get("http://localhost:5000/api/");
// //       if (voiceRes.data.status !== "success") {
// //         appendLog("❌ Voice bot error: " + voiceRes.data.message);
// //         return;
// //       }

// //       const complaintData = voiceRes.data.data;
// //       appendLog("✅ Voice bot finished. Data:");
// //       appendLog(JSON.stringify(complaintData, null, 2));

// //       // 2. Send that same data to the complaints endpoint
// //       const formRes = await axios.post(
// //         "http://localhost:5000/api/complaint",
// //         {
// //           name: complaintData["शिकायतकर्ता का नाम"] || complaintData.name,
// //           complaint: complaintData["शिकायत"] || complaintData.complaint,
// //           location: complaintData["स्थान"] || complaintData.location,
// //           // map any other fields if needed
// //         }
// //       );

// //       // 3. Capture and display the Complaint ID
// //       const newId = formRes.data.complaintId || formRes.data.complaintId;
// //       setComplaintId(newId);
// //       setSubmitted(true);
// //       appendLog(`📬 Complaint submitted. ID: ${newId}`);
// //     } catch (err) {
// //       appendLog("❌ Error: " + err.message);
// //     } finally {
// //       setLoading(false);
// //     }
// //   };

// //   return (
// //     <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
// //       <h2 className="text-2xl font-semibold mb-4">Voice Complaint</h2>
// //       <button
// //         onClick={handleVoiceComplaint}
// //         disabled={loading}
// //         className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
// //       >
// //         {loading ? "Processing..." : "Start Voice Complaint"}
// //       </button>

// //       <div className="mt-6 bg-gray-900 text-green-200 p-4 rounded font-mono h-48 overflow-y-scroll">
// //         {logs.map((line, i) => (
// //           <div key={i}>{line}</div>
// //         ))}
// //       </div>

// //       {submitted && (
// //         <div className="mt-6 text-green-700 font-semibold">
// //           Complaint submitted successfully!<br />
// //           Your Complaint ID: <span className="font-bold">{complaintId}</span>
// //         </div>
// //       )}
// //     </div>
// //   );
// // }


// import React, { useState, useEffect } from "react";
// import { Phone, PhoneCall, Mic, MicOff, Volume2, VolumeX } from "lucide-react";

// export default function VoiceComplaint() {
//   const [callState, setCallState] = useState("idle"); // idle, calling, connected, ended
//   const [isListening, setIsListening] = useState(false);
//   const [isSpeaking, setIsSpeaking] = useState(false);
//   const [callDuration, setCallDuration] = useState(0);
//   const [logs, setLogs] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [complaintId, setComplaintId] = useState(null);
//   const [submitted, setSubmitted] = useState(false);
//   const [currentStep, setCurrentStep] = useState("");

//   // Timer for call duration
//   useEffect(() => {
//     let interval;
//     if (callState === "connected") {
//       interval = setInterval(() => {
//         setCallDuration(prev => prev + 1);
//       }, 1000);
//     }
//     return () => clearInterval(interval);
//   }, [callState]);

//   const formatTime = (seconds) => {
//     const mins = Math.floor(seconds / 60);
//     const secs = seconds % 60;
//     return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
//   };

//   const appendLog = (line, type = "info") => {
//     setLogs((prev) => [...prev, { message: line, type, time: new Date().toLocaleTimeString() }]);
//   };

//   const startCall = async () => {
//     setCallState("calling");
//     setCallDuration(0);
//     setLogs([]);
//     setComplaintId(null);
//     setSubmitted(false);
//     setCurrentStep("Connecting to JantaVoice...");
    
//     // Simulate connecting
//     setTimeout(() => {
//       setCallState("connected");
//       setCurrentStep("Connected - Starting voice complaint process");
//       appendLog("🔗 Connected to JantaVoice system", "success");
//       handleVoiceComplaint();
//     }, 2000);
//   };

//   const endCall = () => {
//     setCallState("ended");
//     setIsListening(false);
//     setIsSpeaking(false);
//     setCurrentStep(submitted ? "Call completed successfully" : "Call ended");
//     setTimeout(() => {
//       setCallState("idle");
//       setCurrentStep("");
//     }, 3000);
//   };

//   const handleVoiceComplaint = async () => {
//     setLoading(true);
//     setIsSpeaking(true);
//     appendLog("🎙️ Voice complaint started...", "info");
//     setCurrentStep("Processing voice input...");

//     try {
//       // 1. Trigger the Python voice bot and get structured data
//       setCurrentStep("Connecting to voice bot...");
//       appendLog("📞 Connecting to voice bot system...", "info");
      
//       const voiceRes = await fetch("http://localhost:5000/api/voice-complaint");
//       const voiceData = await voiceRes.json();
      
//       if (voiceData.status !== "success") {
//         appendLog("❌ Voice bot error: " + voiceData.message, "error");
//         setCurrentStep("Voice bot connection failed");
//         setIsSpeaking(false);
//         return;
//       }

//       const complaintData = voiceData.data;
//       setIsSpeaking(false);
//       setCurrentStep("Voice conversation completed");
//       appendLog("✅ Voice bot finished. Data collected:", "success");
//       appendLog(JSON.stringify(complaintData, null, 2), "data");

//       // Show conversation details in a user-friendly way
//       if (complaintData["शिकायत"]) {
//         appendLog(`📝 Complaint: ${complaintData["शिकायत"]}`, "conversation");
//       }
//       if (complaintData["स्थान"]) {
//         appendLog(`📍 Location: ${complaintData["स्थान"]}`, "conversation");
//       }
//       if (complaintData["शिकायतकर्ता का नाम"]) {
//         appendLog(`👤 Name: ${complaintData["शिकायतकर्ता का नाम"]}`, "conversation");
//       }
//       if (complaintData["मोबाइल नंबर"]) {
//         appendLog(`📱 Phone: ${complaintData["मोबाइल नंबर"]}`, "conversation");
//       }
//       if (complaintData["विभाग"]) {
//         appendLog(`🏢 Department: ${complaintData["विभाग"]}`, "conversation");
//       }

//       // 2. Send that same data to the complaints endpoint
//       setCurrentStep("Submitting to admin dashboard...");
//       appendLog("📤 Submitting complaint to admin dashboard...", "info");
      
//       const formRes = await fetch("http://localhost:5000/api/complaint", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({
//             name: complaintData["शिकायतकर्ता का नाम"] || complaintData.name || "Kunal Thakare",
//             description: complaintData["शिकायत"] || complaintData.complaint || "No description",
//             location: complaintData["स्थान"] || complaintData.location || "Unknown",
//             urgency: "normal", // Add missing urgency field
//             department: complaintData["विभाग"] || complaintData.department || "General",
//         }),

//       });

//       const formData = await formRes.json();

//       // 3. Capture and display the Complaint ID
//       const newId = formData.complaintId || complaintData.complaint_id || "CMP-" + Date.now();
//       setComplaintId(newId);
//       setSubmitted(true);
//       setCurrentStep("Complaint registered successfully!");
//       appendLog(`📬 Complaint submitted to admin dashboard!`, "success");
//       appendLog(`🆔 Complaint ID: ${newId}`, "success");
//       appendLog("✅ Admin will review and take action soon", "success");

//     } catch (err) {
//       appendLog("❌ Error: " + err.message, "error");
//       setCurrentStep("Error occurred during processing");
//     } finally {
//       setLoading(false);
//       setIsSpeaking(false);
//       setIsListening(false);
//     }
//   };

//   const getLogIcon = (type) => {
//     switch (type) {
//       case "success": return "✅";
//       case "error": return "❌";
//       case "conversation": return "💬";
//       case "data": return "📊";
//       default: return "ℹ️";
//     }
//   };

//   const getLogColor = (type) => {
//     switch (type) {
//       case "success": return "text-green-400";
//       case "error": return "text-red-400";
//       case "conversation": return "text-blue-400";
//       case "data": return "text-yellow-400";
//       default: return "text-gray-300";
//     }
//   };

//   return (
//     <div className="max-w-md mx-auto mt-10 bg-gradient-to-b from-gray-900 to-gray-800 rounded-3xl p-6 text-white shadow-2xl">
//       {/* Header */}
//       <div className="text-center mb-8">
//         <h2 className="text-xl font-semibold mb-2">जनता वॉइस</h2>
//         <div className="text-sm text-gray-300">आवाज़ शिकायत प्रणाली</div>
//       </div>

//       {/* Call Status */}
//       <div className="text-center mb-8">
//         {callState === "idle" && (
//           <div>
//             <div className="w-24 h-24 mx-auto mb-4 bg-green-600 rounded-full flex items-center justify-center">
//               <Phone size={32} />
//             </div>
//             <div className="text-lg">कॉल करने के लिए तैयार</div>
//             <div className="text-sm text-gray-400">वॉइस शिकायत शुरू करने के लिए टैप करें</div>
//           </div>
//         )}

//         {callState === "calling" && (
//           <div>
//             <div className="w-24 h-24 mx-auto mb-4 bg-yellow-600 rounded-full flex items-center justify-center animate-pulse">
//               <PhoneCall size={32} />
//             </div>
//             <div className="text-lg">Connecting...</div>
//             <div className="text-sm text-gray-400">Please wait</div>
//           </div>
//         )}

//         {callState === "connected" && (
//           <div>
//             <div className="w-24 h-24 mx-auto mb-4 bg-green-600 rounded-full flex items-center justify-center relative">
//               <PhoneCall size={32} />
//               {(isListening || isSpeaking) && (
//                 <div className="absolute -inset-2 border-4 border-green-400 rounded-full animate-ping"></div>
//               )}
//             </div>
//             <div className="text-lg">Connected</div>
//             <div className="text-sm text-gray-400">Duration: {formatTime(callDuration)}</div>
//             <div className="text-xs text-blue-400 mt-1">{currentStep}</div>
//           </div>
//         )}

//         {callState === "ended" && (
//           <div>
//             <div className="w-24 h-24 mx-auto mb-4 bg-red-600 rounded-full flex items-center justify-center">
//               <Phone size={32} />
//             </div>
//             <div className="text-lg">Call Ended</div>
//             <div className="text-sm text-gray-400">
//               {complaintId ? `Complaint ID: ${complaintId}` : "Call completed"}
//             </div>
//           </div>
//         )}
//       </div>

//       {/* Status Indicators */}
//       {callState === "connected" && (
//         <div className="flex justify-center space-x-8 mb-6">
//           <div className={`flex items-center space-x-2 ${isSpeaking ? 'text-blue-400' : 'text-gray-500'}`}>
//             {isSpeaking ? <Volume2 size={20} /> : <VolumeX size={20} />}
//             <span className="text-sm">Bot</span>
//           </div>
//           <div className={`flex items-center space-x-2 ${isListening ? 'text-green-400' : 'text-gray-500'}`}>
//             {isListening ? <Mic size={20} /> : <MicOff size={20} />}
//             <span className="text-sm">You</span>
//           </div>
//         </div>
//       )}

//       {/* Call Controls */}
//       <div className="flex justify-center space-x-4 mb-6">
//         {callState === "idle" && (
//           <button
//             onClick={startCall}
//             disabled={loading}
//             className="w-16 h-16 bg-green-600 hover:bg-green-700 disabled:opacity-50 rounded-full flex items-center justify-center transition-colors"
//           >
//             <Phone size={24} />
//           </button>
//         )}

//         {(callState === "connected" || callState === "calling") && (
//           <button
//             onClick={endCall}
//             className="w-16 h-16 bg-red-600 hover:bg-red-700 rounded-full flex items-center justify-center transition-colors"
//           >
//             <Phone size={24} className="transform rotate-45" />
//           </button>
//         )}
//       </div>

//       {/* Real-time Logs */}
//       {logs.length > 0 && (
//         <div className="bg-gray-800 rounded-lg p-4 max-h-64 overflow-y-auto mb-4">
//           <div className="text-sm text-gray-400 mb-2">Live Process Log:</div>
//           {logs.map((log, index) => (
//             <div key={index} className="mb-2 text-sm">
//               <div className={`${getLogColor(log.type)} break-words`}>
//                 <span className="mr-2">{getLogIcon(log.type)}</span>
//                 {log.message}
//                 <div className="text-xs opacity-50 ml-6">{log.time}</div>
//               </div>
//             </div>
//           ))}
//         </div>
//       )}

//       {/* Success Message */}
//       {submitted && (
//         <div className="p-4 bg-green-900 border border-green-600 rounded-lg text-center">
//           <div className="text-green-400 font-semibold">✅ Complaint Registered!</div>
//           <div className="text-sm text-green-300 mt-1">ID: {complaintId}</div>
//           <div className="text-xs text-green-200 mt-2">
//             Your complaint has been sent to the admin dashboard
//           </div>
//         </div>
//       )}

//       {/* Loading Indicator */}
//       {loading && (
//         <div className="text-center text-blue-400">
//           <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-400 mx-auto mb-2"></div>
//           <div className="text-sm">Processing...</div>
//         </div>
//       )}
//     </div>
//   );
// }


import React, { useState, useEffect, useRef } from "react";
import { Phone, PhoneCall, Mic, MicOff, Volume2, VolumeX } from "lucide-react";

export default function VoiceComplaint() {
  const [callState, setCallState] = useState("idle"); // idle, calling, connected, ended
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [callDuration, setCallDuration] = useState(0);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [complaintId, setComplaintId] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [currentStep, setCurrentStep] = useState("");
  
  // Add ref to track if call should be aborted
  const abortControllerRef = useRef(null);
  const callAbortedRef = useRef(false);

  // Timer for call duration
  useEffect(() => {
    let interval;
    if (callState === "connected") {
      interval = setInterval(() => {
        setCallDuration(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [callState]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const appendLog = (line, type = "info") => {
    // Only append log if call hasn't been aborted
    if (!callAbortedRef.current) {
      setLogs((prev) => [...prev, { message: line, type, time: new Date().toLocaleTimeString() }]);
    }
  };

  const startCall = async () => {
    setCallState("calling");
    setCallDuration(0);
    setLogs([]);
    setComplaintId(null);
    setSubmitted(false);
    setCurrentStep("Connecting to JantaVoice...");
    callAbortedRef.current = false;
    
    // Create new abort controller for this call
    abortControllerRef.current = new AbortController();
    
    // Simulate connecting
    setTimeout(() => {
      if (!callAbortedRef.current) {
        setCallState("connected");
        setCurrentStep("Connected - Starting voice complaint process");
        appendLog("🔗 Connected to JantaVoice system", "success");
        handleVoiceComplaint();
      }
    }, 2000);
  };

  const endCall = () => {
    // Set abort flag immediately
    callAbortedRef.current = true;
    
    // Abort any ongoing fetch requests
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    // Reset all states immediately
    setCallState("ended");
    setIsListening(false);
    setIsSpeaking(false);
    setLoading(false);
    setCurrentStep("Call ended by user");
    
    // Add final log entry
    setLogs(prev => [...prev, { 
      message: "📞 Call terminated by user", 
      type: "info", 
      time: new Date().toLocaleTimeString() 
    }]);
    
    setTimeout(() => {
      setCallState("idle");
      setCurrentStep("");
    }, 3000);
  };

  const handleVoiceComplaint = async () => {
    // Check if call was aborted before starting
    if (callAbortedRef.current) return;
    
    setLoading(true);
    setIsSpeaking(true);
    appendLog("🎙️ Voice complaint started...", "info");
    setCurrentStep("Processing voice input...");

    try {
      // 1. Trigger the Python voice bot and get structured data
      setCurrentStep("Connecting to voice bot...");
      appendLog("📞 Connecting to voice bot system...", "info");
      
      // Check abort before fetch
      if (callAbortedRef.current) return;
      
      // Add timeout to the fetch request (30 seconds)
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Request timeout')), 30000);
      });
      
      const fetchPromise = fetch("http://localhost:5000/api/voice-complaint", {
        signal: abortControllerRef.current?.signal
      });
      
      const voiceRes = await Promise.race([fetchPromise, timeoutPromise]);
      
      // Check abort after fetch
      if (callAbortedRef.current) return;
      
      const voiceData = await voiceRes.json();
      
      if (voiceData.status !== "success") {
        if (!callAbortedRef.current) {
          appendLog("❌ Voice bot error: " + voiceData.message, "error");
          setCurrentStep("Voice bot connection failed");
          setIsSpeaking(false);
        }
        return;
      }

      // Check abort before processing data
      if (callAbortedRef.current) return;

      const complaintData = voiceData.data;
      setIsSpeaking(false);
      setCurrentStep("Voice conversation completed");
      appendLog("✅ Voice bot finished. Data collected:", "success");
      appendLog(JSON.stringify(complaintData, null, 2), "data");

      // Show conversation details in a user-friendly way
      if (complaintData["शिकायत"]) {
        appendLog(`📝 Complaint: ${complaintData["शिकायत"]}`, "conversation");
      }
      if (complaintData["स्थान"]) {
        appendLog(`📍 Location: ${complaintData["स्थान"]}`, "conversation");
      }
      if (complaintData["शिकायतकर्ता का नाम"]) {
        appendLog(`👤 Name: ${complaintData["शिकायतकर्ता का नाम"]}`, "conversation");
      }
      if (complaintData["मोबाइल नंबर"]) {
        appendLog(`📱 Phone: ${complaintData["मोबाइल नंबर"]}`, "conversation");
      }
      if (complaintData["विभाग"]) {
        appendLog(`🏢 Department: ${complaintData["विभाग"]}`, "conversation");
      }

      // Check abort before submitting
      if (callAbortedRef.current) return;

      // 2. Send that same data to the complaints endpoint
      setCurrentStep("Submitting to admin dashboard...");
      appendLog("📤 Submitting complaint to admin dashboard...", "info");
      
      const formRes = await fetch("http://localhost:5000/api/complaint", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: complaintData["शिकायतकर्ता का नाम"] || complaintData.name || "Kunal Thakare",
            description: complaintData["शिकायत"] || complaintData.complaint || "No description",
            location: complaintData["स्थान"] || complaintData.location || "Unknown",
            urgency: "normal", // Add missing urgency field
            department: complaintData["विभाग"] || complaintData.department || "General",
        }),
        signal: abortControllerRef.current?.signal
      });

      // Check abort after final submit
      if (callAbortedRef.current) return;

      const formData = await formRes.json();

      // 3. Capture and display the Complaint ID
      const newId = formData.complaintId || complaintData.complaint_id || "CMP-" + Date.now();
      setComplaintId(newId);
      setSubmitted(true);
      setCurrentStep("Complaint registered successfully!");
      appendLog(`📬 Complaint submitted to admin dashboard!`, "success");
      appendLog(`🆔 Complaint ID: ${newId}`, "success");
      appendLog("✅ Admin will review and take action soon", "success");

    } catch (err) {
      // Only log errors if call wasn't aborted
      if (!callAbortedRef.current) {
        if (err.name === 'AbortError') {
          appendLog("🚫 Request cancelled by user", "info");
          setCurrentStep("Call cancelled by user");
        } else if (err.message === 'Request timeout') {
          appendLog("⏰ Voice bot request timed out", "error");
          setCurrentStep("Voice bot connection timed out");
        } else {
          appendLog("❌ Error: " + err.message, "error");
          setCurrentStep("Error occurred during processing");
        }
      }
    } finally {
      // Only update states if call wasn't aborted
      if (!callAbortedRef.current) {
        setLoading(false);
        setIsSpeaking(false);
        setIsListening(false);
      }
    }
  };

  const getLogIcon = (type) => {
    switch (type) {
      case "success": return "✅";
      case "error": return "❌";
      case "conversation": return "💬";
      case "data": return "📊";
      default: return "ℹ️";
    }
  };

  const getLogColor = (type) => {
    switch (type) {
      case "success": return "text-green-400";
      case "error": return "text-red-400";
      case "conversation": return "text-blue-400";
      case "data": return "text-yellow-400";
      default: return "text-gray-300";
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 bg-gradient-to-b from-gray-900 to-gray-800 rounded-3xl p-6 text-white shadow-2xl">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-xl font-semibold mb-2">जनता वॉइस</h2>
        <div className="text-sm text-gray-300">आवाज़ शिकायत प्रणाली</div>
      </div>

      {/* Call Status */}
      <div className="text-center mb-8">
        {callState === "idle" && (
          <div>
            <div className="w-24 h-24 mx-auto mb-4 bg-green-600 rounded-full flex items-center justify-center">
              <Phone size={32} />
            </div>
            <div className="text-lg">कॉल करने के लिए तैयार</div>
            <div className="text-sm text-gray-400">वॉइस शिकायत शुरू करने के लिए टैप करें</div>
          </div>
        )}

        {callState === "calling" && (
          <div>
            <div className="w-24 h-24 mx-auto mb-4 bg-yellow-600 rounded-full flex items-center justify-center animate-pulse">
              <PhoneCall size={32} />
            </div>
            <div className="text-lg">Connecting...</div>
            <div className="text-sm text-gray-400">Please wait</div>
          </div>
        )}

        {callState === "connected" && (
          <div>
            <div className="w-24 h-24 mx-auto mb-4 bg-green-600 rounded-full flex items-center justify-center relative">
              <PhoneCall size={32} />
              {(isListening || isSpeaking) && (
                <div className="absolute -inset-2 border-4 border-green-400 rounded-full animate-ping"></div>
              )}
            </div>
            <div className="text-lg">Connected</div>
            <div className="text-sm text-gray-400">Duration: {formatTime(callDuration)}</div>
            <div className="text-xs text-blue-400 mt-1">{currentStep}</div>
          </div>
        )}

        {callState === "ended" && (
          <div>
            <div className="w-24 h-24 mx-auto mb-4 bg-red-600 rounded-full flex items-center justify-center">
              <Phone size={32} />
            </div>
            <div className="text-lg">Call Ended</div>
            <div className="text-sm text-gray-400">
              {complaintId ? `Complaint ID: ${complaintId}` : "Call completed"}
            </div>
          </div>
        )}
      </div>

      {/* Status Indicators */}
      {callState === "connected" && (
        <div className="flex justify-center space-x-8 mb-6">
          <div className={`flex items-center space-x-2 ${isSpeaking ? 'text-blue-400' : 'text-gray-500'}`}>
            {isSpeaking ? <Volume2 size={20} /> : <VolumeX size={20} />}
            <span className="text-sm">Bot</span>
          </div>
          <div className={`flex items-center space-x-2 ${isListening ? 'text-green-400' : 'text-gray-500'}`}>
            {isListening ? <Mic size={20} /> : <MicOff size={20} />}
            <span className="text-sm">You</span>
          </div>
        </div>
      )}

      {/* Call Controls */}
      <div className="flex justify-center space-x-4 mb-6">
        {callState === "idle" && (
          <button
            onClick={startCall}
            disabled={loading}
            className="w-16 h-16 bg-green-600 hover:bg-green-700 disabled:opacity-50 rounded-full flex items-center justify-center transition-colors"
          >
            <Phone size={24} />
          </button>
        )}

        {(callState === "connected" || callState === "calling") && (
          <button
            onClick={endCall}
            className="w-16 h-16 bg-red-600 hover:bg-red-700 rounded-full flex items-center justify-center transition-colors"
          >
            <Phone size={24} className="transform rotate-45" />
          </button>
        )}
      </div>

      {/* Real-time Logs */}
      {logs.length > 0 && (
        <div className="bg-gray-800 rounded-lg p-4 max-h-64 overflow-y-auto mb-4">
          <div className="text-sm text-gray-400 mb-2">Live Process Log:</div>
          {logs.map((log, index) => (
            <div key={index} className="mb-2 text-sm">
              <div className={`${getLogColor(log.type)} break-words`}>
                <span className="mr-2">{getLogIcon(log.type)}</span>
                {log.message}
                <div className="text-xs opacity-50 ml-6">{log.time}</div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Success Message */}
      {submitted && (
        <div className="p-4 bg-green-900 border border-green-600 rounded-lg text-center">
          <div className="text-green-400 font-semibold">✅ Complaint Registered!</div>
          <div className="text-sm text-green-300 mt-1">ID: {complaintId}</div>
          <div className="text-xs text-green-200 mt-2">
            Your complaint has been sent to the admin dashboard
          </div>
        </div>
      )}

      {/* Loading Indicator */}
      {loading && (
        <div className="text-center text-blue-400">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-400 mx-auto mb-2"></div>
          <div className="text-sm">Processing...</div>
        </div>
      )}
    </div>
  );
}