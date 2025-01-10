const API_BASE_URL = 'http://localhost:8000';

        async function addUrl() {
            const urlInput = document.getElementById('urlInput');
            const responseDiv = document.getElementById('urlResponse');
            const url = urlInput.value.trim();

            if (!url) {
                responseDiv.innerHTML = '<div class="error"><i class="fas fa-exclamation-circle"></i> Please enter a valid URL</div>';
                return;
            }

            try {
                responseDiv.innerHTML = '<div class="loading"><div class="loading-spinner"></div>Adding URL to knowledge base...</div>';
                const response = await fetch(`${API_BASE_URL}/link?url=${encodeURIComponent(url)}`, {
                    method: 'POST'
                });
                
                const data = await response.json();
                responseDiv.innerHTML = `<div class="success"><i class="fas fa-check-circle"></i> ${data.response || data}</div>`;
                urlInput.value = '';
            } catch (error) {
                responseDiv.innerHTML = `<div class="error"><i class="fas fa-exclamation-circle"></i> Error: ${error.message}</div>`;
            }
        }

        async function askQuestion() {
            const questionInput = document.getElementById('questionInput');
            const responseDiv = document.getElementById('questionResponse');
            const loadingIndicator = document.getElementById('loadingIndicator');
            const question = questionInput.value.trim();

            if (!question) {
                responseDiv.innerHTML = '<div class="error"><i class="fas fa-exclamation-circle"></i> Please enter a question</div>';
                return;
            }

            loadingIndicator.style.display = 'flex';
            responseDiv.innerHTML = '';

            try {
                const response = await fetch(`${API_BASE_URL}/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: question })
                });

                const data = await response.json();
                
                let html = `<div class="response">
                    <div><strong><i class="fas fa-question"></i> Question:</strong> ${data.question}</div>
                    <div style="margin-top: 1rem;"><strong><i class="fas fa-comment-dots"></i> Answer:</strong> ${data.answer}</div>`;
                
                if (data.documents && data.documents.length > 0) {
                    html += `<div class="documents">
                        <strong><i class="fas fa-book"></i> Source Documents:</strong>
                        <ul>`;
                    data.documents.forEach(doc => {
                        html += `<li>${doc.page_content}</li>`;
                    });
                    html += '</ul></div>';
                }

                html += '</div>';
                responseDiv.innerHTML = html;
                questionInput.value = '';
            } catch (error) {
                responseDiv.innerHTML = `<div class="error"><i class="fas fa-exclamation-circle"></i> Error: ${error.message}</div>`;
            } finally {
                loadingIndicator.style.display = 'none';
            }
        }

        // Add keyboard shortcuts
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const activeElement = document.activeElement;
                if (activeElement.id === 'urlInput') {
                    addUrl();
                } else if (activeElement.id === 'questionInput') {
                    askQuestion();
                }
            }
        });