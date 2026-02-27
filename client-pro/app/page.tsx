"use client";
import React, { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import ProductCard from '@/components/ProductCard';
import { getTrending, getPersonalized, getProducts } from '@/lib/api';
import { motion } from 'framer-motion';
import { Sparkles, TrendingUp, Gift, ArrowRight, Zap, ShieldCheck, Globe } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
    const [trending, setTrending] = useState([]);
    const [personalized, setPersonalized] = useState([]);
    const [catalog, setCatalog] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchData() {
            try {
                const [t, p, c] = await Promise.all([
                    getTrending(),
                    getPersonalized().catch(() => ({ data: [] })),
                    getProducts()
                ]);
                setTrending(t.data);
                setPersonalized(p.data);
                setCatalog(c.data);
            } catch (err) {
                console.error("Failed to fetch products", err);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    return (
        <div className="min-h-screen">
            <Navbar />

            {/* Hero Section */}
            <section className="relative pt-48 pb-32 px-6 overflow-hidden">
                {/* Animated Background Orbs */}
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/20 rounded-full blur-[120px] -mr-64 -mt-64 animate-pulse"></div>
                <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-indigo-600/10 rounded-full blur-[100px] -ml-48 -mb-48"></div>

                <div className="max-w-7xl mx-auto relative z-10">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
                        className="text-center space-y-10"
                    >
                        <div className="inline-flex items-center gap-2 glass px-6 py-2 rounded-full text-xs font-black tracking-widest text-primary border-primary/20">
                            <Zap size={14} fill="currentColor" /> NEXT-GEN SHOPPING
                        </div>

                        <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-[0.9] text-white">
                            Revolutionizing <br />
                            <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary via-indigo-400 to-indigo-600">e-Commerce</span>
                        </h1>

                        <p className="text-foreground/60 text-xl md:text-2xl max-w-2xl mx-auto font-medium leading-relaxed">
                            Unlock a hyper-personalized shopping experience powered by our industry-grade ML hybrid recommendation engine.
                        </p>

                        <div className="flex flex-col sm:flex-row justify-center gap-6 pt-4">
                            <Link href="/catalog" className="btn-primary flex items-center justify-center gap-3 group">
                                Shop Collection <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
                            </Link>
                            <Link href="/recommendations" className="glass px-10 py-5 rounded-2xl font-bold flex items-center justify-center gap-3 hover:bg-white/10 transition-all">
                                AI Recommendations
                            </Link>
                        </div>

                        {/* Trust Badges */}
                        <div className="pt-16 flex flex-wrap justify-center gap-12 text-foreground/30 font-black uppercase tracking-[0.3em] text-[10px]">
                            <div className="flex items-center gap-2"><ShieldCheck size={16} /> Secure SSL</div>
                            <div className="flex items-center gap-2"><Globe size={16} /> Global Shipping</div>
                            <div className="flex items-center gap-2"><Zap size={16} /> ML Optimized</div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Recommended for You */}
            {personalized.length > 0 && (
                <section className="py-24 px-6 max-w-7xl mx-auto">
                    <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16">
                        <div className="space-y-4">
                            <div className="flex items-center gap-3 text-pink-500 font-black text-xs tracking-widest uppercase">
                                <Sparkles size={18} /> YOUR SPECIAL PICKS
                            </div>
                            <h2 className="text-4xl md:text-5xl font-black text-white">Matched for You</h2>
                        </div>
                        <Link href="/recommendations" className="text-primary font-bold flex items-center gap-2 hover:gap-3 transition-all border-b border-primary/0 hover:border-primary pb-1">
                            View Personalized Feed <ArrowRight size={18} />
                        </Link>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {personalized.map((p: any) => (
                            <ProductCard key={p.id} product={p} />
                        ))}
                    </div>
                </section>
            )}

            {/* Trending Section */}
            <section className="py-24 px-6 max-w-7xl mx-auto border-t border-white/5">
                <div className="space-y-4 mb-16">
                    <div className="flex items-center gap-3 text-orange-500 font-black text-xs tracking-widest uppercase">
                        <TrendingUp size={18} /> Popular Items
                    </div>
                    <h2 className="text-4xl md:text-5xl font-black text-white">Trending Now</h2>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {trending.map((p: any) => (
                        <ProductCard key={p.id} product={p} />
                    ))}
                </div>
            </section>

            {/* Banner / Value Prop */}
            <section className="py-24 px-6 max-w-7xl mx-auto">
                <div className="glass rounded-[4rem] p-12 md:p-24 relative overflow-hidden text-center space-y-8 bg-gradient-to-br from-primary/5 to-transparent">
                    <h3 className="text-4xl md:text-6xl font-black text-white leading-tight">
                        The Future of Shopping is <br /> <span className="text-primary">Intelligent.</span>
                    </h3>
                    <p className="text-foreground/50 text-lg max-w-xl mx-auto">
                        Our hybrid recommender combines SVD matrix factorization with transformer-based NLP to understand your taste better than anyone else.
                    </p>
                    <div className="pt-6">
                        <Link href="/auth/login" className="btn-primary px-12 py-5">
                            Get Started Now
                        </Link>
                    </div>

                    <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-[80px] -mr-32 -mt-32"></div>
                </div>
            </section>

            {/* Full Catalog Grid */}
            <section id="catalog" className="py-24 px-6 max-w-7xl mx-auto border-t border-white/5">
                <div className="flex items-center justify-between mb-16">
                    <div className="space-y-4">
                        <div className="flex items-center gap-3 text-indigo-500 font-black text-xs tracking-widest uppercase">
                            <Gift size={18} /> THE COMPLETE STORE
                        </div>
                        <h2 className="text-4xl md:text-5xl font-black text-white">Full Catalog</h2>
                    </div>
                    <Link href="/catalog" className="glass px-6 py-3 rounded-xl font-bold text-sm hover:bg-white/10 transition-all">
                        See All
                    </Link>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-8">
                    {catalog.slice(0, 10).map((p: any) => (
                        <ProductCard key={p.id} product={p} />
                    ))}
                </div>
            </section>

            <footer className="py-32 px-6 border-t border-white/5 bg-[#030408]/50">
                <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-16">
                    <div className="space-y-6">
                        <h3 className="text-2xl font-black text-white tracking-tighter">AuraStyle</h3>
                        <p className="text-foreground/40 text-sm leading-relaxed">
                            Precision-engineered recommendation systems for the modern retail landscape. Powered by advanced SVD and Transformer architectures.
                        </p>
                    </div>
                    {/* ... links ... */}
                </div>
                <div className="max-w-7xl mx-auto pt-20 mt-20 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-8">
                    <p className="text-foreground/30 text-xs font-bold uppercase tracking-widest">© 2026 AuraStyle ML. All rights reserved.</p>
                    <div className="flex gap-8 text-foreground/40 text-xs font-bold transition-colors">
                        <a href="#" className="hover:text-primary">Privacy Policy</a>
                        <a href="#" className="hover:text-primary">Terms of Service</a>
                    </div>
                </div>
            </footer>
        </div>
    );
}
