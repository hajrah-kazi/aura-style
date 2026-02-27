import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import { useCart } from '../context/CartContext';
import { Star, Truck, ShieldCheck, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard';

export default function ProductDetail() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [recs, setRecs] = useState([]);
    const { addToCart } = useCart();

    useEffect(() => {
        window.scrollTo(0, 0);
        const fetchData = async () => {
            try {
                const res = await api.get(`/products/${id}`);
                setProduct(res.data);
                const recRes = await api.get(`/recommendations/content/${id}`);
                setRecs(recRes.data);
            } catch (e) { }
        };
        fetchData();
    }, [id]);

    if (!product) return <div style={{ height: '100vh' }}></div>;

    return (
        <div style={{ paddingTop: 'var(--header-height)', minHeight: '100vh', background: '#000' }}>

            {/* Sticky Header for Back */}
            <div style={{ padding: '1rem 2rem', borderBottom: '1px solid var(--border-light)' }}>
                <Link to="/" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)' }}>
                    <ArrowLeft size={18} /> Back to Gallery
                </Link>
            </div>

            <div className="container" style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.5fr) minmax(0, 1fr)', gap: '4rem', padding: '4rem 2rem' }}>

                {/* Gallery */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                    <div style={{ borderRadius: '2rem', overflow: 'hidden', border: '1px solid var(--border-light)', background: '#111' }}>
                        <img src={product.image_url} alt={product.name} style={{ width: '100%', objectFit: 'contain' }} />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <div style={{ aspectRatio: '16/9', background: '#111', borderRadius: '1rem' }} />
                        <div style={{ aspectRatio: '16/9', background: '#111', borderRadius: '1rem' }} />
                    </div>
                </div>

                {/* Info */}
                <div style={{ position: 'sticky', top: '120px', height: 'fit-content' }}>
                    <span style={{ color: 'var(--accent-primary)', textTransform: 'uppercase', letterSpacing: '0.1em', fontSize: '0.8rem', fontWeight: 600 }}>{product.category} Series</span>
                    <h1 style={{ marginTop: '0.5rem', marginBottom: '1rem' }}>{product.name}</h1>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                        <div style={{ display: 'flex', gap: '2px' }}>
                            {[1, 2, 3, 4, 5].map(i => <Star key={i} size={16} fill={i <= product.rating ? "#fff" : "none"} stroke="#fff" />)}
                        </div>
                        <span style={{ color: 'var(--text-secondary)' }}>4.9 (12 reviews)</span>
                    </div>

                    <div style={{ fontSize: '2.5rem', fontWeight: 600, marginBottom: '2rem' }}>${product.price}</div>

                    <p style={{ fontSize: '1.1rem', marginBottom: '2rem' }}>{product.description}</p>

                    <div style={{ display: 'flex', gap: '1rem', marginBottom: '3rem' }}>
                        <button onClick={() => addToCart(product)} className="btn btn-primary" style={{ flex: 1, padding: '1rem' }}>Add to Bag</button>
                        <button className="btn btn-outline" style={{ padding: '0 1.5rem' }}>Save</button>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', borderTop: '1px solid var(--border-light)', paddingTop: '2rem' }}>
                        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', color: 'var(--text-secondary)' }}>
                            <Truck size={20} /> <span>Free Shipping Worldwide</span>
                        </div>
                        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', color: 'var(--text-secondary)' }}>
                            <ShieldCheck size={20} /> <span>2 Year Warranty Included</span>
                        </div>
                    </div>
                </div>

            </div>

            {/* Recommendations */}
            <section style={{ padding: '4rem 0', borderTop: '1px solid var(--border-light)' }}>
                <div className="container">
                    <h2 className="title-font" style={{ marginBottom: '3rem' }}>You May Also Like</h2>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '2rem' }}>
                        {recs.map(p => <ProductCard key={p.id} product={p} />)}
                    </div>
                </div>
            </section>

        </div>
    );
}
