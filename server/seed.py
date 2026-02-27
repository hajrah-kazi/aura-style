from app.core.database import SessionLocal, engine, Base
from app.models.models import User, Product, Interaction
from app.routers.auth import get_password_hash
import random

def seed_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Seeding Users...")
    users = [
        User(email="test@example.com", full_name="Test User", hashed_password=get_password_hash("password123")),
        User(email="jane@doe.com", full_name="Jane Doe", hashed_password=get_password_hash("jane123")),
        User(email="bob@smith.com", full_name="Bob Smith", hashed_password=get_password_hash("bob123")),
    ]
    db.add_all(users)
    db.commit()

    print("Seeding Products...")
    categories = [
        ("Electronics", ["Wireless Headphones", "Smartwatch Pro", "Mechanical Keyboard", "Gaming Mouse", "Noise Cancelling Earbuds"]),
        ("Fashion", ["Classic Denim Jacket", "Canvas Sneakers", "Leather Wallet", "Cotton Hoodie", "Wristwatch Minimalist"]),
        ("Home & Living", ["Weighted Blanket", "Desk Lamp LED", "Ceramic Coffee Mug", "Succulent Set", "Aroma Diffuser"]),
        ("Fitness", ["Yoga Mat", "Dumbbell Set 10kg", "Resistance Bands", "Foam Roller", "Protein Shaker"]),
    ]
    
    # Image mapping for categories
    category_images = {
        "Electronics": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80", # Headphones
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80", # Watch
            "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80", # Keyboard
            "https://images.unsplash.com/photo-1527866959252-deab85ef7d1b?w=800&q=80", # Mouse
            "https://images.unsplash.com/photo-1588333234836-1e9619c95d90?w=800&q=80"  # Earbuds
        ],
        "Fashion": [
            "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=800&q=80", # Jacket
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80", # Sneakers
            "https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&q=80", # Wallet
            "https://images.unsplash.com/photo-1556821810-ac1b45574471?w=800&q=80", # Hoodie
            "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=800&q=80"  # Watch
        ],
        "Home & Living": [
            "https://images.unsplash.com/photo-1580302200322-959cde116f64?w=800&q=80", # Blanket
            "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80", # Lamp
            "https://images.unsplash.com/photo-1517256011271-bfbd70416a9a?w=800&q=80", # Mug
            "https://images.unsplash.com/photo-1485955900106-19d1cb7a4628?w=800&q=80", # Succulent
            "https://images.unsplash.com/photo-1602928321679-560bb453f190?w=800&q=80"  # Diffuser
        ],
        "Fitness": [
            "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&q=80", # Yoga Mat
            "https://images.unsplash.com/photo-1583454110551-21f2fa2ec617?w=800&q=80", # Dumbbell
            "https://images.unsplash.com/photo-1598289431512-b97b0917a63e?w=800&q=80", # Bands
            "https://images.unsplash.com/photo-1591171889500-2f16b229712a?w=800&q=80", # Roller
            "https://images.unsplash.com/photo-1593079831268-3381b0fdb527?w=800&q=80"  # Shaker
        ]
    }
    
    products = []
    adjectives = ["Premium", "Ultra", "Lite", "Essential", "Modern", "Sleek", "Classic"]
    
    for cat_name, items in categories:
        for idx, item in enumerate(items):
            # Pick image based on index to ensure variety or fallback to random
            img_list = category_images.get(cat_name, ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80"])
            p_img = img_list[idx % len(img_list)]
            
            p = Product(
                name=f"{random.choice(adjectives)} {item}",
                description=f"High quality {item} from our latest collection. Perfect for daily use and designed for durability in the {cat_name} category.",
                category=cat_name,
                price=round(random.uniform(19.99, 199.99), 2),
                rating=round(random.uniform(3.5, 5.0), 1),
                stock_count=random.randint(5, 50),
                brand="AuraStyle",
                tags=f"{cat_name.lower()}, {item.lower().replace(' ', ', ')}, premium",
                image_url=p_img
            )
            products.append(p)
    
    db.add_all(products)
    db.commit()

    print("Seeding Interactions (to warm up CF model)...")
    all_users = db.query(User).all()
    all_products = db.query(Product).all()
    
    for user in all_users:
        # Each user likes 2-3 specific categories
        fav_cats = random.sample([c[0] for c in categories], 2)
        liked_products = [p for p in all_products if p.category in fav_cats]
        
        # Add 5-10 interactions per user
        for _ in range(random.randint(5, 10)):
            p = random.choice(liked_products)
            inter = Interaction(
                user_id=user.id,
                product_id=p.id,
                interaction_type=random.choice(["view", "view", "view", "click", "cart"]),
                value=random.uniform(1.0, 5.0)
            )
            db.add(inter)
            
    db.commit()
    db.close()
    print("Seeding Complete!")

if __name__ == "__main__":
    seed_data()
