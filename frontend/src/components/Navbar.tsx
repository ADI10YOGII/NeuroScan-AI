import React from 'react';
import { Brain, Activity } from 'lucide-react';

export const Navbar: React.FC = () => {
    return (
        <nav className="border-b border-slate-800 bg-slate-950/50 backdrop-blur-md sticky top-0 z-50">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="bg-primary-500/10 p-2 rounded-lg">
                        <Brain className="w-6 h-6 text-primary-400" />
                    </div>
                    <span className="font-display font-bold text-xl text-slate-100">NeuroScan AI</span>
                </div>

                <div className="flex items-center gap-6">
                    <div className="hidden md:flex items-center gap-2 text-sm font-medium text-green-400 bg-green-400/10 px-3 py-1 rounded-full border border-green-400/20">
                        <Activity className="w-4 h-4" />
                        <span>System Operational</span>
                    </div>
                    <button className="text-sm font-medium text-slate-400 hover:text-slate-100 transition-colors">
                        About Technology
                    </button>
                </div>
            </div>
        </nav>
    );
};
