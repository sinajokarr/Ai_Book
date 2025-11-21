/**
 * * =================================================================
 * 1. PRODUCT DATA (Hardcoded for demonstration)
 * -----------------------------------------------------------------
 * This object holds all the product data required by the StoreManager
 * to process cart additions, search, and filtering.
 * =================================================================
 * */

const products = {
    // === Courses from courses_page.html ===
    "1": {
        id: "1",
        title: "ChatGPT Enterprise Mastery",
        price: 149.00,
        category: 1, // AI Engineering
        keywords: "AI, ChatGPT, Prompt Engineering, Business, Advanced",
        element: null // Placeholder for the actual DOM element
    },
    "2": {
        id: "2",
        title: "Midjourney V6: The Visual Architect",
        price: 99.00,
        category: 1, // AI Engineering
        keywords: "Midjourney, Design, Visuals, Creative, UI/UX",
        element: null
    },
    "3": {
        id: "3",
        title: "Python for Business Automation",
        price: 199.00,
        category: 1, // AI Engineering
        keywords: "Python, Automation, Backend, Coding, Data",
        element: null
    },
    "4": {
        id: "4",
        title: "Blessing of the Energy Centers",
        price: 35.00,
        category: 2, // Meditation & Energy
        keywords: "Meditation, Energy, Alignment, Dispenza, Guided",
        element: null
    },
    "5": {
        id: "5",
        title: "Subconscious Reprogramming",
        price: 59.00,
        category: 2, // Meditation & Energy
        keywords: "Mind, Reprogramming, Sleep, Theta, Wellness",
        element: null
    },
    
    // === Books/Static Products from books_page.html ===
    "10": {
        id: "10",
        title: "Deep Quantum Practice",
        price: 39.00,
        category: 2, // Meditation & Energy
        keywords: "Quantum, Meditation, Dispenza, Neuroscience",
        element: null
    },
    "11": {
        id: "11",
        title: "Spiritual Discipline",
        price: 29.00,
        category: 2, // Meditation & Energy
        keywords: "High Performance, Routine, Zen, Discipline",
        element: null
    },
    "12": {
        id: "12",
        title: "Energy Kebab for Entrepreneurs",
        price: 24.00,
        category: 3, // Mindset & Books
        keywords: "Strategy, Motivation, Entrepreneurship, Mindset",
        element: null
    },
    "13": {
        id: "13",
        title: "AI Playbook for Business",
        price: 34.00,
        category: 1, // AI Engineering
        keywords: "AI, ChatGPT, Guide, Automation, Business",
        element: null
    },
    "14": {
        id: "14",
        title: "Calm Money for Creators",
        price: 31.00,
        category: 3, // Mindset & Books
        keywords: "Finance, Wealth, Mindset, Creators, Handbook",
        element: null
    },
    
    // === Books from the general category (if any more static books exist) ===
    "15": {
        id: "15",
        title: "Atomic Habits",
        price: 18.50,
        category: 3,
        keywords: "System, Productivity, Habits",
        element: null
    },
    "16": {
        id: "16",
        title: "The 5 AM Club",
        price: 22.00,
        category: 3,
        keywords: "Routine, Mastery, Productivity",
        element: null
    },
    "17": {
        id: "17",
        title: "Psycho-Cybernetics",
        price: 16.99,
        category: 3,
        keywords: "Classic, Self-Image, Mindset",
        element: null
    }
};


/**
 * * =================================================================
 * 2. StoreManager Class
 * -----------------------------------------------------------------
 * Manages the core functionality: Search, Filter, and Cart.
 * =================================================================
 * */
class StoreManager {
    constructor(products) {
        // Now, the class receives and uses the defined products object
        this.products = products; 
        this.cart = this.loadCart();
        
        // DOM Elements
        this.gridContainer = document.getElementById('courses-grid');
        this.searchInput = document.getElementById('search-input');
        this.categorySelect = document.getElementById('category-select');
        this.loadingMessage = document.getElementById('courses-loading');
        this.errorMessage = document.getElementById('courses-error');
        this.emptyMessage = document.getElementById('courses-empty');
        this.cartCountElement = document.getElementById('cart-item-count');

        this.init();
    }

    // --- (The rest of the methods like init, loadCart, saveCart, etc. remain the same) ---
    
    init() {
        this.setupEventListeners();
        this.renderInitialProducts();
        this.updateCartDisplay();
    }

    // --- CART METHODS ---
    loadCart() {
        try {
            const cartString = localStorage.getItem('AICart');
            return cartString ? JSON.parse(cartString) : {};
        } catch (e) {
            console.error("Error loading cart from storage:", e);
            return {};
        }
    }

