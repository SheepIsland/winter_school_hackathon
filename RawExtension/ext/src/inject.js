var emojiStrategy = {
    id: 'emoji',
    match: /(.*)/,
    search: function (term, callback) {
        chrome.extension.sendMessage({text: term}, function(response) {
            callback(response.emojis)
        });
    },
    template: function (name) {
        return name;
    },
    replace: function (name) {
        return '$1' + ' ' + name + ' ';
    }
};


function register(el) {
    var editor = new Textcomplete.editors.Textarea(el);

    var textcomplete = new Textcomplete(editor, {
        dropdown: {
            maxCount: 5
        }
    });
    textcomplete.register([emojiStrategy]);
}


function ready() {
    jQuery('input, textarea').each(function(i, el) {register(el);});
}


chrome.extension.sendMessage({}, function(response) {
	var readyStateCheckInterval = setInterval(function() {
        if (document.readyState === "complete") {
            clearInterval(readyStateCheckInterval);
            ready();
        }
	}, 10);
});
