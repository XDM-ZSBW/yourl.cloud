// Popup script for Yourl.Cloud Assistant

document.addEventListener('DOMContentLoaded', () => {
  const copyCodeBtn = document.getElementById('copyCode');
  const recoverCodeBtn = document.getElementById('recoverCode');
  const goToHomeBtn = document.getElementById('goToHome');
  const codeSection = document.getElementById('codeSection');
  const currentCodeElement = document.getElementById('currentCode');
  const recoveryStatus = document.getElementById('recoveryStatus');

  // Handle code recovery
  recoverCodeBtn.addEventListener('click', async () => {
    try {
      const response = await fetch('https://yourl.cloud/recover', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          recovery_method: 'auto'
        })
      });

      const data = await response.json();
      
      if (data.success) {
        codeSection.style.display = 'block';
        currentCodeElement.textContent = data.suggested_code;
        showStatus('success', 'Code recovered successfully!');
      } else {
        showStatus('error', data.message || 'Recovery failed. Please try again.');
      }
    } catch (error) {
      showStatus('error', 'Failed to connect to Yourl.Cloud. Please try again.');
      console.error('Recovery error:', error);
    }
  });

  // Handle code copying (respecting organization clipboard policies)
  copyCodeBtn.addEventListener('click', async () => {
    const code = currentCodeElement.textContent;
    try {
      // Use the newer Clipboard API with fallback
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(code);
        showStatus('success', 'Code copied to clipboard!');
      } else {
        // Fallback for when Clipboard API is not available
        const textArea = document.createElement('textarea');
        textArea.value = code;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
          document.execCommand('copy');
          showStatus('success', 'Code copied to clipboard!');
        } catch (error) {
          showStatus('error', 'Failed to copy code. Please copy manually.');
        } finally {
          textArea.remove();
        }
      }
    } catch (error) {
      showStatus('error', 'Failed to copy code. Please copy manually.');
      console.error('Copy error:', error);
    }
  });

  // Navigate to Yourl.Cloud
  goToHomeBtn.addEventListener('click', () => {
    chrome.tabs.create({ url: 'https://yourl.cloud' });
  });

  // Helper function to show status messages
  function showStatus(type, message) {
    recoveryStatus.textContent = message;
    recoveryStatus.className = `status ${type}`;
    recoveryStatus.style.display = 'block';
    
    // Hide status after 3 seconds
    setTimeout(() => {
      recoveryStatus.style.display = 'none';
    }, 3000);
  }
});

