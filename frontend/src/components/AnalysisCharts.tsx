import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface HistogramData {
    name: string;
    data: number[];
}

interface AnalysisChartsProps {
    histogram: HistogramData[];
}

export const AnalysisCharts: React.FC<AnalysisChartsProps> = ({ histogram }) => {
    // Process data for Recharts (simplified for bar chart)
    // We'll take the average intensity for 10 bins to make it readable
    const processData = (channelData: number[]) => {
        const binSize = 25; // 256 / 10 approx
        const bins = [];
        for (let i = 0; i < 10; i++) {
            const start = i * binSize;
            const end = Math.min((i + 1) * binSize, 256);
            const slice = channelData.slice(start, end);
            const sum = slice.reduce((a, b) => a + b, 0);
            bins.push({
                range: `${start}-${end}`,
                value: sum,
            });
        }
        return bins;
    };

    const redData = processData(histogram.find(h => h.name === 'R')?.data || []);

    return (
        <div className="bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl p-6">
            <h3 className="text-slate-100 font-semibold mb-4">Pixel Intensity Distribution</h3>
            <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={redData}>
                        <XAxis dataKey="range" stroke="#94a3b8" fontSize={12} />
                        <YAxis stroke="#94a3b8" fontSize={12} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#f1f5f9' }}
                        />
                        <Bar dataKey="value" fill="#38bdf8" radius={[4, 4, 0, 0]}>
                            {redData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={`rgba(56, 189, 248, ${0.5 + (index / 20)})`} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
            <p className="text-xs text-slate-500 mt-2 text-center">
                Distribution of pixel brightness values in the MRI scan
            </p>
        </div>
    );
};
