/**
 * AI Insights Panel Component
 * Displays Gemini-powered natural language analysis
 */

import React, { useState, useEffect } from 'react';
import api from '../services/api';

interface AIInsightsPanelProps {
    correlationId: string;
}

const AIInsightsPanel: React.FC<AIInsightsPanelProps> = ({ correlationId }) => {
    const [insights, setInsights] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [expanded, setExpanded] = useState(false);

    useEffect(() => {
        if (correlationId && expanded) {
            fetchAIInsights();
        }
    }, [correlationId, expanded]);

    const fetchAIInsights = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await api.get(`/correlations/ai-insights/${correlationId}`);
            setInsights(response.data.ai_insights);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to load AI insights');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="mt-6">
            <button
                onClick={() => setExpanded(!expanded)}
                className="w-full flex items-center justify-between p-4 bg-white border-2 border-gray-300 text-black rounded-xl shadow-md hover:shadow-lg transition-all duration-300"
            >
                <div className="flex items-center space-x-3">
                    <svg className="w-6 h-6" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                        <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                    </svg>
                    <div className="text-left">
                        <span className="font-semibold text-lg">AI-Powered Deep Insights</span>
                        <p className="text-xs text-white/80">Advanced analysis by Gemini AI</p>
                    </div>
                </div>
                <svg
                    className={`w-6 h-6 transition-transform duration-300 ${expanded ? 'rotate-180' : ''}`}
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path d="M19 9l-7 7-7-7"></path>
                </svg>
            </button>

            {expanded && (
                <div className="mt-4 card animate-fade-in">
                    {loading && (
                        <div className="flex items-center justify-center py-12">
                            <div className="flex flex-col items-center space-y-3">
                                <div className="spinner"></div>
                                <p className="text-[#5D5A54]">Generating AI insights...</p>
                            </div>
                        </div>
                    )}

                    {error && (
                        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 text-red-800">
                            <div className="flex items-start space-x-2">
                                <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path>
                                </svg>
                                <div>
                                    <p className="font-medium">Error loading insights</p>
                                    <p className="text-sm mt-1">{error}</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {insights && !loading && (
                        <div className="space-y-6">
                            <div className="flex items-center justify-between pb-4 border-b border-[#C15F3C]/20">
                                <h3 className="text-xl font-bold text-[#C15F3C]">AI Analysis</h3>
                                <span className="px-3 py-1 bg-white border border-gray-300 text-black text-xs font-semibold rounded-full">
                                    POWERED BY GEMINI
                                </span>
                            </div>

                            {/* Statistical Interpretation */}
                            {insights.statistical && (
                                <div className="space-y-2">
                                    <div className="flex items-center space-x-2">
                                        <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                                            <svg className="w-5 h-5 text-blue-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                                                <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                                            </svg>
                                        </div>
                                        <h4 className="font-semibold text-[#2D2A26]">Statistical Interpretation</h4>
                                    </div>
                                    <p className="text-[#5D5A54] leading-relaxed pl-10">{insights.statistical}</p>
                                </div>
                            )}

                            {/* Potential Explanations */}
                            {insights.explanations && (
                                <div className="space-y-2">
                                    <div className="flex items-center space-x-2">
                                        <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                                            <svg className="w-5 h-5 text-green-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                                                <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                                            </svg>
                                        </div>
                                        <h4 className="font-semibold text-[#2D2A26]">Potential Explanations</h4>
                                    </div>
                                    <p className="text-[#5D5A54] leading-relaxed pl-10">{insights.explanations}</p>
                                </div>
                            )}

                            {/* Investment Implications */}
                            {insights.implications && (
                                <div className="space-y-2">
                                    <div className="flex items-center space-x-2">
                                        <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                                            <svg className="w-5 h-5 text-orange-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                                                <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                            </svg>
                                        </div>
                                        <h4 className="font-semibold text-[#2D2A26]">Investment Implications</h4>
                                    </div>
                                    <p className="text-[#5D5A54] leading-relaxed pl-10">{insights.implications}</p>
                                </div>
                            )}

                            {/* Recommendations */}
                            {insights.recommendations && (
                                <div className="space-y-2">
                                    <div className="flex items-center space-x-2">
                                        <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                                            <svg className="w-5 h-5 text-purple-600" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                                                <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
                                            </svg>
                                        </div>
                                        <h4 className="font-semibold text-[#2D2A26]">Recommendations</h4>
                                    </div>
                                    <p className="text-[#5D5A54] leading-relaxed pl-10">{insights.recommendations}</p>
                                </div>
                            )}

                            {/* Disclaimer */}
                            <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                                <p className="text-xs text-yellow-800">
                                    <span className="font-semibold">Disclaimer:</span> AI-generated insights are for informational purposes only and should not be considered as financial advice. Always conduct your own research and consult with financial professionals before making investment decisions.
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default AIInsightsPanel;
