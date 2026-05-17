document.addEventListener('DOMContentLoaded', function() {
    const greetForm = document.getElementById('greetForm');
    
    if (greetForm) {
        greetForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const nameInput = document.getElementById('name');
            const responseDiv = document.getElementById('response');
            const responseText = document.getElementById('responseText');
            
            try {
                const response = await fetch('/api/greet', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name: nameInput.value }),
                });
                
                const data = await response.json();
                responseText.textContent = data.message;
                responseDiv.classList.remove('hidden');
            } catch (error) {
                console.error('Error:', error);
                responseText.textContent = 'An error occurred. Please try again.';
                responseDiv.classList.remove('hidden');
            }
        });
    }
});
