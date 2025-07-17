/**
 * Loading Components and Page Transition Utilities
 * 
 * This script handles loading states, page transitions, and UI feedback
 * for the NCM Enricher application.
 */

// Loading Overlay Management
class LoadingManager {
  constructor() {
    this.overlayId = 'loading-overlay';
    this.progressBarId = 'progress-bar';
    this.initialized = false;
    this.init();
  }

  init() {
    if (this.initialized) return;
    
    // Create loading overlay if not exists
    if (!document.getElementById(this.overlayId)) {
      const overlay = document.createElement('div');
      overlay.id = this.overlayId;
      overlay.className = 'loading-overlay';
      overlay.innerHTML = `
        <div class="loading-content">
          <div class="spinner"></div>
          <div class="loading-text">Carregando dados...</div>
        </div>
      `;
      document.body.appendChild(overlay);
    }
    
    // Create progress bar if not exists
    if (!document.getElementById(this.progressBarId)) {
      const progressBar = document.createElement('div');
      progressBar.id = this.progressBarId;
      progressBar.className = 'progress-bar';
      progressBar.innerHTML = '<div class="progress-bar-value"></div>';
      document.body.appendChild(progressBar);
    }
    
    // Setup link interception for page transitions
    this.setupLinkInterception();
    
    this.initialized = true;
  }

  setupLinkInterception() {
    // Intercept all internal links to show loading state
    document.addEventListener('click', (e) => {
      // Find closest anchor element
      const link = e.target.closest('a');
      
      if (link && this.isInternalLink(link)) {
        // Only handle links without target="_blank" and that don't have a download attribute
        if (!link.target && !link.hasAttribute('download') && !link.hasAttribute('data-no-loading')) {
          // Show loading state
          this.showLoading();
          
          // Allow default behavior to navigate
        }
      }
    });
    
    // Handle form submissions
    document.addEventListener('submit', (e) => {
      const form = e.target;
      
      // Only handle forms that are internal (not going to external URLs)
      if (!form.hasAttribute('data-no-loading')) {
        // Show loading state
        this.showLoading();
        
        // Allow default behavior to submit
      }
    });
  }

  isInternalLink(link) {
    // Check if the link is to the same origin
    if (!link.href) return false;
    
    try {
      const url = new URL(link.href);
      return url.origin === window.location.origin;
    } catch (e) {
      return true; // If URL parsing fails, assume it's internal
    }
  }

  showLoading() {
    const overlay = document.getElementById(this.overlayId);
    if (overlay) {
      overlay.classList.add('active');
    }
    
    const progressBar = document.getElementById(this.progressBarId);
    if (progressBar) {
      progressBar.style.display = 'block';
    }
  }

  hideLoading() {
    const overlay = document.getElementById(this.overlayId);
    if (overlay) {
      overlay.classList.remove('active');
    }
    
    const progressBar = document.getElementById(this.progressBarId);
    if (progressBar) {
      progressBar.style.display = 'none';
    }
  }
}

// Shimmer placeholder generator
class ShimmerPlaceholders {
  /**
   * Create shimmer placeholder for search results
   * @param {HTMLElement} container - The container to add the placeholders to
   * @param {number} rows - Number of result rows to simulate
   */
  static createSearchResults(container, rows = 5) {
    container.innerHTML = '';
    container.classList.add('search-results-shimmer');
    
    // Create header shimmer
    const header = document.createElement('div');
    header.className = 'shimmer shimmer-header';
    container.appendChild(header);
    
    // Create table header shimmer
    const tableHeader = document.createElement('div');
    tableHeader.className = 'shimmer-table-header';
    for (let i = 0; i < 5; i++) {
      const cell = document.createElement('div');
      cell.className = 'shimmer shimmer-table-cell';
      tableHeader.appendChild(cell);
    }
    container.appendChild(tableHeader);
    
    // Create rows
    for (let i = 0; i < rows; i++) {
      const row = document.createElement('div');
      row.className = 'shimmer-table-row';
      
      for (let j = 0; j < 5; j++) {
        const cell = document.createElement('div');
        cell.className = 'shimmer shimmer-table-cell';
        row.appendChild(cell);
      }
      
      container.appendChild(row);
    }
  }
  
  /**
   * Create shimmer placeholder for any content based on a template
   * @param {string} template - HTML string with shimmer-* classes
   * @param {HTMLElement} container - The container to add the placeholder to
   */
  static createCustom(template, container) {
    container.innerHTML = template;
  }
}

// Page transition effects
class PageTransitions {
  /**
   * Apply a fade-in effect to elements
   * @param {string} selector - CSS selector for target elements
   */
  static fadeIn(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      el.classList.add('fade-in');
      el.addEventListener('animationend', () => {
        el.classList.remove('fade-in');
      }, { once: true });
    });
  }
  
  /**
   * Apply a slide-in effect to elements
   * @param {string} selector - CSS selector for target elements
   */
  static slideIn(selector) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      el.classList.add('slide-in');
      el.addEventListener('animationend', () => {
        el.classList.remove('slide-in');
      }, { once: true });
    });
  }
  
  /**
   * Apply staggered animation to a list of elements
   * @param {string} selector - CSS selector for target elements
   * @param {string} animationClass - CSS animation class to apply
   * @param {number} delayMs - Delay between each element animation in milliseconds
   */
  static stagger(selector, animationClass, delayMs = 50) {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, index) => {
      setTimeout(() => {
        el.classList.add(animationClass);
        el.addEventListener('animationend', () => {
          el.classList.remove(animationClass);
        }, { once: true });
      }, index * delayMs);
    });
  }
}

// Make classes available globally
window.PageTransitions = PageTransitions;
window.ShimmerPlaceholders = ShimmerPlaceholders;

// Initialize loading manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.loadingManager = new LoadingManager();
  
  // Hide loading when page is loaded
  window.addEventListener('load', () => {
    if (window.loadingManager) {
      window.loadingManager.hideLoading();
    }
  });
  
  // Apply animations to search results if they exist
  if (document.querySelector('.search-results')) {
    if (window.PageTransitions) {
      window.PageTransitions.fadeIn('.search-results');
      window.PageTransitions.stagger('.search-results tbody tr', 'slide-in', 30);
    }
  }
  
  // Handle back button navigation
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
      // Page was loaded from cache (back/forward navigation)
      if (window.loadingManager) {
        window.loadingManager.hideLoading();
      }
    }
  });
});