import React from 'react';
import { ShieldCheck, Zap, Activity } from 'lucide-react';

export const Hero: React.FC = () => {
    return (
        <div className="text-center max-w-4xl mx-auto mb-12">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-400 text-sm font-medium mb-6 animate-fade-in-up">
                <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-primary-500"></span>
                </span>
                v2.0 Model Live
            </div>

            <h1 className="text-5xl md:text-7xl font-display font-bold text-slate-50 mb-6 tracking-tight leading-tight">
                Advanced AI for <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-accent-400">
                    Brain Tumor Detection
                </span>
            </h1>

            <p className="text-xl text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed">
                Utilizing state-of-the-art Convolutional Neural Networks to assist medical professionals in early diagnosis with <span className="text-slate-200 font-semibold">91% accuracy</span>.
            </p>

            <div className="flex flex-wrap justify-center gap-4 md:gap-8">
                {[
                    { icon: ShieldCheck, label: "Medical Grade Analysis" },
                    { icon: Zap, label: "Instant Results" },
                    { icon: Activity, label: "91% Accuracy Model" }
                ].map((item, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-slate-400 bg-slate-900/50 px-4 py-2 rounded-lg border border-slate-800/50">
                        <item.icon className="w-5 h-5 text-primary-500" />
                        <span className="font-medium">{item.label}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};
