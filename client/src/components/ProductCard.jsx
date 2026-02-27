import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { motion } from 'framer-motion';

export default function ProductCard({ product }) {
    const { addToCart } = useCart();

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            style={{
                display: 'flex', flexDirection: 'column', gap: '1rem',
                background: '#121212', borderRadius: '1.5rem', padding: '1.5rem',
                position: 'relative', overflow: 'hidden', height: '100%',
                cursor: 'pointer'
            }}
            className="group"
        >
            <Link to={`/products/${product.id}`} style={{ display: 'block', overflow: 'hidden', borderRadius: '1rem', aspectRatio: '1/1', background: '#000' }}>
                <motion.img
                    whileHover={{ scale: 1.05 }}
                    transition={{ duration: 0.4 }}
                    src={product.image_url}
                    alt={product.name}
                    style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: 0.9 }}
                />
            </Link>

            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                    {product.category}
                </div>
                <Link to={`/products/${product.id}`}>
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 600, lineHeight: 1.3, marginBottom: '0.5rem', color: '#fff' }}>
                        {product.name}
                    </h3>
                </Link>
                <div style={{ marginTop: 'auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>${product.price}</span>
                    <button
                        onClick={(e) => { e.preventDefault(); addToCart(product); }}
                        style={{
                            width: '32px', height: '32px', borderRadius: '50%', background: '#fff', color: '#000',
                            display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold'
                        }}
                    >
                        +
                    </button>
                </div>
            </div>
        </motion.div>
    );
}
