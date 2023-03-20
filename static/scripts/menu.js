var strPDate = "";
var siteLastUpdated = "27 January 2022"

var menuBarURL = new  Array (
	'/index.html',
	'/articles.html',
	'/translations.html',
	'/announcements.html',
	'/demos.html'
);

var menuBarTxt = new Array (
	'home',
	'articles &amp; notes',
	'translations',
	'announcements',
	'projects &amp; demos'
);

	var strMenu = '';
	var strCurrent = "javascript: void(0)"
	var strStyle = " style='text-decoration:none'";
// to avoid it

function MenuWrite () {
	for (var i = 0;  i < menuBarURL.length; i++) {
		if (location.href.indexOf (menuBarURL[i]) == -1) {
			strMenu += ' <b>[</b><a href=' + menuBarURL[i] + '>' +
				menuBarTxt[i] + '</a><b>]</b> ';
		}
		else {
			strMenu += ' [<a href="' + strCurrent + '" ' + strStyle + '")>' +
				menuBarTxt[i] + '</a>] ';
		};
	};
	document.writeln('<center>' + strMenu + '</center>');
};


function footerWrite () {
var str ='<table border="0" width="100%" style="margin-bottom: 0px; padding-bottom: 0px;">' +
	'<tbody><tr><td colspan="2"><hr /></td></tr><tr><td align="left">' +
	'<a style="text-decoration: none"  href="/"><b>Salicicola</b></a>' +
	'</td><td align="right">   Last updated:    ' +
	'<i>' + siteLastUpdated + '</script></i>' +
	'<br/><a style="text-decoration: none" ' +
	'href="mailto:webmaster@salicicola.com">webmaster</a>' +
	'</td></tr></tbody></table>   ';
document.writeln(str);
};


function headerWriteStart () {
var str = '<center>' +
 '<a href="/index.html"><img border="0" height="40" src="/salicicola.gif"' +
 ' alt="Salicicola Home" vspace="0" /></a><br clear="all" />' +
 '</center>';
 document.write(str);
};

function headerWriteEnd () {
 document.write ('<hr />');
}

function headerWriteImage(string) {
 headerWriteStart ();
 if (string.length>0) {
  document.write('<center><h2 style="margin-bottom:0"><i>' + string + '</i></h2></center>');
 }
 headerWriteEnd ();
}

function headerWriteText(string, isLink) {
	var str = '<table bgcolor="#8B0000" border="0" width="100%" cellspacing="0" style="background-color: #8B0000;">' +
            '<tbody valign="top" style="background-color: #8B0000;"><tr>' +
            '<td bgcolor="#8B0000" nowrap style="padding-top: 0px; height: 40px; margin-top: 0px; ' +
	    'vertical-align: middle; text-align:left; background-color: #8B0000; ' +
	    'font-size: 30pt; color: #F0FFF0;"><a href="/" style="color: white; ' +
	    'text-decoration: none;"><img border="0" height=40" alt="" src="/static/images/Salicicola__40.gif"></a></td>' +
	    '<td align="right" bgcolor="#8B0000" nowrap style="padding-top: 0px; height: 40px; margin-top: 0px; ' +
	    'vertical-align: middle; text-align:right; background-color: #8B0000; '+
	    'font-size: 30pt; color: #F0FFF0;"><img  border="0" src="/static/images/' +
	    string +
	    '__40.gif" height=40"></td></tr></tbody></table>';
   	    document.writeln(str);
	
	    /*
'<table border="0" width="100%" cellspacing="0" style="background-color: #8B0000;">' +
            '<tbody valign="top"><tr>' +
            '<td nowrap style="padding-top: 0px; height: 60px; margin-top: 0px; ' +
	    'vertical-align: middle; text-align:left; background-color: #8B0000;' +
	    'font-size: 30pt; color: #F0FFF0;"><a href="/" style="color: white; ' +
	    'text-decoration: none;"><span style="color: white; font-weight: bold; ' +
	    'vertical-align: top;"> &nbsp; &nbsp; &nbsp; Salicicola</span></a></td>' +
	    '<td nowrap style="padding-top: 0px; height: 60px; margin-top: 0px; ' +
	    'vertical-align: middle; text-align:right; background-color: #8B0000;' +
	    'font-size: 30pt; color: #F0FFF0;"><span style="font-size:30pt">' +
	    string +
	    '&nbsp; &nbsp; &nbsp; </span></td></tr></tbody></table>';


*/	
/*	
var str = '\n<center><h2 class="header" ><i><big>\n';
 if (isLink == true) { 
	str += '<a class="header" href="/index.html">Salicicola</a></big>\n'; 
	}
 else { 
	str += 'Salicicola</big>'; 
	}
 if (string.length>0) {
  str += '<br />' + string;
 }
 str += '</i></h2></center><hr />\n';
 document.writeln(str);
*/
};


function PDateWrite() {
	if (strPDate != '') {
var str = '<div><hr align="left" width="20%" >' +
'<i><span style="font-size:80%">' + 
 strPDate +
'</span></i></div>';
document.writeln(str);
	}
}


function PDateWriteI() {
var str = '<div><hr align="left" width="20%" >' +
'<span style="font-size:80%"><i>' + 
'I. Kadis' + '<br />' +
 strPDate +
'</i></span></div>';
document.writeln(str);
}

function PDateWriteStr(string) {
var str = '<div><hr align="left" width="20%" >' +
'<span style="font-size:80%"><i>' + string + '<br />' +
 strPDate +
'</i></span></div>';
document.writeln(str);
}


function projects_menu(string) {
var str = '' +
'      <center>' +
'         <table width="100%" border="0" cellspacing="0" cellpadding="0">' +
'            <tr>' +
'               <td align="center" nowrap colspan="2"><b><h2 class="header">Salicicola &#151; ' +
'Website For Salicologists and Symphytologists &#151; ' + string + '</h2></b></td>' +
'            </tr>' +
'            <tr>' +
'               <td align="center" nowrap colspan="2">';
document.writeln(str);
MenuWrite();
str = '<hr/>' + 
'	 </td>' +
'            </tr>' +
'         </table>' +
'     </center>';
document.writeln(str);
}


