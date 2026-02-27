import React from 'react';
import { useCart } from '../context/CartContext';
import { Trash2, Plus, Minus } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Cart() {
    const { cart, removeFromCart, total } = useCart();

    if (cart.length === 0) {
        return (
            <div className="container" style={{ textAlign: 'center', padding: '4rem' }}>
                <h2 style={{ marginBottom: '1rem' }}>Your cart is empty</h2>
                <Link to="/" className="btn btn-primary">Start Shopping</Link>
            </div>
        );
    }

    return (
        <div className="container" style={{ padding: '2rem 1rem' }}>
            <h1 className="section-title">Your Shopping Cart</h1>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {cart.map(item => (
                        <div key={item.id} className="glass" style={{ display: 'flex', padding: '1rem', borderRadius: '1rem', alignItems: 'center', gap: '1rem' }}>
                            <img src={item.image_url} alt={item.name} style={{ width: '80px', height: '80px', objectFit: 'cover', borderRadius: '0.5rem' }} />

                            <div style={{ flex: 1 }}>
                                <h3 style={{ marginBottom: '0.5rem' }}>{item.name}</h3>
                                <div style={{ color: 'var(--text-secondary)' }}>${item.price}</div>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', background: 'var(--bg-primary)', padding: '0.5rem', borderRadius: '2rem' }}>
                                <span style={{ fontWeight: 'bold', padding: '0 0.5rem' }}>Qty: {item.quantity}</span>
                            </div>

                            <div style={{ fontWeight: 'bold' }}>
                                ${(item.price * item.quantity).toFixed(2)}
                            </div>

                            <button onClick={() => removeFromCart(item.id)} style={{ color: 'var(--danger)', padding: '0.5rem' }}>
                                <Trash2 size={20} />
                            </button>
                        </div>
                    ))}
                </div>

                <div>
                    <div className="glass" style={{ padding: '2rem', borderRadius: '1rem', position: 'sticky', top: '100px' }}>
                        <h2 style={{ marginBottom: '1.5rem' }}>Order Summary</h2>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', fontSize: '1.1rem' }}>
                            <span>Subtotal</span>
                            <span>${total.toFixed(2)}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem', color: 'var(--text-secondary)' }}>
                            <span>Shipping</span>
                            <span>Free</span>
                        </div>
                        <div style={{ borderTop: '1px solid var(--bg-card)', paddingTop: '1rem', display: 'flex', justifyContent: 'space-between', fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '2rem' }}>
                            <span>Total</span>
                            <span>${total.toFixed(2)}</span>
                        </div>
                        <button className="btn btn-primary" style={{ width: '100%', fontSize: '1.2rem' }}>Checkout</button>
                    </div>
                </div>
            </div>
        </div>
    );
}
