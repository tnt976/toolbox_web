document.addEventListener('DOMContentLoaded', () => {
    const text1Input = document.getElementById('text1');
    const text2Input = document.getElementById('text2');
    const file1Input = document.getElementById('file1');
    const file2Input = document.getElementById('file2');
    const compareBtn = document.getElementById('compareBtn');
    const swapBtn = document.getElementById('swapBtn');
    const clearBtn = document.getElementById('clearBtn');
    const resultsSection = document.getElementById('resultsSection');
    const diff1 = document.getElementById('diff1');
    const diff2 = document.getElementById('diff2');
    const similarityValue = document.getElementById('similarityValue');
    const changesCount = document.getElementById('changesCount');
    const text1Length = document.getElementById('text1Length');
    const text2Length = document.getElementById('text2Length');
    const currentYear = document.getElementById('currentYear');

    currentYear.textContent = new Date().getFullYear();

    function readFile(input, textarea) {
        input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    textarea.value = event.target.result;
                };
                reader.readAsText(file);
            }
        });
    }

    readFile(file1Input, text1Input);
    readFile(file2Input, text2Input);

    swapBtn.addEventListener('click', () => {
        const temp = text1Input.value;
        text1Input.value = text2Input.value;
        text2Input.value = temp;
    });

    clearBtn.addEventListener('click', () => {
        text1Input.value = '';
        text2Input.value = '';
        resultsSection.style.display = 'none';
    });

    compareBtn.addEventListener('click', async () => {
        const text1 = text1Input.value;
        const text2 = text2Input.value;

        if (!text1 || !text2) {
            alert('请在两个输入框中都输入内容');
            return;
        }

        compareBtn.disabled = true;
        compareBtn.innerHTML = '<span class="btn-icon">⏳</span><span class="btn-text">对比中...</span>';

        try {
            const response = await fetch('/api/compare', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text1, text2 })
            });

            const result = await response.json();
            displayResults(result);
        } catch (error) {
            console.error('对比失败:', error);
            alert('对比失败，请重试');
        } finally {
            compareBtn.disabled = false;
            compareBtn.innerHTML = '<span class="btn-icon">↔</span><span class="btn-text">开始对比</span>';
        }
    });

    function displayResults(result) {
        resultsSection.style.display = 'block';
        similarityValue.textContent = Math.round(result.similarity * 100) + '%';
        
        const actualChanges = result.changes.filter(c => c.type !== 'equal');
        changesCount.textContent = actualChanges.length;
        text1Length.textContent = result.text1.length;
        text2Length.textContent = result.text2.length;

        diff1.innerHTML = '';
        diff2.innerHTML = '';

        let currentPos1 = 0;
        let currentPos2 = 0;

        result.changes.forEach((change) => {
            if (change.type === 'equal' || change.type === 'replace' || change.type === 'delete') {
                if (change.text1_content) {
                    const span = document.createElement('span');
                    span.textContent = change.text1_content;
                    if (change.type !== 'equal') {
                        span.className = 'diff-removed';
                    } else {
                        span.className = 'diff-equal';
                    }
                    diff1.appendChild(span);
                }
            }

            if (change.type === 'equal' || change.type === 'replace' || change.type === 'insert') {
                if (change.text2_content) {
                    const span = document.createElement('span');
                    span.textContent = change.text2_content;
                    if (change.type !== 'equal') {
                        span.className = 'diff-added';
                    } else {
                        span.className = 'diff-equal';
                    }
                    diff2.appendChild(span);
                }
            }
        });

        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
});
