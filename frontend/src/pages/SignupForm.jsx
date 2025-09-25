// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import axios from "axios";

// export default function SignupForm() {
//   const navigate = useNavigate();
//   const [form, setForm] = useState({
//     name: "",
//     email: "",
//     password: "",
//     phone: "",
//     address: "",
//   });
//   const [photo, setPhoto] = useState(null);

//   const handleChange = (e) => {
//     setForm({ ...form, [e.target.name]: e.target.value });
//   };

//   const handlePhotoChange = (e) => {
//     if (e.target.files && e.target.files[0]) {
//       setPhoto(e.target.files[0]);
//     }
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       const formData = new FormData();
//       Object.keys(form).forEach((key) => formData.append(key, form[key]));
//       if (photo) formData.append("photo", photo);

//       await axios.post("http://localhost:5000/api/auth/register", formData, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });

//       alert("Signup successful! Please login now.");
//       setForm({ name: "", email: "", password: "", phone: "", address: "" });
//       setPhoto(null);
//       navigate("/login"); // redirect to login page after signup
//     } catch (err) {
//       alert(err.response?.data?.error || "Signup failed");
//     }
//   };

//   return (
//     <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
//       <h2 className="text-2xl font-semibold mb-4">Signup</h2>
//       <form onSubmit={handleSubmit} className="space-y-4">
//         <input name="name" value={form.name} onChange={handleChange} placeholder="Full Name" required className="w-full border px-3 py-2 rounded" />
//         <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="Email" required className="w-full border px-3 py-2 rounded" />
//         <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="Password" required className="w-full border px-3 py-2 rounded" />
//         <input name="phone" value={form.phone} onChange={handleChange} placeholder="Phone Number" required className="w-full border px-3 py-2 rounded" />
//         <textarea name="address" value={form.address} onChange={handleChange} placeholder="Full Address" required className="w-full border px-3 py-2 rounded" />
//         <input type="file" accept="image/*" onChange={handlePhotoChange} className="w-full border px-3 py-2 rounded" />
//         <button type="submit" className="w-full bg-blue-600 text-white px-4 py-2 rounded">Signup</button>
//       </form>

//       <p className="mt-4 text-center text-gray-600">
//         Already have an account?{" "}
//         <span
//           onClick={() => navigate("/login")}
//           className="text-blue-600 underline cursor-pointer"
//         >
//           Login here
//         </span>
//       </p>
//     </div>
//   );
// }



import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import PlacesAutocomplete, {
  geocodeByAddress,
  getLatLng,
} from "react-places-autocomplete";

