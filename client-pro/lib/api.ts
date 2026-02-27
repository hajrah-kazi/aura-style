import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

// Add interceptor for auth
api.interceptors.request.use((config) => {
    if (typeof window !== 'undefined') {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
    }
    return config;
});

export const getProducts = () => api.get('/products');
export const getProduct = (id: number) => api.get(`/products/${id}`);
export const getTrending = () => api.get('/recommendations/trending');
export const getPersonalized = () => api.get('/recommendations/personalized');
export const getSimilar = (id: number) => api.get(`/recommendations/similar/${id}`);
export const loginUser = (data: FormData) => api.post('/auth/login', data);
export const registerUser = (data: any) => api.post('/auth/register', data);
export const trackInteraction = (pid: number, type: string) => api.post(`/products/${pid}/interact`, { product_id: pid, interaction_type: type });

export default api;
