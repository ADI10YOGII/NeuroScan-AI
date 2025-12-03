import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, Image as ImageIcon, X } from 'lucide-react';
import { cn } from '../lib/utils';

interface UploadZoneProps {
    onFileSelect: (file: File) => void;
    selectedFile: File | null;
    onClear: () => void;
    isLoading: boolean;
}

export const UploadZone: React.FC<UploadZoneProps> = ({
    onFileSelect,
    selectedFile,
    onClear,
    isLoading
}) => {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 0) {
            onFileSelect(acceptedFiles[0]);
        }
    }, [onFileSelect]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        },
        maxFiles: 1,
        disabled: isLoading
    });

    if (selectedFile) {
        return (
            <div className="w-full max-w-xl mx-auto">
                <div className="relative rounded-2xl overflow-hidden border border-slate-200 shadow-lg bg-white">
                    <div className="aspect-square w-full relative bg-slate-100 flex items-center justify-center">
                        <img
                            src={URL.createObjectURL(selectedFile)}
                            alt="Preview"
                            className="max-h-full max-w-full object-contain"
                        />
                        {!isLoading && (
                            <button
                                onClick={onClear}
                                className="absolute top-4 right-4 p-2 bg-white/80 backdrop-blur-sm rounded-full hover:bg-white transition-colors shadow-sm"
                            >
                                <X className="h-5 w-5 text-slate-600" />
                            </button>
                        )}
                    </div>
                    <div className="p-4 bg-white border-t border-slate-100 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-primary-50 rounded-lg">
                                <ImageIcon className="h-5 w-5 text-primary-600" />
                            </div>
                            <div>
                                <p className="text-sm font-medium text-slate-900 truncate max-w-[200px]">
                                    {selectedFile.name}
                                </p>
                                <p className="text-xs text-slate-500">
                                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div
            {...getRootProps()}
            className={cn(
                "w-full max-w-xl mx-auto min-h-[400px] rounded-3xl border-2 border-dashed transition-all duration-300 flex flex-col items-center justify-center p-8 cursor-pointer group",
                isDragActive
                    ? "border-primary-500 bg-primary-50/50 scale-[1.02]"
                    : "border-slate-200 hover:border-primary-300 hover:bg-slate-50"
            )}
        >
            <input {...getInputProps()} />
            <div className="w-20 h-20 bg-primary-50 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <UploadCloud className="h-10 w-10 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-slate-900 mb-2 text-center">
                Upload MRI Scan
            </h3>
            <p className="text-slate-500 text-center max-w-xs mb-6">
                Drag and drop your MRI scan here, or click to browse files
            </p>
            <div className="flex gap-2 text-xs text-slate-400 font-medium uppercase tracking-wider">
                <span>PNG</span>
                <span>•</span>
                <span>JPG</span>
                <span>•</span>
                <span>TIFF</span>
            </div>
        </div>
    );
};
