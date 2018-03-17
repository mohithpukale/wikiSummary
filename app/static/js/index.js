
//adjust footer bottom
function ct() {
	return document.compatMode == "BackCompat" ? document.body.clientHeight : document.documentElement.clientHeight;
}
var f = document.getElementById('footer');
(window.onresize = function () {
		f.style.position = document.body.scrollHeight > ct() ? '' : 'absolute';
})();

// search event
	// click search btn
$('#searchBtn').click(function() {
    searchES()
});

$('#searchBtn2').click(function () {
    searchSolr()
});
	// press enter
$('#inputField').keydown(function(e){
	if (e.keyCode == 13) {
        searchES()
	}
});

// go backend to search
function searchES() {
	var q = $('#inputField').val();
	if (q == "" || q == null || q == undefined) {
		location.href='/';
	} else {
		//parse special char
		var  entry = { "'": "&apos;", '"': '&quot;', '<': '&lt;', '>': '&gt;' };
		q = q.replace(/(['")-><&\\\/\.])/g, function ($0) { return entry[$0] || $0; });

        var string = '/query/es?q=' + q;
		location.href = string;
	};

}

function searchSolr() {
    var q = $('#inputField').val();
    if (q == "" || q == null || q == undefined) {
        location.href = '/';
    } else {
        //parse special char
        var entry = {"'": "&apos;", '"': '&quot;', '<': '&lt;', '>': '&gt;'};
        q = q.replace(/(['")-><&\\\/\.])/g, function ($0) {
            return entry[$0] || $0;
        });

        var string = '/query/solr?q=' + q;
        location.href = string;
    }
    ;

}
