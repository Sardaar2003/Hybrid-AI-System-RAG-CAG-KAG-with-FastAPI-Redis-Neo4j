// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const queryInput = document.getElementById('query-input');
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const uploadStatus = document.getElementById('upload-status');

// Handle Textarea Enter Key
queryInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Auto-resize textarea
queryInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if(this.value === '') this.style.height = 'auto';
});

// --- Chat Logic ---
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = queryInput.value.trim();
    if (!query) return;

    // Reset input
    queryInput.value = '';
    queryInput.style.height = 'auto';

    // 1. Add User Message
    addMessage(query, 'user-message');

    // 2. Add Skeleton Loader
    const typingId = addTypingSkeleton();

    try {
        // 3. Send to Backend
        const response = await fetch('/query/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        // 4. Remove Skeleton
        removeElement(typingId);

        // 5. Add AI Message
        addAIMessage(data.response, data.source);

    } catch (error) {
        console.error("Query Error:", error);
        removeElement(typingId);
        addAIMessage("Sorry, there was an error processing your request. Ensure the backend is running.", 'error');
    }
});

function addMessage(text, className) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;
    msgDiv.innerHTML = `<div class="message-content">${escapeHTML(text)}</div>`;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addAIMessage(text, source) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ai-message`;

    // Map source string to class/color and label
    let sourceClass = "source-rag";
    let sourceLabel = "RAG Pipeline";

    if (source && source.toLowerCase().includes('kag')) {
        sourceClass = "source-kag";
        sourceLabel = "KAG Pipeline";
    } else if (source && source.toLowerCase().includes('hybrid')) {
        sourceClass = "source-hybrid";
        sourceLabel = "Cached Hybrid";
    }

    const badgeHtml = source ? `<div class="source-badge ${sourceClass}"><span class="dot ${sourceClass.replace('source-', '')}"></span> ${sourceLabel}</div>` : '';

    msgDiv.innerHTML = `
        ${badgeHtml}
        <div class="message-content typing-effect"></div>
    `;
    
    chatMessages.appendChild(msgDiv);
    
    // Typewriter effect
    const contentDiv = msgDiv.querySelector('.message-content');
    let i = 0;
    const speed = 15; // ms per char
    function typeWriter() {
        if (i < text.length) {
            contentDiv.innerHTML += escapeHTML(text.charAt(i));
            i++;
            chatMessages.scrollTop = chatMessages.scrollHeight;
            setTimeout(typeWriter, speed);
        }
    }
    typeWriter();
}

function addTypingSkeleton() {
    const id = 'typing-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.id = id;
    msgDiv.className = `message ai-message`;
    msgDiv.innerHTML = `
        <div class="message-content typing-skeleton">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// --- Drag & Drop File Upload ---
dropZone.addEventListener('click', () => fileInput.click());

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evt => {
    dropZone.addEventListener(evt, preventDefaults, false);
});

function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }

['dragenter', 'dragover'].forEach(evt => dropZone.addEventListener(evt, () => dropZone.classList.add('dragover'), false));
['dragleave', 'drop'].forEach(evt => dropZone.addEventListener(evt, () => dropZone.classList.remove('dragover'), false));

dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleUpload(files[0]);
});

fileInput.addEventListener('change', function() {
    handleUpload(this.files[0]);
});

async function handleUpload(file) {
    if (!file) return;

    // Show status
    uploadStatus.className = 'status-message';
    uploadStatus.style.background = 'rgba(88, 166, 255, 0.1)';
    uploadStatus.style.color = 'var(--text-main)';
    
    uploadStatus.innerHTML = `
        <div class="status-text-row">
            Processing <span style="font-weight: 600; color: var(--rag-glow); margin: 0 4px;">${file.name}</span>... <div class="typing-dot"></div>
        </div>
        <div class="progress-bar-container">
            <div class="progress-bar-fill" id="upload-progress"></div>
        </div>
    `;

    const progressFill = document.getElementById('upload-progress');
    let progress = 0;

    // Simulate progress (asymptotically approaches 95% while uploading/extracting graphs)
    const progressInterval = setInterval(() => {
        progress += (95 - progress) * 0.05;
        if (progressFill) progressFill.style.width = `${progress}%`;
    }, 600);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/ingest/', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Snap to 100% on completion
        clearInterval(progressInterval);
        if (progressFill) progressFill.style.width = '100%';

        // Wait a brief moment to show the full bar before replacing text
        setTimeout(() => {
            uploadStatus.style.background = 'rgba(63, 185, 80, 0.1)';
            uploadStatus.style.color = 'var(--hybrid-glow)';
            uploadStatus.innerHTML = `<div class="status-text-row">✅ Successfully ingested <strong>${file.name}</strong></div>`;
            
            // Hide after 5 seconds
            setTimeout(() => uploadStatus.className = 'hidden', 5000);
        }, 600);

    } catch (error) {
        clearInterval(progressInterval);
        console.error('Upload Error:', error);
        uploadStatus.style.background = 'rgba(255, 85, 85, 0.1)';
        uploadStatus.style.color = '#ff5555';
        uploadStatus.innerHTML = `<div class="status-text-row">❌ Failed to ingest <strong>${file.name}</strong></div>`;
    }
}

function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag])
    );
}
