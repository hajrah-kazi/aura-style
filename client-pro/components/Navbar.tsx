"use client";
import React, { useEffect, useState } from 'react';
import { ShoppingBag, User, Search, Menu, X } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';

export default function Navbar() {
    const pathname = usePathname();
    const [scrolled, setScrolled] = useState(false);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const links = [
        { name: 'Home', href: '/' },
        { name: 'Catalog', href: '/catalog' },
        { name: 'For You', href: '/recommendations' },
    ];

    return (
        <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'py-4' : 'py-8'}`}>
            <div className="max-w-7xl mx-auto px-6">
                <div className={`glass rounded-[2rem] px-8 py-5 flex items-center justify-between transition-all duration-300 ${scrolled ? 'shadow-2xl' : ''}`}>
                    <Link href="/" className="text-3xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-primary via-indigo-400 to-indigo-600">
                        AuraStyle
                    </Link>

                    <div className="hidden md:flex items-center gap-10">
                        {links.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                className={`text-sm font-bold transition-all relative group ${pathname === link.href ? 'text-primary' : 'text-foreground/50 hover:text-foreground'
                                    }`}
                            >
                                {link.name}
                                {pathname === link.href && (
                                    <motion.div layoutId="underline" className="absolute -bottom-1 left-0 right-0 h-0.5 bg-primary rounded-full" />
                                )}
                            </Link>
                        ))}
                    </div>

                    <div className="flex items-center gap-4">
                        <button className="p-3 hover:bg-white/5 rounded-2xl transition-colors text-foreground/70">
                            <Search size={22} />
                        </button>
                        <button className="p-3 hover:bg-white/5 rounded-2xl transition-colors text-foreground/70 relative">
                            <ShoppingBag size={22} />
                            <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-primary rounded-full ring-4 ring-[#030408]"></span>
                        </button>
                        <div className="h-6 w-[1px] bg-white/10 mx-2 hidden md:block"></div>
                        <Link href="/auth/login" className="hidden md:flex items-center gap-3 bg-primary/10 hover:bg-primary/20 text-primary px-6 py-3 rounded-2xl transition-all border border-primary/20 font-bold text-sm">
                            <User size={20} />
                            Account
                        </Link>

                        <button
                            className="md:hidden p-3 glass rounded-2xl"
                            onClick={() => setIsOpen(!isOpen)}
                        >
                            {isOpen ? <X size={22} /> : <Menu size={22} />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="md:hidden absolute top-28 left-6 right-6 glass rounded-[2.5rem] p-8 space-y-6 shadow-2xl"
                    >
                        {links.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                onClick={() => setIsOpen(false)}
                                className="block text-2xl font-bold text-foreground/80 hover:text-primary transition-colors"
                            >
                                {link.name}
                            </Link>
                        ))}
                        <hr className="border-white/5" />
                        <Link
                            href="/auth/login"
                            onClick={() => setIsOpen(false)}
                            className="flex items-center gap-3 text-primary text-xl font-bold"
                        >
                            <User size={24} /> Account
                        </Link>
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
}
