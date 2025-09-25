// // import React, { useState } from "react";
// // import axios from "axios";
// // import PlacesAutocomplete, { geocodeByAddress, getLatLng } from "react-places-autocomplete";

// // export default function ComplaintForm() {
// //   const [formData, setFormData] = useState({
// //     name: "",
// //     complaint: "",
// //     location: "",
// //     urgency: "normal",
// //     department: "",
// //   });

// //   const [photo, setPhoto] = useState(null);
// //   const [complaintId, setComplaintId] = useState(null);
// //   const [submitted, setSubmitted] = useState(false);

// //   const handleChange = (e) => {
// //     setFormData({ ...formData, [e.target.name]: e.target.value });
// //   };

// //   // location select handler
// //   const handleSelect = async (address) => {
// //     setFormData({ ...formData, location: address });
// //     try {
// //       const results = await geocodeByAddress(address);
// //       const latLng = await getLatLng(results[0]);
// //       console.log("Coordinates: ", latLng); // agar latitude/longitude bhi chahiye backend ke liye
// //     } catch (error) {
// //       console.error("Error fetching coordinates", error);
// //     }
// //   };

// //   const handlePhotoChange = (e) => {
// //     if (e.target.files && e.target.files[0]) {
// //       setPhoto(e.target.files[0]);
// //     }
// //   };

// //   const handleSubmit = async (e) => {
// //     e.preventDefault();

// //     try {
// //       const formDataToSend = new FormData();
// //       Object.keys(formData).forEach((key) => {
// //         formDataToSend.append(key, formData[key]);
// //       });
// //       if (photo) {
// //         formDataToSend.append("photo", photo);
// //       }

// //       const res = await axios.post("http://localhost:5000/api/complaint", formDataToSend, {
// //         headers: { "Content-Type": "multipart/form-data" },
// //       });

// //       setComplaintId(res.data.complaint.complaintId);
// //       setSubmitted(true);

// //       setFormData({
// //         name: "",
// //         complaint: "",
// //         location: "",
// //         urgency: "normal",
// //         department: "",
// //       });
// //       setPhoto(null);
// //     } catch (err) {
// //       console.error("Submission failed:", err.message);
// //       alert("Complaint submission failed. Try again.");
// //     }
// //   };

// //   return (
// //     <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
// //       <h2 className="text-2xl font-semibold mb-4">Complaint Form</h2>
// //       <form onSubmit={handleSubmit} className="space-y-4">
// //         <input
// //           name="name"
// //           value={formData.name}
// //           onChange={handleChange}
// //           placeholder="Your Name"
// //           required
// //           className="w-full border px-3 py-2 rounded"
// //         />
// //         <textarea
// //           name="complaint"
// //           value={formData.complaint}
// //           onChange={handleChange}
// //           placeholder="Describe your complaint"
// //           required
// //           className="w-full border px-3 py-2 rounded"
// //         />

// //         {/* Location Autocomplete */}
// //         <PlacesAutocomplete
// //           value={formData.location}
// //           onChange={(address) => setFormData({ ...formData, location: address })}
// //           onSelect={handleSelect}
// //           searchOptions={{ componentRestrictions: { country: ["in"] } }} // restrict to India
// //         >
// //           {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
// //             <div>
// //               <input
// //                 {...getInputProps({
// //                   placeholder: "Search Location (India only)",
// //                   className: "w-full border px-3 py-2 rounded",
// //                 })}
// //               />
// //               <div className="border rounded bg-white mt-1">
// //                 {loading && <div className="p-2 text-gray-500">Loading...</div>}
// //                 {suggestions.map((suggestion) => {
// //                   const className = suggestion.active
// //                     ? "p-2 bg-blue-100 cursor-pointer"
// //                     : "p-2 cursor-pointer";
// //                   return (
// //                     <div
// //                       {...getSuggestionItemProps(suggestion, { className })}
// //                       key={suggestion.placeId}
// //                     >
// //                       {suggestion.description}
// //                     </div>
// //                   );
// //                 })}
// //               </div>
// //             </div>
// //           )}
// //         </PlacesAutocomplete>

// //         {/* Department */}
// //         <select
// //           name="department"
// //           value={formData.department}
// //           onChange={handleChange}
// //           className="w-full border px-3 py-2 rounded"
// //           required
// //         >
// //           <option value="">Select a Department</option>
// //           <option value="Public Works">Public Works</option>
// //           <option value="Water Supply">Water Supply</option>
// //           <option value="Sanitation">Sanitation</option>
// //           <option value="Electricity">Electricity</option>
// //           <option value="Other">Other</option>
// //         </select>

// //         {/* Urgency */}
// //         <select
// //           name="urgency"
// //           value={formData.urgency}
// //           onChange={handleChange}
// //           className="w-full border px-3 py-2 rounded"
// //         >
// //           <option value="normal">Normal</option>
// //           <option value="urgent">Urgent</option>
// //         </select>

// //         {/* Photo Upload */}
// //         <div>
// //           <label className="block text-sm font-medium text-gray-700 mb-1">
// //             Upload / Capture Photo
// //           </label>
// //           <input
// //             type="file"
// //             accept="image/*"
// //             capture="environment"
// //             onChange={handlePhotoChange}
// //             className="w-full border px-3 py-2 rounded"
// //           />
// //           {photo && (
// //             <p className="text-xs text-gray-500 mt-1">Selected: {photo.name}</p>
// //           )}
// //         </div>

// //         <button
// //           type="submit"
// //           className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
// //         >
// //           Submit
// //         </button>
// //       </form>

