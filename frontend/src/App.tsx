import { Routes, Route } from "react-router-dom";
import Home from "@/pages/Home";
import AICurator from "@/pages/AICurator";
import TimeStream from "@/pages/TimeStream";
import MemoryPalette from "@/pages/MemoryPalette";
import ThemeMuseum from "@/pages/ThemeMuseum";
import PrivateDiary from "@/pages/PrivateDiary";
import { useState } from "react";
import { AuthContext } from '@/contexts/authContext';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const logout = () => {
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, setIsAuthenticated, logout }}
    >
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/timestream" element={<TimeStream />} />
        <Route path="/aicurator" element={<AICurator />} />
        <Route path="/memorypalette" element={<MemoryPalette />} />
         <Route path="/thememuseum" element={<ThemeMuseum />} />
         <Route path="/privatediary" element={<PrivateDiary />} />
        <Route path="/other" element={<div className="text-center text-xl">Other Page - Coming Soon</div>} />
      </Routes>
    </AuthContext.Provider>
  );
}
