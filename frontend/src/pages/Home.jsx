import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronRight, Mic, Zap, BarChart3, Shield, Users, CheckCircle, ArrowRight, Play, Star, Heart, Award } from 'lucide-react';

const Home = () => {
  const navigate = useNavigate();
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const FloatingElements = () => (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Soft Mesh Gradient Background */}
      <div className="absolute inset-0 "></div>

      {/* Animated Orbs with softer movements and colors */}
      <div
        className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-r from-blue-300/20 to-purple-300/20 rounded-full blur-3xl animate-gentle-float animate-morph"
        style={{ transform: `translate(${scrollY * 0.1}px, ${scrollY * 0.05}px)` }}
      />
      <div
        className="absolute top-3/4 right-1/4 w-80 h-80 bg-gradient-to-r from-green-300/20 to-blue-300/20 rounded-full blur-3xl animate-gentle-float animate-morph"
        style={{ transform: `translate(${scrollY * -0.1}px, ${scrollY * 0.08}px)`, animationDelay: '2s' }}
      />
      <div
        className="absolute top-1/2 left-3/4 w-64 h-64 bg-gradient-to-r from-purple-300/20 to-pink-300/20 rounded-full blur-2xl animate-gentle-float animate-morph"
        style={{ transform: `translate(${scrollY * 0.15}px, ${scrollY * -0.1}px)`, animationDelay: '1s' }}
      />

      {/* Minimalist Grid Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="grid grid-cols-20 gap-8 h-full w-full">
          {[...Array(200)].map((_, i) => (
            <div
              key={i}
              className="w-1 h-1 bg-gray-400 rounded-full animate-grid-sparkle"
              style={{ animationDelay: `${Math.random() * 3}s` }}
            />
          ))}
        </div>
      </div>

      {/* Softer, Dynamic Particles */}
      {[...Array(15)].map((_, i) => (
        <div
          key={i}
          className="absolute animate-particle-float"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${4 + Math.random() * 3}s`,
          }}
        >
          <div className={`w-${Math.random() > 0.5 ? '2' : '3'} h-${Math.random() > 0.5 ? '2' : '3'} bg-gradient-to-r ${['from-blue-200 to-purple-200', 'from-green-200 to-blue-200', 'from-purple-200 to-pink-200'][Math.floor(Math.random() * 3)]
            } rounded-full opacity-60 animate-particle-glow`} />
        </div>
      ))}

    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 via-blue-50 to-purple-50 relative overflow-hidden">
      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg) scale(1); opacity: 0.7; }
          25% { transform: translateY(-15px) rotate(90deg) scale(1.1); opacity: 0.9; }
          50% { transform: translateY(-25px) rotate(180deg) scale(1.2); opacity: 1; }
          75% { transform: translateY(-15px) rotate(270deg) scale(1.1); opacity: 0.9; }
        }
        @keyframes glow {
          0%, 100% { box-shadow: 0 0 25px rgba(59, 130, 246, 0.4), 0 0 50px rgba(59, 130, 246, 0.2); }
          50% { box-shadow: 0 0 35px rgba(59, 130, 246, 0.6), 0 0 70px rgba(59, 130, 246, 0.3); }
        }
        @keyframes slideInUp {
          from { opacity: 0; transform: translateY(60px) scale(0.95); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes fadeInScale {
          from { opacity: 0; transform: scale(0.8) rotate(-5deg); }
          to { opacity: 1; transform: scale(1) rotate(0deg); }
        }
        @keyframes shimmer {
          0% { background-position: -200px 0; }
          100% { background-position: 200px 0; }
        }
        @keyframes morphing {
          0%, 100% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
          50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
        }
        
        /* Enhanced Premium Animations */
        @keyframes floating-orb {
          0%, 100% { transform: translateY(0px) translateX(0px) scale(1) rotate(0deg); }
          25% { transform: translateY(-20px) translateX(15px) scale(1.1) rotate(90deg); }
          50% { transform: translateY(-40px) translateX(0px) scale(1.2) rotate(180deg); }
          75% { transform: translateY(-20px) translateX(-15px) scale(1.1) rotate(270deg); }
        }
        
        @keyframes floating-orb-reverse {
          0%, 100% { transform: translateY(0px) translateX(0px) scale(1) rotate(360deg); }
          25% { transform: translateY(20px) translateX(-15px) scale(1.1) rotate(270deg); }
          50% { transform: translateY(40px) translateX(0px) scale(1.2) rotate(180deg); }
          75% { transform: translateY(20px) translateX(15px) scale(1.1) rotate(90deg); }
        }
        
        @keyframes particle-float {
          0%, 100% { transform: translateY(0px) translateX(0px) rotate(0deg) scale(1); opacity: 0.4; }
          25% { transform: translateY(-30px) translateX(20px) rotate(90deg) scale(1.2); opacity: 0.8; }
          50% { transform: translateY(-60px) translateX(0px) rotate(180deg) scale(1.4); opacity: 1; }
          75% { transform: translateY(-30px) translateX(-20px) rotate(270deg) scale(1.2); opacity: 0.8; }
        }
        
        @keyframes particle-glow {
          0%, 100% { filter: brightness(1) blur(0px); }
          50% { filter: brightness(1.5) blur(1px); }
        }
        
        @keyframes grid-sparkle {
          0%, 80%, 100% { opacity: 0.1; transform: scale(1); }
          40% { opacity: 0.8; transform: scale(1.5); }
        }
        
        @keyframes line-draw {
          0% { stroke-dasharray: 0 100; opacity: 0; }
          50% { stroke-dasharray: 50 100; opacity: 0.3; }
          100% { stroke-dasharray: 100 100; opacity: 0.1; }
        }
        
        @keyframes pulse-slow {
          0%, 100% { opacity: 0.8; }
          50% { opacity: 1; }
        }
        
        @keyframes text-glow {
          0%, 100% { text-shadow: 0 0 20px rgba(59, 130, 246, 0.5); }
          50% { text-shadow: 0 0 30px rgba(59, 130, 246, 0.8), 0 0 40px rgba(139, 69, 19, 0.3); }
        }
        
        @keyframes button-breathe {
          0%, 100% { transform: scale(1) rotate(0deg); box-shadow: 0 0 25px rgba(59, 130, 246, 0.4); }
          50% { transform: scale(1.02) rotate(1deg); box-shadow: 0 0 35px rgba(59, 130, 246, 0.6); }
        }
        
        @keyframes card-hover-glow {
          0%, 100% { box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); }
          50% { box-shadow: 0 12px 40px rgba(59, 130, 246, 0.2), 0 0 30px rgba(59, 130, 246, 0.1); }
        }
        
        @keyframes icon-dance {
          0%, 100% { transform: translateY(0) rotate(0deg); }
          25% { transform: translateY(-5px) rotate(5deg); }
          75% { transform: translateY(5px) rotate(-5deg); }
        }
        
        @keyframes progress-flow {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(300%); }
        }
        
        @keyframes wave-motion {
          0%, 100% { d: path("M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z"); }
          50% { d: path("M0,0V56.29c57.79,32.2,113.59,42.17,168,38,80.36-15.37,146.33-43.31,216.8-47.5C448.64,42.43,522.34,63.67,593,82.05c79.27,28,148.3,34.88,219.4,23.08,46.15-16,79.85-27.84,114.45-39.34C999.49,35,1123-4.29,1200,62.47V0Z"); }
        }
        
        @keyframes gradient-flow {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        
        @keyframes gentle-float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-15px); }
        }
        
        @keyframes soft-glow {
          0%, 100% { box-shadow: 0 5px 25px rgba(59, 130, 246, 0.2); }
          50% { box-shadow: 0 8px 35px rgba(59, 130, 246, 0.35); }
        }
        
        @keyframes shimmer-light {
          0% { background-position: -200px 0; }
          100% { background-position: 200px 0; }
        }
        
        @keyframes pulse-soft {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.05); opacity: 0.9; }
        }
        
        .animate-float { animation: float 5s ease-in-out infinite; }
        .animate-glow { animation: glow 3s ease-in-out infinite; }
        .animate-slide-up { animation: slideInUp 1s ease-out forwards; }
        .animate-fade-scale { animation: fadeInScale 0.8s ease-out forwards; }
        .animate-shimmer { 
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
          background-size: 200px 100%;
          animation: shimmer 2s infinite;
        }
        .animate-morph { animation: morphing 6s ease-in-out infinite; }
        
        /* New Enhanced Animations */
        .animate-floating-orb { animation: floating-orb 8s ease-in-out infinite; }
        .animate-floating-orb-reverse { animation: floating-orb-reverse 10s ease-in-out infinite; }
        .animate-particle-float { animation: particle-float 6s ease-in-out infinite; }
        .animate-particle-glow { animation: particle-glow 3s ease-in-out infinite; }
        .animate-grid-sparkle { animation: grid-sparkle 4s ease-in-out infinite; }
        .animate-line-draw { animation: line-draw 3s ease-in-out infinite; }
        .animate-pulse-slow { animation: pulse-slow 4s ease-in-out infinite; }
        .animate-text-glow { animation: text-glow 3s ease-in-out infinite; }
        .animate-button-breathe { animation: button-breathe 3s ease-in-out infinite; }
        .animate-card-hover-glow { animation: card-hover-glow 3s ease-in-out infinite; }
        .animate-icon-dance { animation: icon-dance 2s ease-in-out infinite; }
        .animate-progress-flow { animation: progress-flow 2s ease-in-out infinite; }
        .animate-wave-motion { animation: wave-motion 4s ease-in-out infinite; }
        .animate-gentle-float { animation: gentle-float 6s ease-in-out infinite; }
        .animate-soft-glow { animation: soft-glow 3s ease-in-out infinite; }
        .animate-pulse-soft { animation: pulse-soft 4s ease-in-out infinite; }

        .glass-effect {
          background: rgba(255, 255, 255, 0.9);
          backdrop-filter: blur(20px);
          border: 1px solid rgba(255, 255, 255, 0.5);
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .glass-effect-strong {
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(25px);
          border: 1px solid rgba(255, 255, 255, 0.4);
          box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }
        .gradient-text {
          background: linear-gradient(135deg, #2563eb, #059669, #7c3aed, #dc2626);
          background-size: 400% 400%;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          animation: gradient-flow 8s ease infinite;
        }
        
        /* Hover Enhanced Effects */
        .hover-lift:hover {
          transform: translateY(-8px) scale(1.02);
          transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        .hover-glow:hover {
          box-shadow: 0 0 40px rgba(59, 130, 246, 0.4), 0 0 80px rgba(59, 130, 246, 0.2);
          transition: all 0.4s ease;
        }
        
        .hover-rotate:hover {
          transform: rotate(2deg) scale(1.05);
          transition: all 0.3s ease;
        }
      `}</style>

      <FloatingElements />





      {/* Hero Section */}
      <div className="relative z-10 px-2 pt-20 pb-20">
        <div className="max-w-7xl mx-auto text-center">
          {/* Main Heading */}
          <div className="animate-fade-in mb-12">
            <div className="inline-block mb-6">
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-lg font-semibold px-6 py-3 rounded-full shadow-lg hover:scale-105 transition-transform duration-300">
                आवाज़-संचालित शिकायत मंच
              </span>
            </div>

            <h2 className="text-6xl md:text-8xl font-black mb-8 leading-tight hover-lift">
              <span className="gradient-text animate-text-glow">Janta Voice</span>
            </h2>

            <p className="text-xl md:text-2xl text-gray-700 max-w-4xl mx-auto mb-4 leading-relaxed animate-fade-in">
              क्रांतिकारी आवाज़-संचालित शिकायत प्रणाली,
              <span className="text-blue-600 font-semibold"> जो आपकी चिंताओं को कार्रवाई में बदलती है</span>
            </p>
            <p className="text-gray-500 max-w-2xl mx-auto animate-pulse-soft">
              अपनी भाषा में बोलें • तुरंत जवाब पाएँ • वास्तविक समय में प्रगति देखें
            </p>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-20 animate-slide-up_2.0s" style={{ animationDelay: '0.1s' }}>
            <button
              onClick={() => navigate("/login")}
              className="group relative bg-gradient-to-r from-blue-600 to-blue-700 px-12 py-5 rounded-2xl text-xl font-bold shadow-2xl transition-all duration-500 hover:scale-110 hover:shadow-blue-500/25 min-w-[250px] overflow-hidden hover-lift animate-soft-glow"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="absolute inset-0 animate-shimmer group-hover:animate-none"></div>
              <span className="relative flex items-center justify-center text-white">
                <Users className="w-6 h-6 mr-3 group-hover: transition-transform duration-100" />
                Start as User
                <ChevronRight className="w-6 h-6 ml-3 group-hover:translate-x-2 transition-transform duration-300" />
              </span>
            </button>


            <button
              onClick={() => navigate('/admin-login')}
              className="group relative bg-gradient-to-r from-green-600 to-teal-600 px-12 py-5 rounded-2xl text-xl font-bold shadow-2xl transition-all duration-500 hover:scale-110 hover:shadow-green-500/25 min-w-[250px] overflow-hidden hover-lift animate-soft-glow"
              style={{ animationDelay: '0.5s' }}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-green-400 to-teal-400 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="absolute inset-0 animate-shimmer group-hover:animate-none"></div>
              <span className="relative flex items-center justify-center text-white">
                <Shield className="w-6 h-6 mr-3 group-hover: transition-transform duration-100" />
                Admin Portal
                <ArrowRight className="w-6 h-6 ml-3 group-hover:translate-x-2 transition-transform duration-300" />
              </span>
            </button>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="relative z-10 px-6 py-0">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16 animate-slide-up">
            <h3 className="text-5xl font-bold text-gray-800 mb-6">
              क्यों चुनें  <span className="gradient-text">जनता वॉइस ?</span>
            </h3>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              शिकायत प्रबंधन का भविष्य, नई तकनीक के साथ
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Mic,
                title: "आवाज़ से शुरुआत का अनुभव",
                description: "किसी भी भारतीय भाषा में आसानी से बोलें। हमारी एआई संदर्भ, भावनाएँ और ज़रूरत को समझती है।",
                gradient: "from-blue-500 to-cyan-500",
                delay: "0s"
              },
              {
                icon: Zap,
                title: "बिजली-सी तेज़ प्रक्रिया",
                description: "शिकायतों की तुरंत प्रक्रिया, श्रेणीकरण और सही विभाग तक पहुंच।",
                gradient: "from-green-500 to-emerald-500",
                delay: "0.2s"
              },
              {
                icon: BarChart3,
                title: "स्मार्ट डैशबोर्ड",
                description: "उन्नत ट्रैकिंग, भावनात्मक विश्लेषण और समाधान का अनुमान।",
                gradient: "from-purple-500 to-pink-500",
                delay: "0.4s"
              }
            ].map((feature, index) => (
              <div key={index} className="group animate-slide-up hover-lift" style={{ animationDelay: feature.delay }}>
                <div className="glass-effect rounded-3xl p-8 hover:bg-white/35 transition-all duration-500 hover:scale-105 hover:rotate-1 h-full animate-soft-glow">
                  <div className={`w-16 h-16 bg-gradient-to-r ${feature.gradient} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-12 transition-all duration-300 shadow-lg`}>
                    <feature.icon className="w-8 h-8 text-white" />
                  </div>
                  <h4 className="text-2xl font-bold text-gray-800 mb-4 group-hover:text-blue-600 transition-colors duration-300">
                    {feature.title}
                  </h4>
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                  <div className="mt-6 flex items-center text-blue-600 group-hover:text-blue-700 transition-colors duration-300">
                    <span className="font-semibold">और जानें</span>
                    <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform duration-300" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Demo Section */}
      <div className="relative z-10 px-6 py-20">
        <div className="max-w-5xl mx-auto text-center">
          <div className="glass-effect-strong rounded-3xl p-12 hover:bg-white/40 transition-all duration-500 animate-slide-up hover-lift animate-soft-glow">
            <div className="mb-8">
              <div className="w-20 h-20 bg-gradient-to-r from-red-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-6 hover:scale-105 transition-transform duration-300">
                <Play className="w-10 h-10 text-white ml-1" />
              </div>
              <h3 className="text-4xl font-bold text-gray-800 mb-4">
                इसे <span className="gradient-text">चलते देखें</span>
              </h3>
              <p className="text-xl text-gray-600 mb-8 animate-pulse-soft">
                देखें कैसे जनता वॉइस एक साधारण आवाज़ शिकायत को ठोस परिणामों में बदल देता है
              </p>
            </div>

            <button className="group bg-gradient-to-r from-red-600 to-orange-600 px-10 py-4 rounded-2xl text-lg font-bold shadow-xl transition-all duration-300 hover:scale-105 hover:shadow-red-500/25 hover-lift animate-soft-glow">
              <span className="flex items-center justify-center text-white">
                <Play className="w-5 h-5 mr-3" />
                डेमो वीडियो देखें
                <ArrowRight className="w-5 h-5 ml-3 group-hover:translate-x-1 transition-transform duration-300" />
              </span>
            </button>
          </div>
        </div>
      </div>

      {/* Footer Wave */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg className="w-full h-32 text-blue-100/40 animate-wave-motion" fill="currentColor" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity="0.6"></path>
        </svg>
      </div>
    </div>
  );
};

export default Home;