// //       {submitted && (
// //         <div className="mt-6 text-green-700 font-semibold">
// //           Complaint submitted successfully!<br />
// //           Your Complaint ID: <span className="font-bold">{complaintId}</span>
// //         </div>
// //       )}
// //     </div>
// //   );
// // }
// import React, { useState } from "react";
// import axios from "axios";
// import PlacesAutocomplete, {
//   geocodeByAddress,
//   getLatLng,
// } from "react-places-autocomplete";

// export default function ComplaintForm() {
//   const [formData, setFormData] = useState({
//     name: "",
//     complaint: "",
//     location: "",
//     urgency: "normal",
//     department: "",
//   });

//   const [photo, setPhoto] = useState(null);
//   const [complaintId, setComplaintId] = useState(null);
//   const [submitted, setSubmitted] = useState(false);
//   const [isSubmitting, setIsSubmitting] = useState(false);
//   const [liveCoords, setLiveCoords] = useState(null);

//   const handleChange = (e) => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//   };

//   const handlePhotoChange = (e) => {
//     if (e.target.files && e.target.files[0]) {
//       setPhoto(e.target.files[0]);
//     }
//   };

//   // Google Places Autocomplete handler
//   const handleSelect = async (address) => {
//     setFormData({ ...formData, location: address });
//     setLiveCoords(null); // Clear live coords if user selects an address
//     try {
//       const results = await geocodeByAddress(address);
//       const latLng = await getLatLng(results[0]);
//       console.log("Selected Location Coordinates: ", latLng);
//       // You can store these coords in state if your backend needs them
//     } catch (error) {
//       console.error("Error fetching coordinates", error);
//     }
//   };

//   // Live location button handler
//   const handleLiveLocation = () => {
//     if (!navigator.geolocation) {
//       alert("Geolocation is not supported by your browser.");
//       return;
//     }

//     setIsSubmitting(true);
//     navigator.geolocation.getCurrentPosition(
//       (position) => {
//         const { latitude, longitude } = position.coords;
//         setLiveCoords({ latitude, longitude });
//         setFormData({ ...formData, location: "Live Location Captured" });
//         alert("Live location successfully captured!");
//         setIsSubmitting(false);
//       },
//       (error) => {
//         console.warn("Geolocation error:", error);
//         alert("⚠ Location not available. Please enable GPS for accurate location.");
//         setLiveCoords(null);
//         setIsSubmitting(false);
//       },
//       { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
//     );
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setIsSubmitting(true);

//     try {
//       const formDataToSend = new FormData();
//       Object.keys(formData).forEach((key) => {
//         formDataToSend.append(key, formData[key]);
//       });

//       if (photo) {
//         formDataToSend.append("photo", photo);
//       }

//       // Logic to determine which location to send
//       let latLng = null;
//       if (liveCoords) {
//         // Option 1: Live location is captured
//         latLng = liveCoords;
//       } else if (formData.location) {
//         // Option 2: User typed and selected a location
//         const results = await geocodeByAddress(formData.location);
//         latLng = await getLatLng(results[0]);
//       }

//       if (latLng) {
//         formDataToSend.append("latitude", latLng.latitude);
//         formDataToSend.append("longitude", latLng.longitude);
//       }

//       const res = await axios.post("http://localhost:5000/api/complaint", formDataToSend, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });

//       setComplaintId(res.data.complaint.complaintId);
//       setSubmitted(true);
//       alert(`Complaint submitted successfully! Your Complaint ID is: ${res.data.complaint.complaintId}`);

//       // Reset form
//       setFormData({
//         name: "",
//         complaint: "",
//         location: "",
//         urgency: "normal",
//         department: "",
//       });
//       setPhoto(null);
//       setLiveCoords(null);
//     } catch (err) {
//       console.error("Submission failed:", err.message);
//       alert("Complaint submission failed. Please try again.");
//     } finally {
//       setIsSubmitting(false);
//     }
//   };

//   return (
//     <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
//       <h2 className="text-2xl font-semibold mb-4">Complaint Form</h2>
//       <form onSubmit={handleSubmit} className="space-y-4">
//         {/* Input fields */}
//         <input
//           name="name"
//           value={formData.name}
//           onChange={handleChange}
//           placeholder="Your Name"
//           required
//           className="w-full border px-3 py-2 rounded"
//         />
//         <textarea
//           name="complaint"
//           value={formData.complaint}
//           onChange={handleChange}
//           placeholder="Describe your complaint"
//           required
//           className="w-full border px-3 py-2 rounded"
//         />

//         {/* Location Section */}
//         <div>
//           <label className="block text-sm font-medium text-gray-700 mb-1">
//             Location
//           </label>
//           <div className="flex gap-2">
//             <PlacesAutocomplete
//               value={formData.location}
//               onChange={(address) => {
//                 setFormData({ ...formData, location: address });
//                 setLiveCoords(null);
//               }}
//               onSelect={handleSelect}
//               searchOptions={{ componentRestrictions: { country: ["in"] } }}
//             >
//               {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
//                 <div className="w-full">
//                   <input
//                     {...getInputProps({
//                       placeholder: "Search Location...",
//                       className: "w-full border px-3 py-2 rounded",
//                     })}
//                   />
//                   <div className="border rounded bg-white mt-1">
//                     {loading && <div className="p-2 text-gray-500">Loading...</div>}
//                     {suggestions.map((suggestion) => {
//                       const className = suggestion.active
//                         ? "p-2 bg-blue-100 cursor-pointer"
//                         : "p-2 cursor-pointer";
//                       return (
//                         <div
//                           {...getSuggestionItemProps(suggestion, { className })}
//                           key={suggestion.placeId}
//                         >
//                           {suggestion.description}
//                         </div>
//                       );
//                     })}
//                   </div>
//                 </div>
//               )}
//             </PlacesAutocomplete>
//             <button
//               type="button"
//               onClick={handleLiveLocation}
//               disabled={isSubmitting}
//               className={`px-4 py-2 rounded text-sm text-white ${
//                 isSubmitting ? "bg-gray-400" : "bg-blue-600"
//               }`}
//             >
//               Live
//             </button>
//           </div>
//           {liveCoords && (
//             <p className="text-xs text-green-600 mt-1">
//               Live Location: {liveCoords.latitude.toFixed(4)}, {liveCoords.longitude.toFixed(4)}
//             </p>
//           )}
//         </div>

