const SENTIMENT_ENDPOINT = 'http://localhost:8089/get_emojis';


function get_emojis(text, callback) {
    fetch(SENTIMENT_ENDPOINT, {
        method: 'POST',
        body: text
    }).then(function(response) {
        console.log(response.json());
        callback(response.json());
    })
}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        get_emojis(request.text, function (emojis) {
            sendResponse({emojis: emojis});
        })
    });