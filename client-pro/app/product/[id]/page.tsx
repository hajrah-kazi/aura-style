"use client";
import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Navbar from '@/components/Navbar';
import ProductCard from '@/components/ProductCard';
import { getProduct, getSimilar, trackInteraction } from '@/lib/api';
import { motion } from 'framer-motion';
import { Star, ShieldCheck, Truck, RefreshCcw, ShoppingCart } from 'lucide-react';

export default function ProductDetailsPage() {
    const { id } = useParams();
    const [product, setProduct] = useState<any>(null);
    const [similar, setSimilar] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchProduct() {
            try {
                const [pRes, sRes] = await Promise.all([
                    getProduct(Number(id)),
                    getSimilar(Number(id))
                ]);
                setProduct(pRes.data);
                setSimilar(sRes.data);
                // Track the view interaction
                trackInteraction(Number(id), 'view');
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        }
        fetchProduct();
    }, [id]);

    if (loading) return null;
    if (!product) return <div>Product not found</div>;

    return (
        <div className="min-h-screen pb-20">
            <Navbar />

            <div className="pt-32 px-6 max-w-7xl mx-auto">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
                    {/* Image Section */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="aspect-square glass rounded-[3rem] p-12 flex items-center justify-center overflow-hidden"
                    >
                        <img
                            src={product.image_url}
                            alt={product.name}
                            className="w-full h-full object-contain hover:scale-110 transition-transform duration-500"
                        />
                    </motion.div>

                    {/* Info Section */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="flex flex-col gap-8 justify-center"
                    >
                        <div className="space-y-4">
                            <span className="glass px-4 py-1 rounded-full text-primary text-sm font-bold uppercase tracking-widest">{product.category}</span>
                            <h1 className="text-5xl font-black">{product.name}</h1>
                            <div className="flex items-center gap-2 text-yellow-500">
                                {[...Array(5)].map((_, i) => (
                                    <Star key={i} size={20} fill={i < Math.floor(product.rating) ? "currentColor" : "none"} />
                                ))}
                                <span className="text-foreground/60 ml-2 font-medium">({product.rating} / 5.0)</span>
                            </div>
                        </div>

                        <p className="text-xl text-foreground/70 leading-relaxed">
                            {product.description}
                        </p>

                        <div className="text-4xl font-bold text-primary">
                            ${product.price}
                        </div>

                        <div className="flex gap-4">
                            <button
                                onClick={() => trackInteraction(Number(id), 'cart')}
                                className="flex-grow bg-primary hover:bg-primary/80 py-5 rounded-2xl font-bold text-lg transition-all flex items-center justify-center gap-3 shadow-xl shadow-primary/20"
                            >
                                <ShoppingCart size={24} /> Add to Cart
                            </button>
                            <button className="glass p-5 rounded-2xl hover:bg-white/10 transition-colors">
                                <Star size={24} />
                            </button>
                        </div>

                        <div className="grid grid-cols-3 gap-4 pt-8 border-t border-white/5">
                            <div className="flex flex-col items-center gap-2 text-center text-xs text-foreground/40 font-bold uppercase">
                                <ShieldCheck className="text-primary mb-1" size={24} /> Secure Payment
                            </div>
                            <div className="flex flex-col items-center gap-2 text-center text-xs text-foreground/40 font-bold uppercase">
                                <Truck className="text-primary mb-1" size={24} /> Free Shipping
                            </div>
                            <div className="flex flex-col items-center gap-2 text-center text-xs text-foreground/40 font-bold uppercase">
                                <RefreshCcw className="text-primary mb-1" size={24} /> 30 Day Returns
                            </div>
                        </div>
                    </motion.div>
                </div>

                {/* Similar Products */}
                <div className="mt-32 space-y-12">
                    <div className="flex items-center justify-between">
                        <h2 className="text-3xl font-bold">Similar Recommendations</h2>
                        <div className="glass px-4 py-2 rounded-full text-sm font-bold text-primary/80">AI Powered</div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                        {similar.map((p: any) => (
                            <ProductCard key={p.id} product={p} />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
