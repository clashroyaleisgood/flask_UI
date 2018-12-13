//------ old methods --------
function json_ajax(url, json) {
    var request = $.ajax({
        url: url,
        type: "POST",
        data: JSON.stringify(json),
        dataType: "json",
        //async: false,
        contentType: "application/json; charset=utf-8"/*,
        success: function (data, status) {
            obj= {hello:data.hello, city:data.city};
            console.log("obj:", obj);

            //$("div").html(data.hello + "<br>" + data.city);
            //$.each(data, function(i, field){
            //$("div").append(i+": "+field + "<br>");
            //});
        }*/
    });
    return request;
}
//----------------- yes! this worked -----------
var alertError = function(jqXHR, textStatus, errorThrown) {
	alert('status: ' + jqXHR.status+'\nerrorThrown: ' + errorThrown)
	//console.log('1: ', jqXHR);
	//console.log('2: ', textStatus);
	//console.log('3: ', errorThrown);
}
//---------------------- 呀呼!!! -----------------------------
jQuery.fn.extend({
	post_ajax: function (url, json, callback) {
		/*console.log('url:', url);
		console.log('json:', json);
		console.log('callback:', callback);*/
		$.ajax({
			url: url,
			type: "POST",
			data: JSON.stringify(json),
			dataType: "json",
			contentType: "application/json; charset=utf-8",
			success: callback,
			error: alertError
		})
	}
});
//-------------------- line 6718  jQuery.load() ---------------
//-------------------- 成功 -----------------------------------
jQuery.fn.extend({
    load_ajax: function (url, json) {
		var self = this;
        $.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify(json),
            dataType: "html",
            contentType: "application/json; charset=utf-8",
            success: function (data) {
                //console.log("data:", data);
                $(self).html(data);
			},
			error: alertError
        });
    }
});

jQuery.fn.extend({
    zigzag: function () {
        var text = $(this).text();
        var zigzagText = '';
        var toggle = true; //lower/uppper toggle
			$.each(text, function(i, nome) {
				zigzagText += (toggle) ? nome.toUpperCase() : nome.toLowerCase();
				toggle = (toggle) ? false : true;
			});
	return zigzagText;
    }
});
/*
jQuery.fn.extend({
	load: function( url, params, callback ) {
		if ( typeof url !== "string" && _load ) {
			return _load.apply( this, arguments );

		// Don't do a request if no elements are being requested
		} else if ( !this.length ) {
			return this;
		}

		var off = url.indexOf( " " );
		if ( off >= 0 ) {
			var selector = url.slice( off, url.length );
			url = url.slice( 0, off );
		}

		// Default to a GET request
		var type = "GET";

		// If the second parameter was provided
		if ( params ) {
			// If it's a function
			if ( jQuery.isFunction( params ) ) {
				// We assume that it's the callback
				callback = params;
				params = undefined;

			// Otherwise, build a param string
			} else if ( typeof params === "object" ) {
				params = jQuery.param( params, jQuery.ajaxSettings.traditional );
				//為啥不這樣做勒??
				//params = JSON.stringify(params);
				type = "POST";
			}
		}

		var self = this;

		// Request the remote document
		jQuery.ajax({
			url: url,
			type: type,
			dataType: "html",
			data: params,
            // 我加的 >> contentType: "application/json; charset=utf-8",
			// Complete callback (responseText is used internally)
			complete: function( jqXHR, status, responseText ) {
				// Store the response as specified by the jqXHR object
				responseText = jqXHR.responseText;
				// If successful, inject the HTML into all the matched elements
				if ( jqXHR.isResolved() ) {
					// #4825: Get the actual response in case
					// a dataFilter is present in ajaxSettings
					jqXHR.done(function( r ) {
						responseText = r;
					});
					// See if a selector was specified
					self.html( selector ?
						// Create a dummy div to hold the results
						jQuery("<div>")
							// inject the contents of the document in, removing the scripts
							// to avoid any 'Permission Denied' errors in IE
							.append(responseText.replace(rscript, ""))

							// Locate the specified elements
							.find(selector) :

						// If not, just inject the full result
						responseText );
				}

				if ( callback ) {
					self.each( callback, [ responseText, status, jqXHR ] );
				}
			}
		});

		return this;
    },
});
*/

function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds) {
            break;
        }
    }
}