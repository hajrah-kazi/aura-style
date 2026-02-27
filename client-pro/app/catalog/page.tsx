"use client";
import React, { useEffect, useState } from 'react';
import Navbar from '@/components/Navbar';
import ProductCard from '@/components/ProductCard';
import { getProducts } from '@/lib/api';
import { Search, Filter } from 'lucide-react';

export default function CatalogPage() {
    const [products, setProducts] = useState([]);
    const [search, setSearch] = useState('');
    const [category, setCategory] = useState('All');

    useEffect(() => {
        getProducts().then(res => setProducts(res.data));
    }, []);

    const categories = ["All", "Electronics", "Fashion", "Home & Living", "Fitness"];

    const filtered = products.filter((p: any) => {
        const matchesSearch = p.name.toLowerCase().includes(search.toLowerCase());
        const matchesCategory = category === 'All' || p.category === category;
        return matchesSearch && matchesCategory;
    });

    return (
        <div className="min-h-screen pb-20">
            <Navbar />

            <div className="pt-32 px-6 max-w-7xl mx-auto space-y-12">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                    <h1 className="text-4xl font-bold">Full Catalog</h1>

                    <div className="flex flex-wrap items-center gap-4">
                        <div className="relative group flex-grow md:flex-grow-0">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-foreground/40 group-focus-within:text-primary transition-colors" size={20} />
                            <input
                                type="text"
                                placeholder="Search products..."
                                className="glass pl-12 pr-6 py-3 rounded-full outline-none focus:ring-2 ring-primary/50 w-full md:w-80"
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                            />
                        </div>

                        <div className="flex items-center gap-2 overflow-x-auto pb-2 md:pb-0">
                            {categories.map(cat => (
                                <button
                                    key={cat}
                                    onClick={() => setCategory(cat)}
                                    className={`px-6 py-3 rounded-full text-sm font-semibold transition-all ${category === cat
                                            ? 'bg-primary text-white'
                                            : 'glass text-foreground/60 hover:bg-white/10'
                                        }`}
                                >
                                    {cat}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5 gap-8">
                    {filtered.map((p: any) => (
                        <ProductCard key={p.id} product={p} />
                    ))}
                    {filtered.length === 0 && (
                        <div className="col-span-full py-20 text-center text-foreground/40">
                            No products found matching your search.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
