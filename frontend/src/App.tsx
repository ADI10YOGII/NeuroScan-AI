import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { UploadZone } from './components/UploadZone';
import { ResultsPanel } from './components/ResultsPanel';
import { predictImage, PredictionResult } from './utils/api';
import { Brain } from 'lucide-react';

function App() {
    const [prediction, setPrediction] = useState<PredictionResult | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileSelect = async (file: File) => {
        setIsLoading(true);
        setError(null);
        try {
            const result = await predictImage(file);
            setPrediction(result);
        } catch (err) {
            setError('Failed to analyze image. Please try again.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleReset = () => {
        setPrediction(null);
        setError(null);
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-50 selection:bg-primary-500/30">
            <Navbar />

            <main className="container mx-auto px-4 py-8 md:py-12">
                {!prediction ? (
                    <div className="space-y-16">
                        <Hero />

                        <div className="max-w-3xl mx-auto">
                            <div className="glass-panel p-1 rounded-3xl">
                                <div className="bg-slate-900/80 rounded-[20px] p-8 md:p-12">
                                    <h2 className="text-2xl font-semibold text-center mb-8 text-slate-200">
                                        Upload MRI Scan for Analysis
                                    </h2>

                                    {error && (
                                        <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-center">
                                            {error}
                                        </div>
                                    )}

                                    {isLoading ? (
                                        <div className="flex flex-col items-center justify-center py-12 space-y-6">
                                            <div className="relative w-24 h-24">
                                                <div className="absolute inset-0 border-4 border-slate-800 rounded-full"></div>
                                                <div className="absolute inset-0 border-4 border-primary-500 rounded-full border-t-transparent animate-spin"></div>
                                                <Brain className="absolute inset-0 m-auto text-primary-500 w-8 h-8 animate-pulse" />
                                            </div>
                                            <div className="text-center space-y-2">
                                                <h3 className="text-xl font-medium text-slate-200">Analyzing Scan...</h3>
                                                <p className="text-slate-400">Processing image and running AI model</p>
                                            </div>
                                        </div>
                                    ) : (
                                        <UploadZone onFileSelect={handleFileSelect} />
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                ) : (
                    <ResultsPanel
                        result={prediction}
                        onReset={handleReset}
                    />
                )}
            </main>
        </div>
    );
}

export default App;
