document.addEventListener('DOMContentLoaded', function() {
    const currentTimeBtn = document.getElementById('getCurrentTime');
    const timestampForm = document.getElementById('timestampForm');
    const datetimeForm = document.getElementById('datetimeForm');
    const urlParseForm = document.getElementById('urlParseForm');
    const urlEncodeForm = document.getElementById('urlEncodeForm');

    if (currentTimeBtn) {
        currentTimeBtn.addEventListener('click', getCurrentTime);
    }

    if (timestampForm) {
        timestampForm.addEventListener('submit', handleTimestampSubmit);
    }

    if (datetimeForm) {
        datetimeForm.addEventListener('submit', handleDatetimeSubmit);
    }

    if (urlParseForm) {
        urlParseForm.addEventListener('submit', handleUrlParse);
    }

    setupTabs();
});

function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');

            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

async function getCurrentTime() {
    try {
        const response = await fetch('/api/time/current');
        const data = await response.json();

        document.getElementById('currentTimestamp').textContent = data.timestamp;
        document.getElementById('currentDatetime').textContent = data.datetime;
        document.getElementById('currentTimeResult').classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        alert('获取当前时间失败，请重试');
    }
}

async function handleTimestampSubmit(e) {
    e.preventDefault();
    const timestamp = document.getElementById('timestampInput').value;

    try {
        const response = await fetch('/api/time/to_datetime', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ timestamp: parseInt(timestamp) })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('timestampOutput').textContent = data.datetime;
            document.getElementById('timestampResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('转换失败，请重试');
    }
}

async function handleDatetimeSubmit(e) {
    e.preventDefault();
    const datetime = document.getElementById('datetimeInput').value;

    try {
        const response = await fetch('/api/time/to_timestamp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ datetime: datetime })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('datetimeOutput').textContent = data.timestamp;
            document.getElementById('datetimeResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('转换失败，请重试');
    }
}

async function encodeBase64() {
    const input = document.getElementById('base64EncodeInput').value;

    try {
        const response = await fetch('/api/encode/base64', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('base64EncodeOutput').textContent = data.result;
            document.getElementById('base64EncodeResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('编码失败，请重试');
    }
}

async function decodeBase64() {
    const input = document.getElementById('base64DecodeInput').value;

    try {
        const response = await fetch('/api/decode/base64', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('base64DecodeOutput').textContent = data.result;
            document.getElementById('base64DecodeResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('解码失败，请重试');
    }
}

async function encodeURL() {
    const input = document.getElementById('urlEncodeInput').value;

    try {
        const response = await fetch('/api/encode/url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('urlEncodeOutput').textContent = data.result;
            document.getElementById('urlEncodeResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('编码失败，请重试');
    }
}

async function decodeURL() {
    const input = document.getElementById('urlDecodeInput').value;

    try {
        const response = await fetch('/api/decode/url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('urlDecodeOutput').textContent = data.result;
            document.getElementById('urlDecodeResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('解码失败，请重试');
    }
}

async function encodeHTML() {
    const input = document.getElementById('htmlEncodeInput').value;

    try {
        const response = await fetch('/api/encode/html', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('htmlEncodeOutput').textContent = data.result;
            document.getElementById('htmlEncodeResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('编码失败，请重试');
    }
}

async function decodeHTML() {
    const input = document.getElementById('htmlDecodeInput').value;

    try {
        const response = await fetch('/api/decode/html', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('htmlDecodeOutput').textContent = data.result;
            document.getElementById('htmlDecodeResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('解码失败，请重试');
    }
}

async function handleUrlParse(e) {
    e.preventDefault();
    const url = document.getElementById('parseUrlInput').value;

    try {
        const response = await fetch('/api/url/parse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('urlScheme').textContent = data.scheme;
            document.getElementById('urlDomain').textContent = data.netloc;
            document.getElementById('urlPath').textContent = data.path || '/';

            const paramsDiv = document.getElementById('urlParams');
            if (Object.keys(data.params).length > 0) {
                let paramsHtml = '<table class="params-table"><thead><tr><th>参数名</th><th>参数值</th></tr></thead><tbody>';
                for (const [key, value] of Object.entries(data.params)) {
                    paramsHtml += `<tr><td>${key}</td><td>${value}</td></tr>`;
                }
                paramsHtml += '</tbody></table>';
                paramsDiv.innerHTML = paramsHtml;
            } else {
                paramsDiv.innerHTML = '<p class="no-params">无参数</p>';
            }

            document.getElementById('urlParseResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('解析失败，请重试');
    }
}

async function encodeFullURL() {
    const input = document.getElementById('urlEncodeInput').value;

    try {
        const response = await fetch('/api/url/encode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: input })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('urlEncodeOutput').textContent = data.result;
            document.getElementById('urlEncodeResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('编码失败，请重试');
    }
}

async function decodeFullURL() {
    const input = document.getElementById('urlEncodeInput').value;

    try {
        const response = await fetch('/api/url/decode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: input })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('urlEncodeOutput').textContent = data.result;
            document.getElementById('urlEncodeResult').classList.remove('hidden');
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('解码失败，请重试');
    }
}

function copyResult(elementId) {
    const text = document.getElementById(elementId).textContent || document.getElementById(elementId).value;
    navigator.clipboard.writeText(text).then(() => {
        alert('已复制到剪贴板');
    }).catch(err => {
        console.error('复制失败:', err);
    });
}

async function encryptAES() {
    const text = document.getElementById('aesInput').value;
    const key = document.getElementById('aesKey').value;
    const mode = document.getElementById('aesMode').value;
    const padding = document.getElementById('aesPadding').value;
    const keySize = document.getElementById('aesKeySize').value;
    const encoding = document.getElementById('aesEncoding').value;
    const outputFormat = document.getElementById('aesFormat').value;

    try {
        const response = await fetch('/api/aes/encrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                key: key,
                mode: mode,
                padding: padding,
                key_size: keySize,
                encoding: encoding,
                output_format: outputFormat
            })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('aesOutput').value = data.result;
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('加密失败，请重试');
    }
}

async function decryptAES() {
    const text = document.getElementById('aesInput').value;
    const key = document.getElementById('aesKey').value;
    const mode = document.getElementById('aesMode').value;
    const padding = document.getElementById('aesPadding').value;
    const keySize = document.getElementById('aesKeySize').value;
    const encoding = document.getElementById('aesEncoding').value;
    const inputFormat = document.getElementById('aesFormat').value;

    try {
        const response = await fetch('/api/aes/decrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                key: key,
                mode: mode,
                padding: padding,
                key_size: keySize,
                encoding: encoding,
                input_format: inputFormat
            })
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('aesOutput').value = data.result;
        } else {
            alert('错误: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('解密失败，请重试');
    }
}

function swapAES() {
    const input = document.getElementById('aesInput');
    const output = document.getElementById('aesOutput');
    const temp = input.value;
    input.value = output.value;
    output.value = temp;
}