//         {/* Other form elements */}
//         <select
//           name="department"
//           value={formData.department}
//           onChange={handleChange}
//           className="w-full border px-3 py-2 rounded"
//           required
//         >
//           <option value="">Select a Department</option>
//           <option value="Public Works">Public Works</option>
//           <option value="Water Supply">Water Supply</option>
//           <option value="Sanitation">Sanitation</option>
//           <option value="Electricity">Electricity</option>
//           <option value="Other">Other</option>
//         </select>

//         <select
//           name="urgency"
//           value={formData.urgency}
//           onChange={handleChange}
//           className="w-full border px-3 py-2 rounded"
//         >
//           <option value="normal">Normal</option>
//           <option value="urgent">Urgent</option>
//         </select>

//         <div>
//           <label className="block text-sm font-medium text-gray-700 mb-1">
//             Upload / Capture Photo
//           </label>
//           <input
//             type="file"
//             accept="image/*"
//             capture="environment"
//             onChange={handlePhotoChange}
//             className="w-full border px-3 py-2 rounded"
//           />
//           {photo && (
//             <p className="text-xs text-gray-500 mt-1">Selected: {photo.name}</p>
//           )}
//         </div>

//         <button
//           type="submit"
//           disabled={isSubmitting}
//           className={`w-full ${
//             isSubmitting ? "bg-gray-400" : "bg-blue-600"
//           } text-white px-4 py-2 rounded hover:bg-blue-700`}
//         >
//           {isSubmitting ? "Submitting..." : "Submit Complaint"}
//         </button>
//       </form>

//       {submitted && (
//         <div className="mt-6 text-green-700 font-semibold">
//           Complaint submitted successfully!<br />
//           Your Complaint ID: <span className="font-bold">{complaintId}</span>
//         </div>
//       )}
//     </div>
//   );
// }









// import React, { useState, useRef, useCallback } from "react";
// import axios from "axios";
// import PlacesAutocomplete, {
//   geocodeByAddress,
//   getLatLng,
// } from "react-places-autocomplete";

// export default function ComplaintForm() {
//   const [formData, setFormData] = useState({
//     name: "",
//     complaint: "",
//     location: ""
//   });

//   const [photo, setPhoto] = useState(null);
//   const [photoPreview, setPhotoPreview] = useState(null);
//   const [complaintId, setComplaintId] = useState(null);
//   const [submitted, setSubmitted] = useState(false);
//   const [isSubmitting, setIsSubmitting] = useState(false);
//   const [liveCoords, setLiveCoords] = useState(null);
//   const [recording, setRecording] = useState(false);
//   const [cameraStream, setCameraStream] = useState(null);
//   const [showCamera, setShowCamera] = useState(false);

//   const recognitionRef = useRef(null);
//   const videoRef = useRef(null);
//   const canvasRef = useRef(null);

//   // 🔤 Transliteration (Hindi → Hinglish)
//   const transliterateToHinglish = async (text) => {
//     try {
//       const res = await fetch(
//         `https://inputtools.google.com/request?text=${encodeURIComponent(
//           text
//         )}&itc=hi-t-i0-und&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=demopage`
//       );
//       const data = await res.json();
//       if (data[0] === "SUCCESS") {
//         return data[1][0][1][0];
//       }
//       return text;
//     } catch (err) {
//       console.error("Transliteration API error:", err);
//       return text;
//     }
//   };

//   // 🌍 Reverse Geocoding - Convert coordinates to address
//   const reverseGeocode = async (latitude, longitude) => {
//     try {
//       const response = await fetch(
//         `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}`
//       );
//       const data = await response.json();
      
//       if (data.results && data.results.length > 0) {
//         return data.results[0].formatted_address;
//       }
//       return `Location: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
//     } catch (error) {
//       console.error("Reverse geocoding error:", error);
//       return `Location: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
//     }
//   };

//   // 🎙️ Speech-to-text
//   const handleSpeechToText = () => {
//     const SpeechRecognition =
//       window.SpeechRecognition || window.webkitSpeechRecognition;

//     if (!SpeechRecognition) {
//       alert("Speech recognition is not supported in this browser. Please use Chrome.");
//       return;
//     }

//     if (recording) {
//       recognitionRef.current?.stop();
//       setRecording(false);
//       return;
//     }

//     const recognition = new SpeechRecognition();
//     recognition.lang = "hi-IN";
//     recognition.continuous = true;
//     recognition.interimResults = true;

//     recognition.onresult = async (event) => {
//       let transcript = "";
//       for (let i = 0; i < event.results.length; i++) {
//         transcript += event.results[i][0].transcript + " ";
//       }
//       const hinglish = await transliterateToHinglish(transcript.trim());
//       setFormData((prev) => ({ ...prev, complaint: hinglish }));
//     };

