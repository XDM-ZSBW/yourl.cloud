// Background service worker for Yourl.Cloud Assistant

// Listen for installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('Yourl.Cloud Assistant installed');
});

// Handle messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'getRecoveryStatus') {
    // TODO: Implement recovery status check
    sendResponse({ status: 'pending' });
  }
  return true;
});

