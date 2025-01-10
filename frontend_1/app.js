

const API_BASE_URL = 'http://localhost:8000';

        async function addUrl() {
            const urlInput = document.getElementById('urlInput');
            const responseDiv = document.getElementById('urlResponse');
            const url = urlInput.value.trim();

            if (!url) {
                responseDiv.innerHTML = '<div class="error">Please enter a valid URL</div>';
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/link?url=${encodeURIComponent(url)}`, {
                    method: 'POST'
                });
                
                const data = await response.json();
                responseDiv.innerHTML = `<div>${data.response || data}</div>`;
            } catch (error) {
                responseDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            }
        }

        async function askQuestion() {
            const questionInput = document.getElementById('questionInput');
            const responseDiv = document.getElementById('questionResponse');
            const loadingIndicator = document.getElementById('loadingIndicator');
            const question = questionInput.value.trim();

            if (!question) {
                responseDiv.innerHTML = '<div class="error">Please enter a question</div>';
                return;
            }

            loadingIndicator.style.display = 'block';
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
                
                let html = `<div><strong>Question:</strong> ${data.question}</div>
                           <div><strong>Answer:</strong> ${data.answer}</div>`;
                
                if (data.documents && data.documents.length > 0) {
                    html += '<div class="documents"><strong>Source Documents:</strong><ul>';
                    data.documents.forEach(doc => {
                        html += `<li>${doc.page_content}</li>`;
                    });
                    html += '</ul></div>';
                }

                responseDiv.innerHTML = html;
            } catch (error) {
                responseDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            } finally {
                loadingIndicator.style.display = 'none';
            }
        }