//     recognition.onerror = (err) => {
//       console.error("Speech Recognition Error:", err);
//       setRecording(false);
//     };

//     recognition.onend = () => {
//       setRecording(false);
//     };

//     recognition.start();
//     recognitionRef.current = recognition;
//     setRecording(true);
//   };

//   // 📷 Camera Functions
//   const startCamera = async () => {
//     try {
//       const stream = await navigator.mediaDevices.getUserMedia({
//         video: { facingMode: 'environment' }, // Use back camera
//         audio: false
//       });
      
//       setCameraStream(stream);
//       setShowCamera(true);
      
//       if (videoRef.current) {
//         videoRef.current.srcObject = stream;
//       }
//     } catch (error) {
//       console.error("Camera access error:", error);
//       alert("Unable to access camera. Please check permissions.");
//     }
//   };

//   const stopCamera = () => {
//     if (cameraStream) {
//       cameraStream.getTracks().forEach(track => track.stop());
//       setCameraStream(null);
//     }
//     setShowCamera(false);
//   };

//   const capturePhoto = useCallback(async () => {
//     if (!videoRef.current || !canvasRef.current) return;

//     const video = videoRef.current;
//     const canvas = canvasRef.current;
//     const context = canvas.getContext('2d');

//     // Set canvas dimensions to match video
//     canvas.width = video.videoWidth;
//     canvas.height = video.videoHeight;

//     // Draw current video frame to canvas
//     context.drawImage(video, 0, 0);

//     // Get current location for geo-tagging
//     if (navigator.geolocation) {
//       navigator.geolocation.getCurrentPosition(
//         async (position) => {
//           const { latitude, longitude } = position.coords;
          
//           // Add geo-tag overlay to image
//           context.fillStyle = 'rgba(0, 0, 0, 0.7)';
//           context.fillRect(0, canvas.height - 60, canvas.width, 60);
//           context.fillStyle = 'white';
//           context.font = '14px Arial';
//           context.fillText(`Location: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}`, 10, canvas.height - 35);
//           context.fillText(`Captured: ${new Date().toLocaleString()}`, 10, canvas.height - 15);

//           // Convert to blob
//           canvas.toBlob((blob) => {
//             const file = new File([blob], `complaint_photo_${Date.now()}.jpg`, {
//               type: 'image/jpeg'
//             });
            
//             setPhoto(file);
//             setPhotoPreview(canvas.toDataURL());
//             stopCamera();
//           }, 'image/jpeg', 0.8);
//         },
//         (error) => {
//           console.warn("Location not available for geo-tagging:", error);
//           // Capture without geo-tag
//           canvas.toBlob((blob) => {
//             const file = new File([blob], `complaint_photo_${Date.now()}.jpg`, {
//               type: 'image/jpeg'
//             });
            
//             setPhoto(file);
//             setPhotoPreview(canvas.toDataURL());
//             stopCamera();
//           }, 'image/jpeg', 0.8);
//         },
//         { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
//       );
//     }
//   }, [cameraStream]);

//   const handlePhotoChange = (e) => {
//     if (e.target.files && e.target.files[0]) {
//       const file = e.target.files[0];
//       setPhoto(file);
      
//       // Create preview
//       const reader = new FileReader();
//       reader.onload = (e) => setPhotoPreview(e.target.result);
//       reader.readAsDataURL(file);
//     }
//   };

//   const handleSelect = async (address) => {
//     setFormData({ ...formData, location: address });
//     setLiveCoords(null);
//     try {
//       const results = await geocodeByAddress(address);
//       await getLatLng(results[0]);
//     } catch (error) {
//       console.error("Error fetching coordinates", error);
//     }
//   };

//   const handleLiveLocation = () => {
//     if (!navigator.geolocation) {
//       alert("Geolocation is not supported by your browser.");
//       return;
//     }

//     setIsSubmitting(true);
//     navigator.geolocation.getCurrentPosition(
//       async (position) => {
//         const { latitude, longitude } = position.coords;
//         setLiveCoords({ latitude, longitude });
        
//         // Get human-readable address
//         const address = await reverseGeocode(latitude, longitude);
//         setFormData({ ...formData, location: address });
        
