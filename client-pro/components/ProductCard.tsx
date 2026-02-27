"use client";
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Star, ShoppingCart, ArrowRight } from 'lucide-react';
import Link from 'next/link';

interface Product {
    id: number;
    name: string;
    price: number;
    image_url: string;
    category: string;
    rating: number;
}

export default function ProductCard({ product }: { product: Product }) {
    const [isHovered, setIsHovered] = useState(false);

    return (
        <motion.div
            onHoverStart={() => setIsHovered(true)}
            onHoverEnd={() => setIsHovered(false)}
            className="glass rounded-[2rem] p-5 flex flex-col gap-5 group relative overflow-hidden"
        >
            <Link href={`/product/${product.id}`} className="block relative aspect-square rounded-[1.5rem] overflow-hidden bg-[#0A0B10]">
                <motion.img
                    src={product.image_url}
                    alt={product.name}
                    animate={{ scale: isHovered ? 1.1 : 1 }}
                    transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                    className="object-cover w-full h-full p-4"
                />

                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-6">
                    <span className="flex items-center gap-2 text-white font-bold text-sm bg-primary/80 backdrop-blur-md px-5 py-2 rounded-full">
                        Quick View <ArrowRight size={16} />
                    </span>
                </div>

                <div className="absolute top-4 right-4 bg-white/10 backdrop-blur-md px-3 py-1.5 rounded-xl text-xs font-black text-white border border-white/20">
                    ${product.price}
                </div>
            </Link>

            <div className="space-y-1">
                <div className="flex items-center justify-between">
                    <span className="text-[10px] text-primary font-black uppercase tracking-[0.2em]">{product.category}</span>
                    <div className="flex items-center gap-1 text-yellow-500">
                        <Star size={12} fill="currentColor" />
                        <span className="text-[11px] font-bold text-foreground/60">{product.rating}</span>
                    </div>
                </div>
                <h3 className="font-bold text-lg leading-tight transition-colors group-hover:text-primary line-clamp-1">
                    {product.name}
                </h3>
            </div>

            <div className="flex items-center gap-3">
                <Link
                    href={`/product/${product.id}`}
                    className="flex-grow glass hover:bg-white/10 text-center py-3.5 rounded-2xl text-xs font-bold transition-all"
                >
                    Details
                </Link>
                <button className="p-3.5 rounded-2xl bg-primary text-white hover:shadow-[0_0_20px_rgba(99,102,241,0.5)] transition-all">
                    <ShoppingCart size={18} />
                </button>
            </div>
        </motion.div>
    );
}
