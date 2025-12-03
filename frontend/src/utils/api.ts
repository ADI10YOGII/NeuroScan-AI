import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8002', // Update this for production
    headers: {
        'Content-Type': 'multipart/form-data',
    },
});

export interface PredictionResult {
    filename: string;
    result: string;
    confidence: number;
    has_tumor: boolean;
    message: string;
    processed_image?: string;
    heatmap_image?: string;
    histogram?: { name: string; data: number[] }[];
    metrics?: {
        entropy: number;
        contrast: number;
        snr: number;
    };
}

export const predictImage = async (file: File): Promise<PredictionResult> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<PredictionResult>('/predict', formData);
    return response.data;
};

export const checkHealth = async () => {
    const response = await api.get('/health');
    return response.data;
};