//         alert("Live location successfully captured!");
//         setIsSubmitting(false);
//       },
//       (error) => {
//         console.warn("Geolocation error:", error);
//         alert("⚠ Location not available. Please enable GPS.");
//         setLiveCoords(null);
//         setIsSubmitting(false);
//       },
//       { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
//     );
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!formData.complaint.trim()) {
//       alert("Please speak or type your complaint.");
//       return;
//     }

//     setIsSubmitting(true);
//     try {
//       const formDataToSend = new FormData();
//       formDataToSend.append("complaint", formData.complaint);
//       formDataToSend.append("location", formData.location);
//       formDataToSend.append("name", formData.name);

//       if (photo) {
//         formDataToSend.append("photo", photo);
//       }

//       if (liveCoords) {
//         formDataToSend.append("latitude", liveCoords.latitude);
//         formDataToSend.append("longitude", liveCoords.longitude);
//       }

//       // Add metadata
//       formDataToSend.append("timestamp", new Date().toISOString());
//       formDataToSend.append("hasPhoto", !!photo);
//       formDataToSend.append("hasGeoLocation", !!liveCoords);
//       formDataToSend.append("dashboardSource", "enhanced-complaint-form");
//       formDataToSend.append("submissionType", "form-with-nlp");
//       formDataToSend.append("userAgent", navigator.userAgent);
//       formDataToSend.append("platform", navigator.platform);

//       const res = await axios.post("http://localhost:5000/api/complaint", formDataToSend, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });

//       // Handle backend response
//       const complaintData = res.data.complaint || res.data;
//       const complaintId = complaintData.complaintId || res.data.complaintId;
//       setComplaintId(complaintId);
//       setSubmitted(true);

//       // Reset form
//       setFormData({
//         name: "",
//         complaint: "",
//         location: ""
//       });
//       setPhoto(null);
//       setPhotoPreview(null);
//       setLiveCoords(null);

//       // Show success message
//       alert(`Complaint submitted successfully! Your Complaint ID is: ${complaintId}`);

//     } catch (err) {
//       console.error("Submission failed:", err.message);
//       alert("Complaint submission failed.");
//     } finally {
//       setIsSubmitting(false);
//     }
//   };

//   return (
//     <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
//       <h2 className="text-2xl font-semibold mb-4">Complaint Form</h2>
      
//       {/* Camera Modal */}
//       {showCamera && (
//         <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
//           <div className="bg-white p-4 rounded-lg max-w-md w-full">
//             <div className="relative">
//               <video
//                 ref={videoRef}
//                 autoPlay
//                 playsInline
//                 className="w-full h-64 object-cover rounded"
//               />
//               <div className="flex justify-center space-x-4 mt-4">
//                 <button
//                   onClick={capturePhoto}
//                   className="bg-blue-600 text-white px-4 py-2 rounded"
//                 >
//                   📷 Capture
//                 </button>
//                 <button
//                   onClick={stopCamera}
//                   className="bg-gray-600 text-white px-4 py-2 rounded"
//                 >
//                   Cancel
//                 </button>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}

//       <form onSubmit={handleSubmit} className="space-y-4">
        
//         {/* 🎙️ Voice-to-Text */}
//         <button
//           type="button"
//           onClick={handleSpeechToText}
//           className={`w-full px-4 py-2 rounded-lg font-semibold ${
//             recording ? "bg-red-500" : "bg-purple-600"
//           } text-white`}
//         >
//           {recording ? "🛑 बोलना रोकें" : "🎤 शिकायत बोलें"}
//         </button>

//         {/* Complaint Text */}
//         <textarea
//           name="complaint"
//           value={formData.complaint}
//           onChange={(e) => setFormData({ ...formData, complaint: e.target.value })}
//           placeholder="Describe your complaint or speak..."
//           required
//           className="w-full border px-3 py-2 rounded h-32"
//         />

//         {/* 📍 Location */}
//         <div>
//           <label className="block text-sm font-medium text-gray-700 mb-1">
//             Location
//           </label>
//           <div className="flex gap-2">
//             <PlacesAutocomplete
//               value={formData.location}
//               onChange={(address) => {
//                 setFormData({ ...formData, location: address });
//                 setLiveCoords(null);
//               }}
//               onSelect={handleSelect}
//               searchOptions={{ componentRestrictions: { country: ["in"] } }}
//             >
//               {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
//                 <div className="w-full">
//                   <input
//                     {...getInputProps({
//                       placeholder: "Search Location...",
//                       className: "w-full border px-3 py-2 rounded",
//                     })}
//                   />
//                   <div className="border rounded bg-white mt-1">
//                     {loading && <div className="p-2 text-gray-500">Loading...</div>}
//                     {suggestions.map((suggestion) => {
//                       const className = suggestion.active
//                         ? "p-2 bg-blue-100 cursor-pointer"
//                         : "p-2 cursor-pointer";
//                       return (
//                         <div
//                           {...getSuggestionItemProps(suggestion, { className })}
//                           key={suggestion.placeId}
//                         >
//                           {suggestion.description}
//                         </div>
//                       );
//                     })}
//                   </div>
//                 </div>
//               )}
//             </PlacesAutocomplete>
//             <button
//               type="button"
//               onClick={handleLiveLocation}
//               disabled={isSubmitting}
//               className={`px-4 py-2 rounded text-sm text-white ${
//                 isSubmitting ? "bg-gray-400" : "bg-blue-600"
//               }`}
//             >
//               📍 Live
//             </button>
//           </div>
//           {liveCoords && (
//             <p className="text-xs text-green-600 mt-1">
//               📍 Live Location Captured: {liveCoords.latitude.toFixed(4)}, {liveCoords.longitude.toFixed(4)}
//             </p>
//           )}
//         </div>

//         {/* 📷 Photo Upload */}
//         <div>
//           <label className="block text-sm font-medium text-gray-700 mb-1">
//             Upload / Capture Photo
//           </label>
//           <div className="flex gap-2">
//             <input
//               type="file"
//               accept="image/*"
//               capture="environment"
//               onChange={handlePhotoChange}
//               className="flex-1 border px-3 py-2 rounded"
//             />
//             <button
//               type="button"
//               onClick={startCamera}
//               className="bg-green-600 text-white px-4 py-2 rounded text-sm"
//             >
//               📷 Camera
//             </button>
//           </div>
          
//           {photoPreview && (
//             <div className="mt-2">
//               <img 
//                 src={photoPreview} 
//                 alt="Preview" 
//                 className="w-full h-32 object-cover rounded border"
//               />
//               <button
//                 type="button"
//                 onClick={() => {
//                   setPhoto(null);
//                   setPhotoPreview(null);
//                 }}
//                 className="mt-1 text-red-600 text-sm"
//               >
//                 ❌ Remove Photo
//               </button>
//             </div>
//           )}
          
//           {photo && !photoPreview && (
//             <p className="text-xs text-gray-500 mt-1">Selected: {photo.name}</p>
//           )}
//         </div>

//         <button
//           type="submit"
//           disabled={isSubmitting}
//           className={`w-full ${
//             isSubmitting ? "bg-gray-400" : "bg-green-600"
//           } text-white px-4 py-2 rounded font-semibold`}
//         >
//           {isSubmitting ? "⏳ Submitting..." : "✅ Submit Complaint"}
//         </button>
//       </form>

//       {submitted && (
//         <div className="mt-6 p-4 bg-green-100 rounded-lg">
//           <div className="text-green-700 font-semibold">
//             ✅ Complaint submitted successfully!<br />
//             <span className="text-lg">Your Complaint ID: <span className="font-bold text-green-800">{complaintId}</span></span>
//           </div>
//           <p className="text-sm text-green-600 mt-2">
//             Your complaint is being analyzed and will be forwarded to the appropriate department based on urgency and category.
//           </p>
//         </div>
//       )}

//       {/* Hidden canvas for photo processing */}
//       <canvas ref={canvasRef} style={{ display: 'none' }} />
//     </div>
//   );
// }


import React, { useState, useRef, useCallback, useEffect } from "react";
import axios from "axios";
import PlacesAutocomplete, {
  geocodeByAddress,
  getLatLng,
} from "react-places-autocomplete";

export default function ComplaintForm() {
  const [formData, setFormData] = useState({
    name: "",
    complaint: "",
    location: ""
  });

  const [photo, setPhoto] = useState(null);
  const [photoPreview, setPhotoPreview] = useState(null);
  const [complaintId, setComplaintId] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [liveCoords, setLiveCoords] = useState(null);
  const [recording, setRecording] = useState(false);
  const [cameraStream, setCameraStream] = useState(null);
  const [showCamera, setShowCamera] = useState(false);
  
  // Authentication state
  const [user, setUser] = useState(null);
  const [authToken, setAuthToken] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const recognitionRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Check authentication on component mount
  useEffect(() => {
    checkAuthentication();
  }, []);

  const checkAuthentication = async () => {
    try {
      // Get token from localStorage or sessionStorage
      const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
      
      if (!token) {
        console.warn("No authentication token found");
        return;
      }

      // Verify token and get user profile
      const response = await axios.get('http://localhost:5000/api/user/profile', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.data.success) {
        setUser(response.data.user);
        setAuthToken(token);
        setIsAuthenticated(true);
        
        // Pre-fill form with user data
        setFormData(prev => ({
          ...prev,
          name: response.data.user.name || ""
        }));
        
        console.log("User authenticated:", response.data.user.name);
      }
    } catch (error) {
      console.error("Authentication check failed:", error);
      // Clear invalid token
      localStorage.removeItem('authToken');
      sessionStorage.removeItem('authToken');
      setUser(null);
      setAuthToken(null);
      setIsAuthenticated(false);
    }
  };

  // Get axios config with authentication headers
  const getAxiosConfig = () => {
    const config = {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    };

    if (authToken) {
      config.headers['Authorization'] = `Bearer ${authToken}`;
    }

    return config;
  };

  // 🔤 Transliteration (Hindi → Hinglish)
  const transliterateToHinglish = async (text) => {
    try {
      const res = await fetch(
        `https://inputtools.google.com/request?text=${encodeURIComponent(
          text
        )}&itc=hi-t-i0-und&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=demopage`
      );
      const data = await res.json();
      if (data[0] === "SUCCESS") {
        return data[1][0][1][0];
      }
      return text;
    } catch (err) {
      console.error("Transliteration API error:", err);
      return text;
    }
  };

  // 🌍 Reverse Geocoding - Convert coordinates to address
  const reverseGeocode = async (latitude, longitude) => {
    try {
      const response = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=AIzaSyA9spKFBlhfECHHoXnMPRziyuUuhL124yo`
      );
      const data = await response.json();
      
      if (data.results && data.results.length > 0) {
        return data.results[0].formatted_address;
      }
      return `Location: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
    } catch (error) {
      console.error("Reverse geocoding error:", error);
      return `Location: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
    }
  };

  // 🎙️ Speech-to-text
  const handleSpeechToText = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser. Please use Chrome.");
      return;
    }

    if (recording) {
      recognitionRef.current?.stop();
      setRecording(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "hi-IN";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = async (event) => {
      let transcript = "";
      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript + " ";
      }
      const hinglish = await transliterateToHinglish(transcript.trim());
      setFormData((prev) => ({ ...prev, complaint: hinglish }));
    };

    recognition.onerror = (err) => {
      console.error("Speech Recognition Error:", err);
      setRecording(false);
    };

    recognition.onend = () => {
      setRecording(false);
    };

    recognition.start();
    recognitionRef.current = recognition;
    setRecording(true);
  };

  // 📷 Camera Functions
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }, // Use back camera
        audio: false
      });
      
      setCameraStream(stream);
      setShowCamera(true);
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error("Camera access error:", error);
      alert("Unable to access camera. Please check permissions.");
    }
  };

  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
      setCameraStream(null);
    }
    setShowCamera(false);
  };

  const capturePhoto = useCallback(async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current video frame to canvas
    context.drawImage(video, 0, 0);

    // Get current location for geo-tagging
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          
          // Add geo-tag overlay to image
          context.fillStyle = 'rgba(0, 0, 0, 0.7)';
          context.fillRect(0, canvas.height - 60, canvas.width, 60);
          context.fillStyle = 'white';
          context.font = '14px Arial';
          context.fillText(`Location: ${latitude.toFixed(6)}, ${longitude.toFixed(6)}`, 10, canvas.height - 35);
          context.fillText(`Captured: ${new Date().toLocaleString()}`, 10, canvas.height - 15);

          // Convert to blob
          canvas.toBlob((blob) => {
            const file = new File([blob], `complaint_photo_${Date.now()}.jpg`, {
              type: 'image/jpeg'
            });
            
            setPhoto(file);
            setPhotoPreview(canvas.toDataURL());
            stopCamera();
          }, 'image/jpeg', 0.8);
        },
        (error) => {
          console.warn("Location not available for geo-tagging:", error);
          // Capture without geo-tag
          canvas.toBlob((blob) => {
            const file = new File([blob], `complaint_photo_${Date.now()}.jpg`, {
              type: 'image/jpeg'
            });
            
            setPhoto(file);
            setPhotoPreview(canvas.toDataURL());
            stopCamera();
          }, 'image/jpeg', 0.8);
        },
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
      );
    }
  }, [cameraStream]);

  const handlePhotoChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setPhoto(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => setPhotoPreview(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  const handleSelect = async (address) => {
    setFormData({ ...formData, location: address });
    setLiveCoords(null);
    try {
      const results = await geocodeByAddress(address);
      await getLatLng(results[0]);
    } catch (error) {
      console.error("Error fetching coordinates", error);
    }
  };

  const handleLiveLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    setIsSubmitting(true);
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        setLiveCoords({ latitude, longitude });
        
        // Get human-readable address
        const address = await reverseGeocode(latitude, longitude);
        setFormData({ ...formData, location: address });
        
        // alert("Live location successfully captured!");
        setIsSubmitting(false);
      },
      (error) => {
        console.warn("Geolocation error:", error);
        alert("⚠ Location not available. Please enable GPS.");
        setLiveCoords(null);
        setIsSubmitting(false);
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.complaint.trim()) {
      alert("Please speak or type your complaint.");
      return;
    }

    // Check authentication before submission
    if (!isAuthenticated) {
      alert("Please log in to submit a complaint. This ensures proper tracking and follow-up.");
      return;
    }

    setIsSubmitting(true);
    try {
      const formDataToSend = new FormData();
      formDataToSend.append("complaint", formData.complaint);
      formDataToSend.append("location", formData.location);
      
      // Use authenticated user's name, not form input
      if (user && user.name) {
        formDataToSend.append("name", user.name);
      }

      if (photo) {
        formDataToSend.append("photo", photo);
      }

      if (liveCoords) {
        formDataToSend.append("latitude", liveCoords.latitude);
        formDataToSend.append("longitude", liveCoords.longitude);
      }

      // Add metadata
      formDataToSend.append("timestamp", new Date().toISOString());
      formDataToSend.append("hasPhoto", !!photo);
      formDataToSend.append("hasGeoLocation", !!liveCoords);
      formDataToSend.append("dashboardSource", "enhanced-complaint-form");
      formDataToSend.append("submissionType", "authenticated-form-with-nlp");
      formDataToSend.append("userAgent", navigator.userAgent);
      formDataToSend.append("platform", navigator.platform);

      // Make authenticated request
      const config = getAxiosConfig();
      const res = await axios.post("http://localhost:5000/api/complaint", formDataToSend, config);

      // Handle backend response
      const complaintData = res.data.complaint || res.data;
      const complaintId = complaintData.complaintId || res.data.complaintId;
      setComplaintId(complaintId);
      setSubmitted(true);

      // Reset form
      setFormData({
        name: user?.name || "",
        complaint: "",
        location: ""
      });
      setPhoto(null);
      setPhotoPreview(null);
      setLiveCoords(null);

      // Show success message with user info
      alert(`Complaint submitted successfully!\n\nComplaint ID: ${complaintId}\nSubmitted by: ${user.name}\nDepartment: ${complaintData.department || 'General'}\nUrgency: ${complaintData.urgency || 'Medium'}`);

    } catch (err) {
      console.error("Submission failed:", err);
      
      // Handle specific error cases
      if (err.response?.status === 401) {
        alert("Authentication expired. Please log in again.");
        setIsAuthenticated(false);
        setUser(null);
        setAuthToken(null);
      } else {
        alert("Complaint submission failed. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-semibold mb-4">Complaint Form</h2>
      
      {/* Authentication Status */}
      {isAuthenticated ? (
        <div className="mb-4 p-3 bg-green-100 rounded-lg">
          <p className="text-green-800">
            <span className="font-semibold">Logged in as:</span> {user?.name} ({user?.email})
          </p>
          <p className="text-sm text-green-600">
            Your complaints will be properly tracked and you'll receive updates.
          </p>
        </div>
      ) : (
        <div className="mb-4 p-3 bg-yellow-100 rounded-lg">
          <p className="text-yellow-800 font-semibold">
            Please log in to submit complaints
          </p>
          <p className="text-sm text-yellow-600">
            Authentication ensures proper complaint tracking and follow-up communication.
          </p>
        </div>
      )}
      
      {/* Camera Modal */}
      {showCamera && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white p-4 rounded-lg max-w-md w-full">
            <div className="relative">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-full h-64 object-cover rounded"
              />
              <div className="flex justify-center space-x-4 mt-4">
                <button
                  onClick={capturePhoto}
                  className="bg-blue-600 text-white px-4 py-2 rounded"
                >
                  📷 Capture
                </button>
                <button
                  onClick={stopCamera}
                  className="bg-gray-600 text-white px-4 py-2 rounded"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        
        {/* User Name (Read-only for authenticated users)
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Name
          </label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="Your name"
            readOnly={isAuthenticated}
            className={`w-full border px-3 py-2 rounded ${
              isAuthenticated ? 'bg-gray-100 cursor-not-allowed' : ''
            }`}
          />
          {isAuthenticated && (
            <p className="text-xs text-gray-500 mt-1">
              Name auto-filled from your account
            </p>
          )}
        </div> */}
        
        {/* 🎙️ Voice-to-Text */}
        <button
          type="button"
          onClick={handleSpeechToText}
          disabled={!isAuthenticated}
          className={`w-full px-4 py-2 rounded-lg font-semibold ${
            !isAuthenticated 
              ? "bg-gray-400 cursor-not-allowed" 
              : recording 
                ? "bg-red-500" 
                : "bg-purple-600"
          } text-white`}
        >
          {!isAuthenticated 
            ? "🔒 Login Required for Voice Input"
            : recording 
              ? "🛑 बोलना रोकें" 
              : "🎤 शिकायत बोलें"
          }
        </button>

        {/* Complaint Text */}
        <textarea
          name="complaint"
          value={formData.complaint}
          onChange={(e) => setFormData({ ...formData, complaint: e.target.value })}
          placeholder="Describe your complaint or speak..."
          required
          disabled={!isAuthenticated}
          className={`w-full border px-3 py-2 rounded h-32 ${
            !isAuthenticated ? 'bg-gray-100 cursor-not-allowed' : ''
          }`}
        />

        {/* 📍 Location */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Location
          </label>
          <div className="flex gap-2">
            <PlacesAutocomplete
              value={formData.location}
              onChange={(address) => {
                setFormData({ ...formData, location: address });
                setLiveCoords(null);
              }}
              onSelect={handleSelect}
              searchOptions={{ componentRestrictions: { country: ["in"] } }}
            >
              {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
                <div className="w-full">
                  <input
                    {...getInputProps({
                      placeholder: "Search Location...",
                      className: `w-full border px-3 py-2 rounded ${
                        !isAuthenticated ? 'bg-gray-100 cursor-not-allowed' : ''
                      }`,
                      disabled: !isAuthenticated
                    })}
                  />
                  {isAuthenticated && (
                    <div className="border rounded bg-white mt-1">
                      {loading && <div className="p-2 text-gray-500">Loading...</div>}
                      {suggestions.map((suggestion) => {
                        const className = suggestion.active
                          ? "p-2 bg-blue-100 cursor-pointer"
                          : "p-2 cursor-pointer";
                        return (
                          <div
                            {...getSuggestionItemProps(suggestion, { className })}
                            key={suggestion.placeId}
                          >
                            {suggestion.description}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              )}
            </PlacesAutocomplete>
            <button
              type="button"
              onClick={handleLiveLocation}
              disabled={isSubmitting || !isAuthenticated}
              className={`px-4 py-2 rounded text-sm text-white ${
                !isAuthenticated || isSubmitting ? "bg-gray-400" : "bg-blue-600"
              }`}
            >
              📍 Live
            </button>
          </div>
          {liveCoords && (
            <p className="text-xs text-green-600 mt-1">
              📍 Live Location Captured: {liveCoords.latitude.toFixed(4)}, {liveCoords.longitude.toFixed(4)}
            </p>
          )}
        </div>

        {/* 📷 Photo Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Upload / Capture Photo
          </label>
          <div className="flex gap-2">
            <input
              type="file"
              accept="image/*"
              capture="environment"
              onChange={handlePhotoChange}
              disabled={!isAuthenticated}
              className={`flex-1 border px-3 py-2 rounded ${
                !isAuthenticated ? 'bg-gray-100 cursor-not-allowed' : ''
              }`}
            />
            <button
              type="button"
              onClick={startCamera}
              disabled={!isAuthenticated}
              className={`px-4 py-2 rounded text-sm text-white ${
                !isAuthenticated ? "bg-gray-400" : "bg-green-600"
              }`}
            >
              📷 Camera
            </button>
          </div>
          
          {photoPreview && (
            <div className="mt-2">
              <img 
                src={photoPreview} 
                alt="Preview" 
                className="w-full h-32 object-cover rounded border"
              />
              <button
                type="button"
                onClick={() => {
                  setPhoto(null);
                  setPhotoPreview(null);
                }}
                className="mt-1 text-red-600 text-sm"
              >
                ❌ Remove Photo
              </button>
            </div>
          )}
          
          {photo && !photoPreview && (
            <p className="text-xs text-gray-500 mt-1">Selected: {photo.name}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={isSubmitting || !isAuthenticated}
          className={`w-full ${
            !isAuthenticated || isSubmitting ? "bg-gray-400" : "bg-green-600"
          } text-white px-4 py-2 rounded font-semibold`}
        >
          {!isAuthenticated 
            ? "🔒 Please Login to Submit" 
            : isSubmitting 
              ? "⏳ Submitting..." 
              : "✅ Submit Complaint"
          }
        </button>
      </form>

      {submitted && (
        <div className="mt-6 p-4 bg-green-100 rounded-lg">
          <div className="text-green-700 font-semibold">
            ✅ Complaint submitted successfully!<br />
            <span className="text-lg">Your Complaint ID: <span className="font-bold text-green-800">{complaintId}</span></span>
          </div>
          {user && (
            <p className="text-sm text-green-600 mt-2">
              Submitted by: <strong>{user.name}</strong> ({user.email})<br />
              Your complaint is being analyzed and will be forwarded to the appropriate department based on urgency and category.
            </p>
          )}
        </div>
      )}

      {/* Hidden canvas for photo processing */}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
}