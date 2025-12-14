import React from 'react';
import Dashboard from './components/Dashboard';

const App: React.FC = () => {
    return (
        <div className="min-h-screen">
            <header className="relative bg-gradient-to-r from-[#C15F3C] to-[#E07A47] shadow-2xl overflow-hidden">
                {/* Decorative pattern */}
                <div className="absolute inset-0 opacity-10">
                    <svg width="100%" height="100%">
                        <pattern id="pattern" x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
                            <circle cx="30" cy="30" r="2" fill="white" />
                        </pattern>
                        <rect width="100%" height="100%" fill="url(#pattern)" />
                    </svg>
                </div>

                <div className="relative max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
                    <div className="text-center">
                        <h1 className="text-6xl md:text-7xl font-bold text-white mb-3 tracking-tight">
                            Climate Signal
                        </h1>
                        <p className="text-white/90 text-lg tracking-widest uppercase font-medium">
                            Unveiling weather-market correlations
                        </p>
                    </div>
                </div>
            </header>

            <main>
                <Dashboard />
            </main>

            <footer className="bg-white border-t border-[#C15F3C]/20 mt-16">
                <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                    <p className="text-center text-sm text-[#5D5A54]">
                        © 2024 Climate Signal | Discover hidden patterns in climate and markets
                    </p>
                </div>
            </footer>
        </div>
    );
};

export default App;
