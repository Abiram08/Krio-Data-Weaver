/**
 * Loading Skeleton Components
 * Professional loading states for better UX
 */

import React from 'react';

export const MetricsSkeleton: React.FC = () => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
                <div key={i} className="metric-card animate-pulse">
                    <div className="h-3 bg-[#B1ADA1]/30 rounded w-24 mb-3"></div>
                    <div className="h-10 bg-[#C15F3C]/20 rounded w-20 mb-2"></div>
                    <div className="h-2 bg-[#B1ADA1]/20 rounded w-32"></div>
                </div>
            ))}
        </div>
    );
};

export const ChartSkeleton: React.FC = () => {
    return (
        <div className="card animate-pulse">
            <div className="h-6 bg-[#C15F3C]/20 rounded w-48 mb-6"></div>
            <div className="h-96 bg-[#B1ADA1]/10 rounded"></div>
        </div>
    );
};

export const InsightsSkeleton: React.FC = () => {
    return (
        <div className="card animate-pulse">
            <div className="h-6 bg-[#C15F3C]/20 rounded w-64 mb-6"></div>
            <div className="space-y-4">
                <div className="h-4 bg-[#B1ADA1]/20 rounded w-full"></div>
                <div className="h-4 bg-[#B1ADA1]/20 rounded w-5/6"></div>
                <div className="h-4 bg-[#B1ADA1]/20 rounded w-4/6"></div>
            </div>
        </div>
    );
};

export const MatrixSkeleton: React.FC = () => {
    return (
        <div className="card animate-pulse">
            <div className="h-6 bg-[#C15F3C]/20 rounded w-56 mb-6"></div>
            <div className="grid grid-cols-5 gap-2">
                {[...Array(20)].map((_, i) => (
                    <div key={i} className="h-16 bg-[#B1ADA1]/10 rounded"></div>
                ))}
            </div>
        </div>
    );
};

export const EmptyState: React.FC<{
    icon?: React.ReactNode;
    title: string;
    description: string;
    action?: React.ReactNode;
}> = ({ icon, title, description, action }) => {
    return (
        <div className="flex flex-col items-center justify-center py-16 px-4">
            {icon && (
                <div className="mb-4 text-[#C15F3C]/40">
                    {icon}
                </div>
            )}
            <h3 className="text-xl font-semibold text-[#2D2A26] mb-2">{title}</h3>
            <p className="text-[#5D5A54] text-center max-w-md mb-6">{description}</p>
            {action && action}
        </div>
    );
};

export default {
    MetricsSkeleton,
    ChartSkeleton,
    InsightsSkeleton,
    MatrixSkeleton,
    EmptyState
};
