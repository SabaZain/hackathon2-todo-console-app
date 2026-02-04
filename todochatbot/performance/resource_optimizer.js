/**
 * Resource Optimizer for Todo AI Chatbot
 *
 * This module optimizes frontend resource usage.
 */

class ResourceOptimizer {
    constructor() {
        this.cachedElements = new Map();
        this.observer = null;
        this.resourcePool = [];
        this.performanceMetrics = {
            memoryUsage: [],
            renderTime: [],
            networkRequests: []
        };
    }

    /**
     * Optimize DOM element creation and manipulation
     */
    createElement(tag, attributes = {}, children = []) {
        // Check if element is already cached
        const cacheKey = `${tag}_${JSON.stringify(attributes)}`;
        if (this.cachedElements.has(cacheKey)) {
            return this.cachedElements.get(cacheKey);
        }

        const element = document.createElement(tag);

        // Set attributes efficiently
        Object.entries(attributes).forEach(([key, value]) => {
            if (typeof value === 'function') {
                element.addEventListener(key.slice(2).toLowerCase(), value); // onClick -> click
            } else {
                element.setAttribute(key, value);
            }
        });

        // Append children efficiently
        if (children.length > 0) {
            const fragment = document.createDocumentFragment();
            children.forEach(child => {
                if (typeof child === 'string') {
                    fragment.appendChild(document.createTextNode(child));
                } else {
                    fragment.appendChild(child);
                }
            });
            element.appendChild(fragment);
        }

        // Cache the element
        this.cachedElements.set(cacheKey, element);
        return element;
    }

    /**
     * Optimize image loading with lazy loading
     */
    loadImage(src, alt = '', className = '') {
        return new Promise((resolve, reject) => {
            const img = new Image();

            // Set up lazy loading
            img.loading = 'lazy';
            img.src = src;
            img.alt = alt;
            img.className = className;

            img.onload = () => resolve(img);
            img.onerror = () => reject(new Error(`Failed to load image: ${src}`));
        });
    }

    /**
     * Optimize CSS class toggling
     */
    toggleClass(element, className, force = undefined) {
        if (element instanceof HTMLElement) {
            if (force === undefined) {
                element.classList.toggle(className);
            } else {
                element.classList.toggle(className, force);
            }
        }
    }

    /**
     * Optimize event listener attachment with passive listeners
     */
    addOptimizedListener(element, eventType, handler, options = {}) {
        const defaultOptions = {
            passive: true,
            capture: false
        };

        const mergedOptions = { ...defaultOptions, ...options };

        element.addEventListener(eventType, handler, mergedOptions);
    }

    /**
     * Optimize rendering with virtual scrolling
     */
    createVirtualScrollContainer(items, renderItem, containerHeight = 400) {
        const container = this.createElement('div', {
            className: 'virtual-scroll-container',
            style: `height: ${containerHeight}px; overflow-y: auto; position: relative;`
        });

        // Create a fixed-size viewport
        const viewport = this.createElement('div', {
            className: 'virtual-viewport',
            style: 'position: relative;'
        });

        // Calculate visible items based on scroll position
        let startIndex = 0;
        let endIndex = Math.ceil(containerHeight / 50) + 5; // Assuming ~50px per item

        const updateViewport = () => {
            // Calculate which items should be visible
            const scrollTop = container.scrollTop;
            const itemHeight = 50; // Estimated height
            startIndex = Math.floor(scrollTop / itemHeight);
            endIndex = Math.min(startIndex + Math.ceil(containerHeight / itemHeight) + 10, items.length);

            // Clear current viewport
            viewport.innerHTML = '';

            // Add padding for scrollable area
            const spacerTop = this.createElement('div', {
                style: `height: ${startIndex * itemHeight}px;`
            });

            const spacerBottom = this.createElement('div', {
                style: `height: ${(items.length - endIndex) * itemHeight}px;`
            });

            // Add visible items
            const visibleItems = items.slice(startIndex, endIndex);
            const itemElements = visibleItems.map((item, index) =>
                renderItem(item, startIndex + index)
            );

            viewport.appendChild(spacerTop);
            itemElements.forEach(el => viewport.appendChild(el));
            viewport.appendChild(spacerBottom);
        };

        // Attach scroll listener
        this.addOptimizedListener(container, 'scroll', updateViewport);

        container.appendChild(viewport);
        updateViewport(); // Initial render

        return container;
    }

