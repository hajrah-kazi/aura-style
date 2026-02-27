"use client";
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { loginUser } from '@/lib/api';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/Navbar';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('username', email); // FastAPI OAuth2 uses 'username'
        formData.append('password', password);

        try {
            const res = await loginUser(formData);
            localStorage.setItem('token', res.data.access_token);
            router.push('/');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Login failed');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center px-6">
            <Navbar />
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass p-10 rounded-3xl w-full max-w-md space-y-8"
            >
                <div className="text-center space-y-2">
                    <h1 className="text-3xl font-bold">Welcome Back</h1>
                    <p className="text-foreground/60">Log in to see your personalized picks</p>
                </div>

                <form onSubmit={handleLogin} className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-sm font-medium ml-1">Email</label>
                        <input
                            type="email"
                            required
                            className="w-full glass bg-white/5 border-white/10 rounded-xl px-4 py-3 outline-none focus:ring-2 ring-primary/50 transition-all"
                            placeholder="name@example.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium ml-1">Password</label>
                        <input
                            type="password"
                            required
                            className="w-full glass bg-white/5 border-white/10 rounded-xl px-4 py-3 outline-none focus:ring-2 ring-primary/50 transition-all"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>

                    {error && <p className="text-red-400 text-sm text-center">{error}</p>}

                    <button
                        type="submit"
                        className="w-full bg-primary hover:bg-primary/80 py-4 rounded-xl font-bold transition-all shadow-lg shadow-primary/20"
                    >
                        Sign In
                    </button>
                </form>

                <p className="text-center text-sm text-foreground/40">
                    Don't have an account? <span className="text-primary hover:underline cursor-pointer">Register now</span>
                </p>
            </motion.div>
        </div>
    );
}
