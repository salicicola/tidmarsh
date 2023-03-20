
var w = null;
var calendar_url = "/servlet/SaxonServletX?source=/calendar/stub.xml&style=/calendar_adv.xsl&clear-stylesheet-cache=yes"
var calendar_url = "/calendar/"
function open_calendar() {
	w=open(calendar_url, 'calendar', 'width=690,height=950,top=50,left=50,resizable=yes,scrollbars=yes');
	w.focus();
}

function fill_contents(page) {
//alert('calling for ' + page + ' active ' + active);
	for (i=0; i < ids.length; i++) {
	   try {
		idv = "menu_" + ids[i]; // no menu calendar
		document.getElementById(idv).style.backgroundColor = '#F0FFF0';
			document.getElementById(ids[i]).style.display = 'none';
		}
		catch (e) {
//			alert(e); // is null;
		}
	} // FIXME
	try {
		amenu = document.getElementById('menu_' + active);
//	alert(amenu);
		atext = amenu.innerHTML;
//	alert(atext);
		amenu.innerHTML = '';
		alink = document.createElement('a');
		alink.setAttribute('href', '/' + active + '/');
		alink.setAttribute('onmousedown', "fill_contents('" + active + "')");
		alink.setAttribute('onclick', "fill_contents('" + active + "'); return false");
		alink.appendChild(document.createTextNode(atext));
		amenu.appendChild(alink);

		document.getElementById(page).style.display='block';
//	alert(document.getElementById(page).innerHTML);
		trg = document.getElementById('menu_' + page);
		trg.removeAttribute('style');
		trg.style.backgroundColor = 'white';
		trg.innerHTML = '';
		trg.appendChild(document.createTextNode(menu[page]));
		active = page;
//alert('reach here');
	}
	catch (e) {
		//alert(e); //trg r amenu is null with calendar usage// XXX display is not null !!
		document.getElementById('calendar_page').style.display = 'none';
		active = page;
		document.getElementById(page).style.display='block';
	}
}

