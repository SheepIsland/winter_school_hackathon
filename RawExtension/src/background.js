const SENTIMENT_ENDPOINT = 'http://localhost:8089/get_emojis';


function get_emojis(text, callback) {
    fetch(SENTIMENT_ENDPOINT, {
        method: 'POST',
        body: text
    }).then(function(response) {
        return response.json();
    }).then(function(json) {
        callback(json);
    })
}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        get_emojis(request.text, function (emojis) {
            sendResponse({emojis: emojis});
        });
        return true;
    });