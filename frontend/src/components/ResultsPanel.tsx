import React, { useState } from 'react';
import { CheckCircle, AlertTriangle, Activity, Brain, FileText, ArrowRight, Eye, Layers, BarChart2 } from 'lucide-react';
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
    const [viewMode, setViewMode] = useState<'processed' | 'heatmap'>('processed');

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
                        <div className="flex items-center justify-between mb-3">
                            <h3 className="text-slate-200 font-semibold flex items-center gap-2">
                                <Brain className="w-5 h-5 text-primary-400" />
                                Scan Analysis
                            </h3>
                            <div className="flex bg-slate-900/50 rounded-lg p-1">
                                <button
                                    onClick={() => setViewMode('processed')}
                                    className={cn("p-1.5 rounded-md transition-colors", viewMode === 'processed' ? "bg-slate-700 text-white" : "text-slate-400 hover:text-slate-200")}
                                    title="Processed View"
                                >
                                    <Eye className="w-4 h-4" />
                                </button>
                                <button
                                    onClick={() => setViewMode('heatmap')}
                                    className={cn("p-1.5 rounded-md transition-colors", viewMode === 'heatmap' ? "bg-slate-700 text-white" : "text-slate-400 hover:text-slate-200")}
                                    title="AI Attention (Grad-CAM)"
                                >
                                    <Layers className="w-4 h-4" />
                                </button>
                            </div>
                        </div>

                        <div className="relative aspect-square rounded-xl overflow-hidden border border-slate-700/50 bg-slate-950 group">
                            {viewMode === 'processed' ? (
                                result.processed_image ? (
                                    <img
                                        src={`data:image/png;base64,${result.processed_image}`}
                                        alt="Processed Scan"
                                        className="w-full h-full object-contain"
                                    />
                                ) : (
                                    <div className="flex items-center justify-center h-full text-slate-500">No processed image</div>
                                )
                            ) : (
                                result.heatmap_image ? (
                                    <img
                                        src={`data:image/png;base64,${result.heatmap_image}`}
                                        alt="AI Heatmap"
                                        className="w-full h-full object-contain"
                                    />
                                ) : (
                                    <div className="flex items-center justify-center h-full text-slate-500">No heatmap available</div>
                                )
                            )}

                            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-slate-950 to-transparent p-4">
                                <p className="text-xs text-slate-300 font-mono flex items-center gap-2">
                                    {viewMode === 'processed' ? "Processed Input (240x240)" : "Grad-CAM Attention Map"}
                                    {viewMode === 'heatmap' && <span className="px-1.5 py-0.5 bg-green-500/20 text-green-400 rounded text-[10px]">AI Focus</span>}
                                </p>
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

                                {/* Metrics Summary */}
                                {result.metrics && (
                                    <div className="grid grid-cols-3 gap-4">
                                        <div className="glass-panel p-4 rounded-xl text-center">
                                            <div className="text-slate-400 text-xs uppercase tracking-wider mb-1">Entropy</div>
                                            <div className="text-xl font-semibold text-slate-100">{result.metrics.entropy.toFixed(2)}</div>
                                        </div>
                                        <div className="glass-panel p-4 rounded-xl text-center">
                                            <div className="text-slate-400 text-xs uppercase tracking-wider mb-1">Contrast</div>
                                            <div className="text-xl font-semibold text-slate-100">{result.metrics.contrast.toFixed(2)}</div>
                                        </div>
                                        <div className="glass-panel p-4 rounded-xl text-center">
                                            <div className="text-slate-400 text-xs uppercase tracking-wider mb-1">SNR</div>
                                            <div className="text-xl font-semibold text-slate-100">{result.metrics.snr.toFixed(2)}</div>
                                        </div>
                                    </div>
                                )}
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

                                <div className="glass-panel p-6 rounded-2xl">
                                    <h3 className="text-slate-100 font-semibold mb-4 flex items-center gap-2">
                                        <BarChart2 className="w-5 h-5 text-primary-400" />
                                        Advanced Metrics Explanation
                                    </h3>
                                    <div className="space-y-4">
                                        <div>
                                            <div className="flex justify-between text-sm mb-1">
                                                <span className="text-slate-300">Entropy (Texture)</span>
                                                <span className="text-primary-400">{result.metrics?.entropy.toFixed(2)}</span>
                                            </div>
                                            <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                                                <div className="h-full bg-primary-500 rounded-full" style={{ width: `${Math.min((result.metrics?.entropy || 0) * 10, 100)}%` }}></div>
                                            </div>
                                            <p className="text-xs text-slate-500 mt-1">Measures the complexity and texture of the brain tissue.</p>
                                        </div>
                                        <div>
                                            <div className="flex justify-between text-sm mb-1">
                                                <span className="text-slate-300">Signal-to-Noise Ratio</span>
                                                <span className="text-primary-400">{result.metrics?.snr.toFixed(2)}</span>
                                            </div>
                                            <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                                                <div className="h-full bg-green-500 rounded-full" style={{ width: `${Math.min((result.metrics?.snr || 0) * 20, 100)}%` }}></div>
                                            </div>
                                            <p className="text-xs text-slate-500 mt-1">Indicates the clarity of the scan relative to background noise.</p>
                                        </div>
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
