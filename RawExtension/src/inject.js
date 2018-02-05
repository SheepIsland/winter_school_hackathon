function ready() {
    $('div[contenteditable="true"], input[type=text], input[type=search], textarea').textcomplete(
        [{
            id: 'emoji',
            index: 1,
            match: /(.*)/,
            search: function (term, callback) {
                chrome.runtime.sendMessage({text: term}, function(response) {
                    callback(response.emojis)
                });
            },
            template: function (emoji) {
                return emoji;
            },
            replace: function (value) {
                return '$1' + ' ' + value + ' ';
            }
        }], {
            dropdownClassName: 'textcomplete-dropdown',
            maxCount: 2,
            debounce: 400,
            zIndex: '999999'
        });
}


chrome.extension.sendMessage({}, function(response) {
	var readyStateCheckInterval = setInterval(function() {
        if (document.readyState === "complete") {
            clearInterval(readyStateCheckInterval);
            ready();
        }
	}, 10);
});
