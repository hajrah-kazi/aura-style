"use client";
import React, { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import ProductCard from '@/components/ProductCard';
import { getPersonalized, getTrending } from '@/lib/api';
import { motion } from 'framer-motion';
import { Sparkles, BrainCircuit, History } from 'lucide-react';

export default function RecommendationsPage() {
    const [personalized, setPersonalized] = useState([]);
    const [trending, setTrending] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        async function fetchData() {
            const token = localStorage.getItem('token');
            setIsLoggedIn(!!token);

            try {
                const [pRes, tRes] = await Promise.all([
                    token ? getPersonalized() : Promise.resolve({ data: [] }),
                    getTrending()
                ]);
                setPersonalized(pRes.data);
                setTrending(tRes.data);
            } catch (err) {
                console.error("Failed to fetch recommendations", err);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    return (
        <div className="min-h-screen pb-20">
            <Navbar />

            <div className="pt-32 px-6 max-w-7xl mx-auto space-y-16">
                <header className="space-y-4">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border-primary/20 text-primary text-sm font-bold">
                        <BrainCircuit size={16} />
                        AI-POWERED INSIGHTS
                    </div>
                    <h1 className="text-5xl font-black">For You</h1>
                    <p className="text-foreground/60 text-xl max-w-2xl">
                        Our recommendation engine analyzes your interactions, preferences, and trending patterns to curate this exclusive selection.
                    </p>
                </header>

                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {[...Array(4)].map((_, i) => (
                            <div key={i} className="glass h-80 rounded-3xl animate-pulse" />
                        ))}
                    </div>
                ) : (
                    <div className="space-y-20">
                        {/* Personalized Section */}
                        <section className="space-y-8">
                            <div className="flex items-center gap-3">
                                <Sparkles className="text-primary" size={28} />
                                <h2 className="text-3xl font-bold">Matched for Your Taste</h2>
                            </div>

                            {!isLoggedIn ? (
                                <div className="glass p-12 rounded-[2.5rem] text-center space-y-6 border-dashed border-2 border-white/5">
                                    <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto text-primary">
                                        <History size={40} />
                                    </div>
                                    <div className="space-y-2">
                                        <h3 className="text-2xl font-bold">Unlock Personalized Picks</h3>
                                        <p className="text-foreground/50 max-w-md mx-auto">Log in to see products tailored specifically to your browsing history and preferences.</p>
                                    </div>
                                    <a href="/auth/login" className="inline-block bg-primary px-8 py-3 rounded-xl font-bold hover:scale-105 transition-transform">
                                        Sign In Now
                                    </a>
                                </div>
                            ) : personalized.length > 0 ? (
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                                    {personalized.map((p: any) => (
                                        <ProductCard key={p.id} product={p} />
                                    ))}
                                </div>
                            ) : (
                                <div className="glass p-12 rounded-[2.5rem] text-center text-foreground/40">
                                    Browse more products to generate personalized recommendations!
                                </div>
                            )}
                        </section>

                        {/* Trending/Popularity Section */}
                        <section className="space-y-8">
                            <div className="flex items-center gap-3">
                                <BrainCircuit className="text-indigo-400" size={28} />
                                <h2 className="text-3xl font-bold">Community Favorites</h2>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                                {trending.map((p: any) => (
                                    <ProductCard key={p.id} product={p} />
                                ))}
                            </div>
                        </section>
                    </div>
                )}
            </div>
        </div>
    );
}
