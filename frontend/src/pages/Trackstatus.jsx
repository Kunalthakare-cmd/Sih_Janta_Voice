//  import React, { useState } from "react";
// import axios from "axios";

// export default function TrackStatus() {
//   const [complaintId, setComplaintId] = useState("");
//   const [result, setResult] = useState(null);
//   const [error, setError] = useState("");

//   const handleTrack = async () => {
//     if (!complaintId.trim()) return;

//     try {
//       const res = await axios.get(`http://localhost:5000/api/complaint/${complaintId.trim()}`);

//       if (res.data.success) {
//         setResult(res.data);
//         setError("");
//       } else {
//         setResult(null);
//         setError("शिकायत नहीं मिली। कृपया सही Complaint ID दर्ज करें।");
//       }
//     } catch (err) {
//       setResult(null);
//       setError("सर्वर से कनेक्ट नहीं हो सका या शिकायत नहीं मिली।");
//     }
//   };

//   return (
//     <div className="m-2 p-10 flex justify-center items-start min-h-screen bg-gray-100">
//       <div className="bg-white border border-blue-300 shadow-2xl rounded-2xl p-8 w-96 mt-20">

//         {/* Gradient Header */}
//         <h2 className="text-2xl font-bold mb-6 text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-blue-400">
//           शिकायत की स्थिति ट्रैक करें
//         </h2>

//         {/* Input */}
//         <input
//           type="text"
//           placeholder="Complaint ID दर्ज करें"
//           className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
//           value={complaintId}
//           onChange={(e) => setComplaintId(e.target.value)}
//         />

//         {/* Orange Gradient Button */}
//         <button
//           onClick={handleTrack}
//           className="w-full bg-gradient-to-r from-orange-500 to-orange-400 text-white py-2 rounded-lg shadow-md hover:from-orange-600 hover:to-orange-500 transition-all"
//         >
//           ट्रैक करें
//         </button>

//         {/* Error */}
//         {error && <p className="text-red-500 mt-4 text-center">{error}</p>}

//         {/* Result */}
//         {result && (
//           <div className="mt-6 border-t pt-4 text-sm space-y-2">
//             <p><strong>स्थिति:</strong> {result.status}</p>
//             <p><strong>शिकायतकर्ता:</strong> {result.name}</p>
//             <p><strong>स्थान:</strong> {result.location}</p>
//             <p><strong>विभाग:</strong> {result.department}</p>
//             <p><strong>विवरण:</strong> {result.description}</p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }


import React, { useState } from "react";
import { Search, CheckCircle, Clock, AlertCircle, MapPin, Building, FileText, User } from "lucide-react";

export default function TrackStatus() {
  const [complaintId, setComplaintId] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleTrack = async () => {
    if (!complaintId.trim()) return;
    
    setIsLoading(true);
    try {
      // Replace axios with fetch for demo purposes
      const res = await fetch(`http://localhost:5000/api/complaint/${complaintId.trim()}`);
      const data = await res.json();

      if (data.success) {
        setResult(data);
        setError("");
      } else {
        setResult(null);
        setError("शिकायत नहीं मिली। कृपया सही Complaint ID दर्ज करें।");
      }
    } catch (err) {
      setResult(null);
      setError("सर्वर से कनेक्ट नहीं हो सका या शिकायत नहीं मिली।");
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const statusLower = status?.toLowerCase() || '';
    if (statusLower.includes('पूर्ण') || statusLower.includes('complete') || statusLower.includes('resolved')) {
      return 'text-green-600 bg-green-50 border-green-200';
    } else if (statusLower.includes('प्रगति') || statusLower.includes('progress') || statusLower.includes('pending')) {
      return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    }
    return 'text-blue-600 bg-blue-50 border-blue-200';
  };

  const getStatusIcon = (status) => {
    const statusLower = status?.toLowerCase() || '';
    if (statusLower.includes('पूर्ण') || statusLower.includes('complete') || statusLower.includes('resolved')) {
      return <CheckCircle className="w-5 h-5 text-green-600" />;
    } else if (statusLower.includes('प्रगति') || statusLower.includes('progress') || statusLower.includes('pending')) {
      return <Clock className="w-5 h-5 text-yellow-600" />;
    }
    return <AlertCircle className="w-5 h-5 text-blue-600" />;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex justify-center items-start p-4">
      <div className="w-full max-w-md mt-16">
        {/* Main Card */}
        <div className="bg-white/80 backdrop-blur-sm border border-white/20 shadow-xl rounded-3xl p-8 mb-6">
          {/* Header with Icon */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl mb-4 shadow-lg">
              <Search className="w-8 h-8 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 mb-2">
              शिकायत की स्थिति ट्रैक करें
            </h2>
            <p className="text-gray-600 text-sm">
              अपनी शिकायत की वर्तमान स्थिति जानने के लिए ID दर्ज करें
            </p>
          </div>

          {/* Input Field */}
          <div className="relative mb-6">
            <input
              type="text"
              placeholder="Complaint ID दर्ज करें"
              className="w-full px-4 py-4 bg-gray-50 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 focus:bg-white transition-all duration-300 text-center font-mono tracking-wider"
              value={complaintId}
              onChange={(e) => setComplaintId(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleTrack()}
            />
          </div>

          {/* Track Button */}
          <button
            onClick={handleTrack}
            disabled={isLoading || !complaintId.trim()}
            className="w-full bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 disabled:from-gray-300 disabled:to-gray-400 text-white py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-300 disabled:transform-none disabled:hover:scale-100 flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                ट्रैक कर रहे हैं...
              </>
            ) : (
              <>
                <Search className="w-5 h-5" />
                ट्रैक करें
              </>
            )}
          </button>

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl">
              <div className="flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            </div>
          )}
        </div>

        {/* Result Card */}
        {result && (
          <div className="bg-white/80 backdrop-blur-sm border border-white/20 shadow-xl rounded-3xl p-8 animate-fadeIn">
            {/* Status Header */}
            <div className="text-center mb-6">
              <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border-2 ${getStatusColor(result.status)}`}>
                {getStatusIcon(result.status)}
                <span className="font-semibold">{result.status}</span>
              </div>
            </div>

            {/* Details */}
            <div className="space-y-4">
              {/* <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-xl">
                <User className="w-5 h-5 text-gray-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm text-gray-600 mb-1">शिकायतकर्ता</p>
                  <p className="font-semibold text-gray-900">{result.name}</p>
                </div>
              </div> */}

              <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-xl">
                <MapPin className="w-5 h-5 text-gray-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm text-gray-600 mb-1">स्थान</p>
                  <p className="font-semibold text-gray-900">{result.location}</p>
                </div>
              </div>

              <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-xl">
                <Building className="w-5 h-5 text-gray-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm text-gray-600 mb-1">विभाग</p>
                  <p className="font-semibold text-gray-900">{result.department}</p>
                </div>
              </div>

              <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-xl">
                <FileText className="w-5 h-5 text-gray-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm text-gray-600 mb-1">विवरण</p>
                  <p className="font-semibold text-gray-900 leading-relaxed">{result.description}</p>
                </div>
              </div>
            </div>

            {/* Success Footer */}
            <div className="mt-6 pt-6 border-t border-gray-200 text-center">
              <p className="text-sm text-gray-600">
                शिकायत सफलतापूर्वक ट्रैक की गई
              </p>
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out;
        }
      `}</style>
    </div>
  );
}