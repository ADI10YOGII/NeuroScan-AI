import React, { useState } from 'react';
import { CheckCircle, AlertTriangle, Activity, Brain, FileText, ArrowRight } from 'lucide-react';
import { PredictionResult } from '../utils/api';
import { AnalysisCharts } from './AnalysisCharts';
import { ReportGenerator } from './ReportGenerator';
import { cn } from '../lib/utils';

interface ResultsPanelProps {
    result: PredictionResult;
    onReset: () => void;
}

export const ResultsPanel: React.FC<ResultsPanelProps> = ({ result, onReset }) => {
    const [activeTab, setActiveTab] = useState<'overview' | 'analysis'>('overview');

    return (
        <div className="w-full max-w-6xl mx-auto animate-fade-in-up">
            {/* Header Status */}
            <div className="mb-8 text-center">
                <div className={cn(
                    "inline-flex items-center gap-2 px-4 py-2 rounded-full border mb-4",
                    result.has_tumor
                        ? "bg-red-500/10 border-red-500/50 text-red-400"
                        : "bg-green-500/10 border-green-500/50 text-green-400"
                )}>
                    {result.has_tumor ? <AlertTriangle className="w-5 h-5" /> : <CheckCircle className="w-5 h-5" />}
                    <span className="font-medium tracking-wide">Analysis Complete</span>
                </div>
                <h2 className="text-4xl md:text-5xl font-display font-bold text-slate-50 mb-2">
                    {result.result}
                </h2>
                <p className="text-slate-400 text-lg">
                    Confidence Score: <span className="text-primary-400 font-semibold">{(result.confidence * 100).toFixed(2)}%</span>
                </p>
            </div>

            {/* Main Dashboard Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                {/* Left Column: Image & Quick Stats */}
                <div className="lg:col-span-1 space-y-6">
                    {/* Image Card */}
                    <div className="glass-panel p-4 rounded-2xl">
                        <h3 className="text-slate-200 font-semibold mb-3 flex items-center gap-2">
                            <Brain className="w-5 h-5 text-primary-400" />
                            Scan Analysis
                        </h3>
                        <div className="relative aspect-square rounded-xl overflow-hidden border border-slate-700/50 bg-slate-950">
                            {result.processed_image ? (
                                <img
                                    src={`data:image/png;base64,${result.processed_image}`}
                                    alt="Processed Scan"
                                    className="w-full h-full object-contain"
                                />
                            ) : (
                                <div className="flex items-center justify-center h-full text-slate-500">
                                    No processed image available
                                </div>
                            )}
                            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-slate-950 to-transparent p-4">
                                <p className="text-xs text-slate-300 font-mono">Processed Input (240x240)</p>
                            </div>
                        </div>
                    </div>

                    {/* Quick Actions */}
                    <div className="glass-panel p-4 rounded-2xl">
                        <ReportGenerator result={result} />
                        <button
                            onClick={onReset}
                            className="w-full mt-3 py-3 px-4 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 transition-colors flex items-center justify-center gap-2"
                        >
                            Analyze Another Scan
                            <ArrowRight className="w-4 h-4" />
                        </button>
                    </div>
                </div>

                {/* Right Column: Detailed Analysis */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Tabs */}
                    <div className="flex gap-4 border-b border-slate-800 pb-1">
                        <button
                            onClick={() => setActiveTab('overview')}
                            className={cn(
                                "pb-3 px-2 text-sm font-medium transition-colors relative",
                                activeTab === 'overview' ? "text-primary-400" : "text-slate-400 hover:text-slate-200"
                            )}
                        >
                            Overview
                            {activeTab === 'overview' && (
                                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-400 rounded-full" />
                            )}
                        </button>
                        <button
                            onClick={() => setActiveTab('analysis')}
                            className={cn(
                                "pb-3 px-2 text-sm font-medium transition-colors relative",
                                activeTab === 'analysis' ? "text-primary-400" : "text-slate-400 hover:text-slate-200"
                            )}
                        >
                            Detailed Metrics
                            {activeTab === 'analysis' && (
                                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-400 rounded-full" />
                            )}
                        </button>
                    </div>

                    {/* Tab Content */}
                    <div className="min-h-[400px]">
                        {activeTab === 'overview' ? (
                            <div className="space-y-6">
                                <div className="glass-panel p-6 rounded-2xl">
                                    <h3 className="text-xl font-semibold text-slate-100 mb-4 flex items-center gap-2">
                                        <Activity className="w-5 h-5 text-primary-400" />
                                        AI Interpretation
                                    </h3>
                                    <p className="text-slate-300 leading-relaxed text-lg">
                                        {result.message}
                                    </p>
                                    <div className="mt-6 p-4 bg-slate-800/50 rounded-xl border border-slate-700/50">
                                        <h4 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-2">Recommendation</h4>
                                        <p className="text-slate-200">
                                            {result.has_tumor
                                                ? "Immediate consultation with a neurologist is recommended for further validation. Please download the report and share it with your medical provider."
                                                : "No anomalies detected. However, regular check-ups are advised if symptoms persist. Consult a specialist for a comprehensive evaluation."}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="space-y-6">
                                {result.histogram && <AnalysisCharts histogram={result.histogram} />}

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="glass-panel p-4 rounded-xl">
                                        <div className="text-slate-400 text-sm mb-1">Model Architecture</div>
                                        <div className="text-slate-100 font-semibold">CNN (VGG-Style)</div>
                                    </div>
                                    <div className="glass-panel p-4 rounded-xl">
                                        <div className="text-slate-400 text-sm mb-1">Input Resolution</div>
                                        <div className="text-slate-100 font-semibold">240 x 240 px</div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Disclaimer */}
            <div className="text-center text-slate-500 text-sm max-w-2xl mx-auto border-t border-slate-800 pt-8">
                <p>
                    <span className="text-red-400/80 font-semibold">Medical Disclaimer:</span> This tool is for educational and research purposes only.
                    It is not a substitute for professional medical advice, diagnosis, or treatment.
                    Always seek the advice of your physician or other qualified health provider.
                </p>
            </div>
        </div>
    );
};