    /**
     * Optimize network requests with caching and batching
     */
    async optimizedRequest(url, options = {}) {
        const cacheKey = `${url}_${JSON.stringify(options)}`;

        // Check request cache
        if (this.cachedElements.has(cacheKey)) {
            const cached = this.cachedElements.get(cacheKey);
            const age = Date.now() - cached.timestamp;

            // Use cached response if not expired (5 minutes)
            if (age < 5 * 60 * 1000) {
                return cached.data;
            }
        }

        // Make the request
        const startTime = performance.now();
        const response = await fetch(url, options);
        const data = await response.clone().json();
        const endTime = performance.now();

        // Cache the response
        this.cachedElements.set(cacheKey, {
            data,
            timestamp: Date.now()
        });

        // Track performance
        this.performanceMetrics.networkRequests.push({
            url,
            startTime,
            endTime,
            duration: endTime - startTime,
            status: response.status
        });

        return data;
    }

    /**
     * Optimize memory usage with object pooling
     */
    borrowFromPool(type) {
        if (!this.resourcePool[type]) {
            this.resourcePool[type] = [];
        }

        if (this.resourcePool[type].length > 0) {
            return this.resourcePool[type].pop();
        }

        // Create new object if pool is empty
        switch (type) {
            case 'messageElement':
                return this.createElement('div', { className: 'chat-message' });
            case 'inputElement':
                return this.createElement('input', { type: 'text' });
            default:
                return {};
        }
    }

    returnToPool(type, object) {
        if (!this.resourcePool[type]) {
            this.resourcePool[type] = [];
        }

        // Reset object properties before returning to pool
        if (object instanceof HTMLElement) {
            object.innerHTML = '';
            object.className = '';
        }

        this.resourcePool[type].push(object);
    }

    /**
     * Optimize animations with requestAnimationFrame
     */
    animateElement(element, animationFn, duration = 300) {
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            animationFn(element, progress);

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    /**
     * Optimize form input handling with debouncing
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Optimize resize handling
     */
    handleResize(callback) {
        let resizeTimeout;

        const optimizedCallback = () => {
            if (resizeTimeout) {
                cancelAnimationFrame(resizeTimeout);
            }

            resizeTimeout = requestAnimationFrame(() => {
                callback();
            });
        };

        window.addEventListener('resize', optimizedCallback);

        return () => {
            window.removeEventListener('resize', optimizedCallback);
            if (resizeTimeout) {
                cancelAnimationFrame(resizeTimeout);
            }
        };
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return {
            ...this.performanceMetrics,
            cacheHitRate: this.calculateCacheHitRate(),
            memoryUsage: this.getMemoryUsage(),
            elementCount: this.cachedElements.size
        };
    }

    calculateCacheHitRate() {
        // Simplified calculation - in a real implementation,
        // you'd track hits vs misses
        return 0.75; // 75% cache hit rate
    }

    getMemoryUsage() {
        // In a real implementation, this would interface with browser memory APIs
        // For now, return a simulated value
        return {
            usedJSHeapSize: 50 * 1024 * 1024, // 50 MB
            totalJSHeapSize: 100 * 1024 * 1024, // 100 MB
            heapSizeLimit: 2000 * 1024 * 1024 // 2 GB
        };
    }

    /**
     * Cleanup resources
     */
    destroy() {
        // Clear all caches
        this.cachedElements.clear();

        // Cancel any ongoing observers
        if (this.observer) {
            this.observer.disconnect();
        }

        // Clear resource pools
        this.resourcePool = [];

        // Reset metrics
        this.performanceMetrics = {
            memoryUsage: [],
            renderTime: [],
            networkRequests: []
        };
    }
}

/**
 * Utility functions for resource optimization
 */
const ResourceUtils = {
    /**
     * Optimize string concatenation
     */
    joinStrings(strings, separator = '') {
        if (strings.length === 0) return '';
        if (strings.length === 1) return strings[0];

        return strings.join(separator);
    },

    /**
     * Optimize array operations
     */
    optimizedMap(array, callback) {
        const result = new Array(array.length);
        for (let i = 0; i < array.length; i++) {
            result[i] = callback(array[i], i, array);
        }
        return result;
    },

    /**
     * Optimize object creation
     */
    createShallowCopy(obj) {
        return Object.assign({}, obj);
    },

    /**
     * Optimize conditional rendering
     */
    conditionalRender(condition, trueElement, falseElement = null) {
        return condition ? trueElement : falseElement;
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ResourceOptimizer, ResourceUtils };
} else if (typeof window !== 'undefined') {
    window.ResourceOptimizer = ResourceOptimizer;
    window.ResourceUtils = ResourceUtils;
}