export default function SignupForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    phone: "",
    address: "",
    latitude: "",
    longitude: "",
  });
  const [photo, setPhoto] = useState(null);
  const [liveCoords, setLiveCoords] = useState(null);
  const [isGettingLocation, setIsGettingLocation] = useState(false);

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

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handlePhotoChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setPhoto(e.target.files[0]);
    }
  };

  // Handle Places Autocomplete selection
  const handleSelect = async (address) => {
    setForm({ ...form, address });
    setLiveCoords(null);
    
    try {
      const results = await geocodeByAddress(address);
      const { lat, lng } = await getLatLng(results[0]);
      
      // Update form with coordinates
      setForm(prev => ({
        ...prev,
        address,
        latitude: lat.toString(),
        longitude: lng.toString()
      }));
    } catch (error) {
      console.error("Error fetching coordinates", error);
    }
  };

  // Get live location
  const handleLiveLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    setIsGettingLocation(true);
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        setLiveCoords({ latitude, longitude });
        
        // Get human-readable address
        const address = await reverseGeocode(latitude, longitude);
        
        // Update form with location data
        setForm(prev => ({
          ...prev,
          address,
          latitude: latitude.toString(),
          longitude: longitude.toString()
        }));
        
        setIsGettingLocation(false);
      },
      (error) => {
        console.warn("Geolocation error:", error);
        alert("⚠ Location not available. Please enable GPS and try again.");
        setLiveCoords(null);
        setIsGettingLocation(false);
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      Object.keys(form).forEach((key) => formData.append(key, form[key]));
      if (photo) formData.append("photo", photo);

      // Add location metadata
      if (liveCoords) {
        formData.append("hasLiveLocation", "true");
        formData.append("locationMethod", "gps");
      } else if (form.latitude && form.longitude) {
        formData.append("hasLiveLocation", "false");
        formData.append("locationMethod", "places_autocomplete");
      }

      await axios.post("http://localhost:5000/api/auth/register", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("Signup successful! Please login now.");
      setForm({ 
        name: "", 
        email: "", 
        password: "", 
        phone: "", 
        address: "",
        latitude: "",
        longitude: ""
      });
      setPhoto(null);
      setLiveCoords(null);
      navigate("/login");
    } catch (err) {
      alert(err.response?.data?.error || "Signup failed");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-semibold mb-4">Signup</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input 
          name="name" 
          value={form.name} 
          onChange={handleChange} 
          placeholder="Full Name" 
          required 
          className="w-full border px-3 py-2 rounded" 
        />
        
        <input 
          type="email" 
          name="email" 
          value={form.email} 
          onChange={handleChange} 
          placeholder="Email" 
          required 
          className="w-full border px-3 py-2 rounded" 
        />
        
        <input 
          type="password" 
          name="password" 
          value={form.password} 
          onChange={handleChange} 
          placeholder="Password" 
          required 
          className="w-full border px-3 py-2 rounded" 
        />
        
        <input 
          name="phone" 
          value={form.phone} 
          onChange={handleChange} 
          placeholder="Phone Number" 
          required 
          className="w-full border px-3 py-2 rounded" 
        />

        {/* 📍 Enhanced Address with Location */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Address
          </label>
          <div className="flex gap-2">
            <PlacesAutocomplete
              value={form.address}
              onChange={(address) => {
                setForm({ ...form, address });
                setLiveCoords(null);
              }}
              onSelect={handleSelect}
              searchOptions={{ componentRestrictions: { country: ["in"] } }}
            >
              {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
                <div className="w-full">
                  <input
                    {...getInputProps({
                      placeholder: "Search Address...",
                      className: "w-full border px-3 py-2 rounded",
                      required: true
                    })}
                  />
                  <div className="border rounded bg-white mt-1">
                    {loading && <div className="p-2 text-gray-500">Loading...</div>}
                    {suggestions.map((suggestion) => {
                      const className = suggestion.active
                        ? "p-2 bg-blue-100 cursor-pointer"
                        : "p-2 cursor-pointer hover:bg-gray-50";
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
                </div>
              )}
            </PlacesAutocomplete>
            
            <button
              type="button"
              onClick={handleLiveLocation}
              disabled={isGettingLocation}
              className={`px-4 py-2 rounded text-sm text-white whitespace-nowrap ${
                isGettingLocation ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              {isGettingLocation ? "📍 Getting..." : "📍 Live"}
            </button>
          </div>
          
          {liveCoords && (
            <p className="text-xs text-green-600 mt-1">
              📍 Live Location Captured: {liveCoords.latitude.toFixed(4)}, {liveCoords.longitude.toFixed(4)}
            </p>
          )}
          
          {form.latitude && form.longitude && (
            <p className="text-xs text-gray-500 mt-1">
              Coordinates: {parseFloat(form.latitude).toFixed(6)}, {parseFloat(form.longitude).toFixed(6)}
            </p>
          )}
        </div>

        {/* Hidden coordinate inputs for form submission */}
        <input 
          type="hidden" 
          name="latitude" 
          value={form.latitude} 
        />
        <input 
          type="hidden" 
          name="longitude" 
          value={form.longitude} 
        />

        <input 
          type="file" 
          accept="image/*" 
          onChange={handlePhotoChange} 
          className="w-full border px-3 py-2 rounded" 
        />
        
        <button 
          type="submit" 
          className="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Signup
        </button>
      </form>

      <p className="mt-4 text-center text-gray-600">
        Already have an account?{" "}
        <span
          onClick={() => navigate("/login")}
          className="text-blue-600 underline cursor-pointer hover:text-blue-800"
        >
          Login here
        </span>
      </p>
    </div>
  );
}
