var emojiStrategy = {
    id: 'emoji',
    match: /(.*)/,
    search: function (term, callback) {
        callback(['1', '2', '3']);
    },
    template: function (name) {
        return name;
    },
    replace: function (name) {
        return '$1' + name + '_emoji ';
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