    saveCart() {
        localStorage.setItem('AICart', JSON.stringify(this.cart));
    }

    updateCartDisplay() {
        const totalItems = Object.values(this.cart).reduce((sum, item) => sum + item.quantity, 0);
        
        if (this.cartCountElement) {
            this.cartCountElement.textContent = totalItems;
            this.cartCountElement.hidden = totalItems === 0;
        }
    }
    
    addToCart(productId) {
        if (!this.products[productId]) {
            console.error(`Product with ID ${productId} not found.`);
            return;
        }

        const product = this.products[productId];

        if (this.cart[productId]) {
            this.cart[productId].quantity += 1;
        } else {
            this.cart[productId] = {
                id: productId,
                title: product.title,
                price: product.price,
                quantity: 1
            };
        }
        
        this.saveCart();
        this.updateCartDisplay();
        this.showToastNotification(product.title);
    }

    // Simple visual feedback for cart action
    showToastNotification(productTitle) {
        const toast = document.createElement('div');
        toast.textContent = `✅ "${productTitle}" Added to Library.`;
        toast.className = 'cart-toast';
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 10); // Start transition

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 500);
        }, 2000);
    }
    
    // --- EVENT HANDLERS ---
    setupEventListeners() {
        // Event for "Add to Cart" buttons
        document.addEventListener('click', (e) => {
            const button = e.target.closest('.js-add-cart');
            if (button) {
                // Find the nearest parent product card
                const card = button.closest('[data-product-id]');
                if (card) {
                    const productId = card.getAttribute('data-product-id');
                    this.addToCart(productId);
                }
            }
        });
        
        // Only setup search/filter listeners if the elements exist (i.e., we are on the courses page)
        if (this.searchInput && this.categorySelect) {
            this.searchInput.addEventListener('input', () => this.filterAndRender());
            this.categorySelect.addEventListener('change', () => this.filterAndRender());
        }
        
        // Add listener for cart icon click (Simple alert for this demo)
        const cartIcon = document.getElementById('cart-icon-container');
        if (cartIcon) {
             cartIcon.addEventListener('click', () => this.displayCartContents());
        }
    }

    displayCartContents() {
        let content = "🛒 Your Library Cart:\n\n";
        let total = 0;
        let count = 0;

        for (const id in this.cart) {
            const item = this.cart[id];
            content += `${item.quantity}x - ${item.title} ($${(item.price * item.quantity).toFixed(2)})\n`;
            total += item.price * item.quantity;
            count += item.quantity;
        }

        if (count === 0) {
            alert("Your Library is empty. Time to Architect!");
        } else {
            content += `\nTotal Items: ${count}\nTotal Price: $${total.toFixed(2)}`;
            alert(content);
        }
    }


    // --- RENDERING & FILTERING (Only for courses_page.html) ---
    renderInitialProducts() {
        // Only run rendering if the grid container exists (i.e., on the courses page)
        if (this.gridContainer) {
            this.loadingMessage.hidden = true; // Stop loading spinner
            this.renderProducts(Object.values(this.products).filter(p => p.category !== 3)); // Show only courses initially
        }
        // For other pages (like books_page.html), the products are static HTML and not rendered here.
    }
    
    filterAndRender() {
        const query = this.searchInput.value.toLowerCase();
        const categoryId = this.categorySelect.value;
        const filteredProducts = [];
        
        for (const id in this.products) {
            const product = this.products[id];
            
            // Exclude static books from dynamic rendering grid (they are on the books page)
            if (product.category === 3) continue;

            // 1. Category Filter
            const categoryMatch = categoryId === "" || product.category.toString() === categoryId;

            // 2. Search Query Filter (Title, Keywords)
            const queryMatch = product.title.toLowerCase().includes(query) || product.keywords.toLowerCase().includes(query);

            if (categoryMatch && queryMatch) {
                filteredProducts.push(product);
            }
        }
        
        this.renderProducts(filteredProducts);
    }
    
    renderProducts(productsToRender) {
        if (!this.gridContainer) return;

        this.gridContainer.innerHTML = '';
        this.emptyMessage.hidden = productsToRender.length > 0;
        
        productsToRender.forEach(product => {
            const cardHtml = this.createCardHtml(product);
            this.gridContainer.insertAdjacentHTML('beforeend', cardHtml);
        });

        // Re-assign product elements after rendering for JS effects (if any)
        productsToRender.forEach(product => {
            product.element = document.querySelector(`[data-product-id="${product.id}"]`);
            this.products[product.id] = product; // Update in the main object
        });
    }

    createCardHtml(product) {
        // --- Helper function to determine badge and glow color based on Category ID
        let badgeType = '';
        let glowColor = '';
        let imageName = 'default-course.jpg'; 
        let metaInfo = '';
        let description = 'Deep dive curriculum.';

        
        if (product.category === 1) { // AI Engineering
            badgeType = 'AI Track';
            glowColor = '#3b82f6'; // Blue
            
            // --- ارجاع تصاویر بر اساس ID محصول ---
            if (product.id === "1") {
                imageName = 'course-chatgpt.jpg'; 
                metaInfo = '15 Hours • Advanced';
                description = 'Move beyond basic prompts. Learn "Chain of Thought" reasoning, building custom GPTs, and automating client communication using the OpenAI API.';
            }
            if (product.id === "2") {
                imageName = 'course-midjourney.jpg'; 
                metaInfo = '8 Hours • Creative';
                description = 'Create award-winning brand assets, UI mockups, and hyper-realistic photography. Master parameters like --stylize, --weird, and multi-prompting.';
            }
            if (product.id === "3") {
                imageName = 'course-python.jpg'; 
                metaInfo = '22 Hours • Backend';
                description = 'Don\'t just use tools, build them. Learn to script simple bots that scrape data, send emails, and connect APIs to save you 20+ hours a week.';
            }

        } else if (product.category === 2) { // Meditation & Energy
            badgeType = 'Energy';
            glowColor = '#10b981'; // Green

            if (product.id === "4") {
                imageName = 'meditation-blessing.jpg';
                metaInfo = 'Guided • Dispenza Style';
                description = 'A powerful method to unstuck energy from the lower 3 centers (survival) and move it to the heart and brain for elevated consciousness.';
            }
            if (product.id === "5") {
                imageName = 'meditation-subconscious.jpg';
                metaInfo = 'Nightly • Sleep Learning';
                description = 'Bypass the analytical mind. Use the theta state just before sleep to install new beliefs about wealth, capability, and health.';
            }
        }
        
        // --- ارجاع تصاویر برای کتاب‌های استاتیک ---
        if (product.category === 3) {
             badgeType = 'Mindset';
             glowColor = '#f59e0b'; // Amber
             if (product.id === "12") imageName = 'book-kebab.jpg';
             if (product.id === "14") imageName = 'book-calmmoney.jpg';
             if (product.id === "15") imageName = 'book-atomic.jpg';
             if (product.id === "16") imageName = 'book-5amclub.jpg';
             if (product.id === "17") imageName = 'book-psycho.jpg';
        }


        // --- Construct the HTML
        const buttonText = product.category === 2 ? 'Start Journey' : 'Join Course';
        
        // 🚀 اصلاح نهایی: استفاده صحیح از STATIC_IMAGE_URL_BASE (که در HTML تعریف شده)
        const imageUrl = STATIC_IMAGE_URL_BASE + imageName;
        
        // استایل اینلاین برای اعمال تصویر به عنوان پس زمینه
        const imageStyle = `background-image: url('${imageUrl}');`;


        return `
            <article class="course-card" data-product-id="${product.id}" style="--glow-color: ${glowColor};">
                <div class="course-card__image-wrapper" style="${imageStyle}">
                    <div class="course-card__badge-group">
                        <span class="course-card__badge course-card__badge--track">${badgeType}</span>
                        <span class="course-card__badge course-card__badge--type">${product.keywords.split(',')[0].trim()}</span>
                    </div>
                </div>
                <div class="course-card__body">
                    <h3 class="course-card__title">${product.title}</h3>
                    <div class="course-card__meta">${metaInfo}</div>
                    <p class="course-card__description">${description}</p>
                </div>
                <div class="course-card__bottom">
                    <span class="course-card__price-main">$${product.price.toFixed(2)}</span>
                    <button class="btn btn--primary js-add-cart">${buttonText}</button>
                </div>
            </article>
        `;
    }
}

/**
 * * =================================================================
 * 3. Initialization
 * -----------------------------------------------------------------
 * Create the StoreManager instance and apply global styles
 * =================================================================
 * */
document.addEventListener('DOMContentLoaded', () => {
    // Pass the products object to the StoreManager
    window.storeManager = new StoreManager(products); 

    // Inject necessary CSS for the Cart Toast (simple notification)
    const style = document.createElement('style');
    style.textContent = `
        .cart-toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #10b981;
            color: #fff;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            font-size: 0.9rem;
            opacity: 0;
            transform: translateY(100px);
            transition: opacity 0.5s ease, transform 0.5s ease;
            z-index: 1000;
        }
        .cart-toast.show {
            opacity: 1;
            transform: translateY(0);
        }
    `;
    document.head.appendChild(style);
});