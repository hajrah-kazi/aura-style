import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { Search, ShoppingBag, User, Menu, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Navbar() {
    const { user, logout } = useAuth();
    const { cart } = useCart();
    const [scrolled, setScrolled] = useState(false);
    const [menuOpen, setMenuOpen] = useState(false);
    const [searchOpen, setSearchOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <nav className={`fixed w-full z-50 transition-all duration-300 ${scrolled ? 'glass' : 'bg-transparent'}`}
            style={{
                height: 'var(--header-height)', display: 'flex', alignItems: 'center',
                background: scrolled ? 'var(--glass-surface)' : 'transparent',
                backdropFilter: scrolled ? 'blur(20px)' : 'none',
                borderBottom: scrolled ? '1px solid var(--border-light)' : 'none',
                position: 'fixed', top: 0, left: 0, right: 0, zIndex: 1000
            }}>
            <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>

                {/* Logo */}
                <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', zIndex: 100 }}>
                    <div style={{ width: 32, height: 32, background: '#fff', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <span style={{ color: '#000', fontWeight: 'bold', fontSize: '18px' }}>L</span>
                    </div>
                    <span style={{ fontSize: '1.25rem', fontWeight: 600, letterSpacing: '-0.02em' }}>LUXESHOP</span>
                </Link>

                {/* Desktop Menu */}
                <div className="hide-mobile" style={{ display: 'flex', gap: '2.5rem', alignItems: 'center' }}>
                    <Link to="/" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', transition: 'color 0.2s' }} className="hover:text-white">Store</Link>
                    <Link to="/" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', transition: 'color 0.2s' }} className="hover:text-white">Mac</Link>
                    <Link to="/" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', transition: 'color 0.2s' }} className="hover:text-white">iPad</Link>
                    <Link to="/" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', transition: 'color 0.2s' }} className="hover:text-white">iPhone</Link>
                    <Link to="/" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', transition: 'color 0.2s' }} className="hover:text-white">Watch</Link>
                    <Link to="/" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', transition: 'color 0.2s' }} className="hover:text-white">Accessories</Link>
                </div>

                {/* Actions */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                    <button onClick={() => setSearchOpen(!searchOpen)} style={{ color: 'var(--text-primary)' }}>
                        <Search size={20} strokeWidth={1.5} />
                    </button>

                    <Link to="/cart" style={{ position: 'relative', color: 'var(--text-primary)' }}>
                        <ShoppingBag size={20} strokeWidth={1.5} />
                        {cart.length > 0 && (
                            <span style={{
                                position: 'absolute', top: '-4px', right: '-4px',
                                background: 'var(--text-primary)', color: '#000',
                                borderRadius: '50%', width: '14px', height: '14px',
                                fontSize: '9px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold'
                            }}>
                                {cart.length}
                            </span>
                        )}
                    </Link>

                    {user ? (
                        <div className="hide-mobile" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                            <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>My Account</span>
                            <button onClick={logout} style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Sign Out</button>
                        </div>
                    ) : (
                        <Link to="/login" className="hide-mobile btn btn-primary" style={{ padding: '0.5rem 1rem', fontSize: '0.8rem' }}>Sign In</Link>
                    )}

                    <button className="show-mobile" onClick={() => setMenuOpen(!menuOpen)} style={{ display: 'none' }}>
                        {menuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>
            </div>

            {/* Mobile Menu Overlay would go here */}
        </nav>
    );
}
