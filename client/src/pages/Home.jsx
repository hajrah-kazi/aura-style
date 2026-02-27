import React, { useEffect, useState } from 'react';
import api from '../api';
import ProductCard from '../components/ProductCard';
import { motion } from 'framer-motion';
import { ChevronRight } from 'lucide-react';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';

export default function Home() {
    const [products, setProducts] = useState([]);
    const [popular, setPopular] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [all, pop] = await Promise.all([
                    api.get('/products/'),
                    api.get('/recommendations/popular')
                ]);
                setProducts(all.data);
                setPopular(pop.data);
            } catch (e) { console.error(e); }
        };
        fetchData();
    }, []);

    return (
        <div style={{ paddingTop: 'var(--header-height)' }}>

            {/* Hero Section */}
            <section style={{
                height: '92vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                textAlign: 'center', background: 'radial-gradient(circle at center, #1a1a1a 0%, #000 100%)',
                position: 'relative', overflow: 'hidden'
            }}>
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    style={{ zIndex: 10 }}
                >
                    <h1 className="title-font" style={{ fontSize: '5rem', marginBottom: '1rem', background: 'linear-gradient(to right, #fff 0%, #aaa 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                        The Future of Luxury.
                    </h1>
                    <p style={{ fontSize: '1.5rem', maxWidth: '600px', margin: '0 auto 2.5rem', color: '#888' }}>
                        Experience the pinnacle of engineering and design. <br /> Curated just for you.
                    </p>
                    <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                        <button className="btn btn-primary" style={{ padding: '1rem 2.5rem', fontSize: '1.1rem' }}>Shop Collection</button>
                        <button className="btn btn-outline" style={{ padding: '1rem 2.5rem', fontSize: '1.1rem' }}>Learn More</button>
                    </div>
                </motion.div>

                {/* Abstract background element */}
                <div style={{
                    position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
                    width: '60vw', height: '60vw', background: 'radial-gradient(circle, rgba(59,130,246,0.15) 0%, rgba(0,0,0,0) 70%)',
                    pointerEvents: 'none'
                }} />
            </section>

            {/* Trending Carousel */}
            <section className="container" style={{ padding: '6rem 2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', marginBottom: '2rem' }}>
                    <h2 className="title-font">Trending Now</h2>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', color: 'var(--accent-primary)', cursor: 'pointer' }}>
                        View All <ChevronRight size={16} />
                    </span>
                </div>

                <Swiper
                    spaceBetween={30}
                    slidesPerView={1.2}
                    breakpoints={{
                        640: { slidesPerView: 2.2 },
                        1024: { slidesPerView: 3.2 },
                    }}
                >
                    {popular.map(p => (
                        <SwiperSlide key={p.id}>
                            <ProductCard product={p} />
                        </SwiperSlide>
                    ))}
                </Swiper>
            </section>

            {/* Grid Collection */}
            <section style={{ background: 'var(--bg-secondary)', padding: '6rem 0' }}>
                <div className="container">
                    <h2 className="title-font" style={{ textAlign: 'center', marginBottom: '4rem' }}>The Collection</h2>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '2rem' }}>
                        {products.map(p => (
                            <ProductCard key={p.id} product={p} />
                        ))}
                    </div>
                </div>
            </section>

        </div>
    );
}
