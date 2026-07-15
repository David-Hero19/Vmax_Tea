"""
Menu data for VMAX Tea & Coffee Shop.

PLACEHOLDER DATA: items, prices, and dietary tags below are samples, not
confirmed with the owner. Update this file once the real menu is
available — everything else (cart, checkout, receipts, filters) reads
from here automatically.

Prices are in Naira (whole numbers). Paystack needs amounts in kobo,
so conversion (price * 100) happens at checkout time, not here.

`dietary` is a list of tags shown as small badges, e.g. ["vegan"],
["gluten-free"], or [] if none apply.
"""

CATEGORIES = [
    {"id": "coffee", "label": "Coffee", "icon": "☕"},
    {"id": "tea", "label": "Tea", "icon": "🍃"},
    {"id": "pastries", "label": "Cakes & Pastries", "icon": "🍰"},
    {"id": "meals", "label": "Breakfast & Meals", "icon": "🍳"},
]

MENU_ITEMS = [
    # Coffee
    {"id": "c1", "category": "coffee", "name": "VMAX Signature Latte",
     "description": "Double shot, steamed milk, a whisper of cinnamon.",
     "price": 2000, "popular": True, "dietary": []},
    {"id": "c2", "category": "coffee", "name": "Classic Cappuccino",
     "description": "Rich espresso, thick foam, cocoa dust on top.",
     "price": 1800, "popular": False, "dietary": []},
    {"id": "c3", "category": "coffee", "name": "Cold Brew",
     "description": "Steeped 18 hours, smooth and never bitter.",
     "price": 2200, "popular": False, "dietary": ["vegan"]},
    {"id": "c4", "category": "coffee", "name": "Americano",
     "description": "Bold shots, hot water, nothing else needed.",
     "price": 1500, "popular": False, "dietary": ["vegan"]},
    {"id": "c5", "category": "coffee", "name": "Mocha Delight",
     "description": "Espresso, dark chocolate, whipped cream crown.",
     "price": 2300, "popular": False, "dietary": []},
    {"id": "c6", "category": "coffee", "name": "Espresso Shot",
     "description": "Small cup, big kick. For the purists.",
     "price": 1200, "popular": False, "dietary": ["vegan"]},
    # Tea
    {"id": "t1", "category": "tea", "name": "Ginger Lemongrass Tea",
     "description": "Fresh ginger, lemongrass, honey, a squeeze of lime.",
     "price": 1500, "popular": True, "dietary": ["vegan", "gluten-free"]},
    {"id": "t2", "category": "tea", "name": "Chamomile Calm",
     "description": "Whole flower chamomile, gentle and soothing.",
     "price": 1600, "popular": False, "dietary": ["vegan", "gluten-free"]},
    {"id": "t3", "category": "tea", "name": "Masala Chai",
     "description": "Black tea simmered with warm spices and milk.",
     "price": 1800, "popular": False, "dietary": ["gluten-free"]},
    {"id": "t4", "category": "tea", "name": "Hibiscus Zobo Iced Tea",
     "description": "Our house zobo, chilled, lightly sweet.",
     "price": 1500, "popular": False, "dietary": ["vegan", "gluten-free"]},
    {"id": "t5", "category": "tea", "name": "Green Tea",
     "description": "Light, grassy, and just the right kind of bitter.",
     "price": 1400, "popular": False, "dietary": ["vegan", "gluten-free"]},
    {"id": "t6", "category": "tea", "name": "Honey Lemon Tea",
     "description": "Black tea, raw honey, fresh lemon slices.",
     "price": 1600, "popular": False, "dietary": ["gluten-free"]},
    # Cakes & Pastries
    {"id": "p1", "category": "pastries", "name": "Red Velvet Slice",
     "description": "Moist layers, cream cheese frosting.",
     "price": 1800, "popular": True, "dietary": []},
    {"id": "p2", "category": "pastries", "name": "Chocolate Chip Muffin",
     "description": "Warm, buttery, loaded with chocolate chips.",
     "price": 1200, "popular": False, "dietary": []},
    {"id": "p3", "category": "pastries", "name": "Croissant",
     "description": "Flaky, buttery, baked fresh each morning.",
     "price": 1000, "popular": False, "dietary": []},
    {"id": "p4", "category": "pastries", "name": "Banana Bread Slice",
     "description": "Dense and moist, a hint of cinnamon.",
     "price": 1100, "popular": False, "dietary": []},
    {"id": "p5", "category": "pastries", "name": "Meat Pie",
     "description": "Savory pastry, seasoned minced filling.",
     "price": 900, "popular": False, "dietary": []},
    # Breakfast & Meals
    {"id": "m1", "category": "meals", "name": "VMAX Breakfast Plate",
     "description": "Eggs, toast, sausage, and fresh fruit.",
     "price": 3200, "popular": True, "dietary": []},
    {"id": "m2", "category": "meals", "name": "Avocado Toast",
     "description": "Sourdough, smashed avocado, chili flakes, lime.",
     "price": 2600, "popular": False, "dietary": ["vegan"]},
    {"id": "m3", "category": "meals", "name": "Club Sandwich",
     "description": "Chicken, egg, lettuce, tomato, toasted.",
     "price": 3000, "popular": False, "dietary": []},
    {"id": "m4", "category": "meals", "name": "Jollof Rice & Chicken",
     "description": "A local favorite, smoky jollof, grilled chicken.",
     "price": 3500, "popular": False, "dietary": ["gluten-free"]},
]


def get_item(item_id):
    return next((i for i in MENU_ITEMS if i["id"] == item_id), None)


def items_by_category(category):
    return [i for i in MENU_ITEMS if i["category"] == category]
