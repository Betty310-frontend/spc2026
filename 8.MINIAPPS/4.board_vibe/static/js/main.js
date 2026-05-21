document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const postForm = document.getElementById('post-form');
    const postTitle = document.getElementById('post-title');
    const postMessage = document.getElementById('post-message');
    const currentChar = document.getElementById('current-char');
    const titleError = document.getElementById('title-error');
    const messageError = document.getElementById('message-error');
    const btnSubmit = document.getElementById('btn-submit');
    const postsGrid = document.getElementById('posts-grid');
    const emptyState = document.getElementById('empty-state');
    const boardCount = document.getElementById('board-count');
    const toastContainer = document.getElementById('toast-container');

    // Initialize Page
    fetchPosts();

    // Event Listeners
    postForm.addEventListener('submit', handleFormSubmit);
    postMessage.addEventListener('input', updateCharCounter);
    
    // Clear errors on input
    postTitle.addEventListener('input', () => clearError(postTitle, titleError));
    postMessage.addEventListener('input', () => clearError(postMessage, messageError));

    // Update Character Counter
    function updateCharCounter() {
        const length = postMessage.value.length;
        currentChar.textContent = length;
        if (length >= 1000) {
            currentChar.style.color = 'var(--error)';
        } else {
            currentChar.style.color = 'var(--text-muted)';
        }
    }

    // Set Error Message
    function setError(inputElement, errorElement, message) {
        inputElement.parentElement.classList.add('has-error');
        errorElement.textContent = message;
        errorElement.classList.add('visible');
    }

    // Clear Error Message
    function clearError(inputElement, errorElement) {
        inputElement.parentElement.classList.remove('has-error');
        errorElement.textContent = '';
        errorElement.classList.remove('visible');
    }

    // Fetch all posts from the server
    async function fetchPosts() {
        try {
            const response = await fetch('/api/posts');
            if (!response.ok) throw new Error('게시글을 불러오는 도중 오류가 발생했습니다.');
            
            const posts = await response.ok ? await response.json() : [];
            renderPosts(posts);
        } catch (error) {
            console.error(error);
            showToast(error.message, 'error');
        }
    }

    // Render Posts in Grid
    function renderPosts(posts) {
        postsGrid.innerHTML = '';
        boardCount.textContent = `${posts.length} ${posts.length === 1 ? 'Post' : 'Posts'}`;

        if (posts.length === 0) {
            emptyState.style.display = 'flex';
            postsGrid.style.display = 'none';
            return;
        }

        emptyState.style.display = 'none';
        postsGrid.style.display = 'grid';

        posts.forEach((post, index) => {
            const card = createCardElement(post, index);
            postsGrid.appendChild(card);
        });
    }

    // Format Date string
    function formatDate(dateStr) {
        // SQLite timestamp usually returns "YYYY-MM-DD HH:MM:SS" in UTC
        // Convert to local date formatting
        try {
            const date = new Date(dateStr.replace(' ', 'T') + 'Z');
            if (isNaN(date.getTime())) return dateStr;
            
            return date.toLocaleDateString('ko-KR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (e) {
            return dateStr;
        }
    }

    // Create a Post Card Element
    function createCardElement(post, index) {
        const card = document.createElement('article');
        card.className = 'glass-card post-card';
        card.style.animation = `fade-up 0.5s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.05}s both`;
        card.dataset.id = post.id;

        card.innerHTML = `
            <div class="card-header">
                <div class="card-date">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    <span>${formatDate(post.created_at)}</span>
                </div>
                <button class="btn-delete" title="삭제하기">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                </button>
            </div>
            <div class="card-body">
                <h3 class="card-title"></h3>
                <p class="card-msg"></p>
            </div>
            <div class="card-reactions">
                <button class="reaction-btn reacted-cool" data-type="cool">
                    <span class="emoji">😎</span> Cool <span class="reaction-count">${post.vibe_cool || 0}</span>
                </button>
                <button class="reaction-btn reacted-fire" data-type="fire">
                    <span class="emoji">🔥</span> Fire <span class="reaction-count">${post.vibe_fire || 0}</span>
                </button>
                <button class="reaction-btn reacted-chill" data-type="chill">
                    <span class="emoji">☕</span> Chill <span class="reaction-count">${post.vibe_chill || 0}</span>
                </button>
            </div>
        `;

        // Safeguard against XSS injection by setting textContent safely
        card.querySelector('.card-title').textContent = post.title;
        card.querySelector('.card-msg').textContent = post.message;

        // Apply visual active feedback for non-zero counts
        if (post.vibe_cool > 0) card.querySelector('[data-type="cool"]').classList.add('active-cool');
        if (post.vibe_fire > 0) card.querySelector('[data-type="fire"]').classList.add('active-fire');
        if (post.vibe_chill > 0) card.querySelector('[data-type="chill"]').classList.add('active-chill');

        // Delete Event
        card.querySelector('.btn-delete').addEventListener('click', () => deletePost(post.id, card));

        // Reaction Events
        card.querySelectorAll('.reaction-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const vibeType = btn.dataset.type;
                handleReaction(post.id, vibeType, btn);
            });
        });

        return card;
    }

    // Handle Form Submit (Async Post insertion)
    async function handleFormSubmit(e) {
        e.preventDefault();
        
        const title = postTitle.value.trim();
        const message = postMessage.value.trim();
        let hasError = false;

        // Title Validation
        if (!title) {
            setError(postTitle, titleError, '제목을 입력해 주세요.');
            hasError = true;
        } else if (title.length > 100) {
            setError(postTitle, titleError, '제목은 100자 이내로 입력해 주세요.');
            hasError = true;
        }

        // Message Validation
        if (!message) {
            setError(postMessage, messageError, '메시지 내용을 입력해 주세요.');
            hasError = true;
        } else if (message.length > 1000) {
            setError(postMessage, messageError, '메시지는 1000자 이내로 입력해 주세요.');
            hasError = true;
        }

        if (hasError) return;

        // Loading state
        btnSubmit.disabled = true;
        btnSubmit.classList.add('loading');
        btnSubmit.querySelector('span').textContent = '등록하는 중...';

        try {
            const response = await fetch('/api/posts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, message })
            });

            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || '등록 중 오류가 발생했습니다.');
            }

            // Success
            showToast('성공적으로 새로운 Vibe가 등록되었습니다! ✨', 'success');
            
            // Clear inputs
            postTitle.value = '';
            postMessage.value = '';
            updateCharCounter();

            // Refresh feed
            await fetchPosts();
        } catch (error) {
            console.error(error);
            showToast(error.message, 'error');
        } finally {
            // Restore button state
            btnSubmit.disabled = false;
            btnSubmit.classList.remove('loading');
            btnSubmit.querySelector('span').textContent = 'Vibe 등록하기';
        }
    }

    // Handle Reaction Increments
    async function handleReaction(postId, vibeType, buttonElement) {
        try {
            const response = await fetch(`/api/posts/${postId}/react`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ vibe_type: vibeType })
            });

            if (!response.ok) throw new Error('반응을 추가할 수 없습니다.');

            const updatedVibes = await response.json();
            
            // Update UI count
            const countSpan = buttonElement.querySelector('.reaction-count');
            countSpan.textContent = updatedVibes[`vibe_${vibeType}`];
            
            // Toggle highlight styling
            buttonElement.classList.add(`active-${vibeType}`);
            
            // Add subtle pulse micro-animation
            buttonElement.style.transform = 'scale(1.2)';
            setTimeout(() => {
                buttonElement.style.transform = '';
            }, 150);

        } catch (error) {
            console.error(error);
            showToast(error.message, 'error');
        }
    }

    // Handle Post Deletion
    async function deletePost(postId, cardElement) {
        if (!confirm('정말로 이 감성 글을 삭제하시겠습니까?')) return;

        try {
            const response = await fetch(`/api/posts/${postId}`, {
                method: 'DELETE'
            });

            if (!response.ok) throw new Error('게시글 삭제에 실패했습니다.');

            // Smooth exit transition
            cardElement.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 1, 1)';
            cardElement.style.transform = 'scale(0.8) translateY(20px)';
            cardElement.style.opacity = '0';
            
            setTimeout(() => {
                cardElement.remove();
                
                // Recalculate board count and handle empty state
                const remainingCards = postsGrid.querySelectorAll('.post-card');
                boardCount.textContent = `${remainingCards.length} ${remainingCards.length === 1 ? 'Post' : 'Posts'}`;
                
                if (remainingCards.length === 0) {
                    emptyState.style.display = 'flex';
                    postsGrid.style.display = 'none';
                }
            }, 400);

            showToast('감성 글이 성공적으로 제거되었습니다.', 'success');
        } catch (error) {
            console.error(error);
            showToast(error.message, 'error');
        }
    }

    // Utility: Show Custom Notification Toast
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        let icon = '';
        if (type === 'success') {
            icon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`;
        } else {
            icon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;
        }

        toast.innerHTML = `${icon}<span>${message}</span>`;
        toastContainer.appendChild(toast);

        // Remove toast automatically
        setTimeout(() => {
            toast.style.transition = 'all 0.3s ease-out';
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3500);
    }
});
