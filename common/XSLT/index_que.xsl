<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />

<xsl:template name="questions">
   <div id="questions">
        <xsl:if test="not ($page='archive')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div class="header">
		<h2><a href="/questions/view/">Questions and Answers</a></h2>
	</div>
        <div class="section">

[<a style="color:red;font-weight:bold" href="/questions/entry/">Post New Question</a>] &#160;
[<a style="color:red;font-weight:bold" href="/questions/view/">View Recent Questions</a>]
<br/>

        	<div class="section_header" style="font-weight:normal;margin-bottom:3px;">   	
        	This web service provides help with identification of plants found in the wild, mostly in eastern Massachusetts, 
        	though occasionally questions come from elsewhere in the world (see map). 
        	It may also be used as a tool for reporting plants (such as invasive or rare). 
        	Cultivated plants are not discussed here.
 <!-- <br/>
      	
[<a style="color:darkred;font-weight:bold" href="/questions/entry/">Post New Question</a>] &#160;
[<a style="color:darkred;font-weight:bold" href="/questions/view/">View Recent Questions</a>]-->

  		<!--	This web service was created to help with plant identification in eastern Massachusetts. 
  			Initially it was intended for the Friends of Myles Standish State Forest 
  			(a state park in Plymouth County, Massachusetts), 
  			yet we have been responding to questions from all over the world. 
  			The service may also work as a tool for 
  			<a style="text-decoration:underline" href="http://fmssf.salicicola.com/mobile/plants/entry?category=a">reporting plants</a> 
  			(report the known plants), for example, invasive or rare ones.  
  			The page is accessible from Salicicola 
  			<a style="text-decoration:underline" href="http://fmssf.salicicola.com/questions">Questions &amp; Answers</a> 
  			page and from the <a href="http://www.friendsmssf.com/pinebarrensplantid.html">Friends of Myles Standish SF website</a>.
-->
        	
        	
<!--			This web service 
			has been created to help with plants ID from Eastern Massachusetts
			(initially intended specifically for Friends of Myles Standish State Forest),
			but actually we are getting requests from all over the the world.
			It may also serve as a tool to 
			<a style="text-decoration:underline" 
				href="http://fmssf.salicicola.com/mobile/plants/entry?category=a">report the known plants</a>, 
			invasive or rare ones
			which is accesible from the main 
			<a style="text-decoration:underline" 
				href="http://fmssf.salicicola.com/questions">Questions &amp; Answers page</a>
			or from the <a href="http://www.friendsmssf.com/pinebarrensplantid.html">Friends 
			of Myles Standish SF website</a>.-->
        	</div>
        	<img src="/static/images/mssf_friends_globe.jpg" /><!-- width="652" height="300" -->
        	<br clear="all"/>
		<!--	<div style="font-size:90%"> ... -->
        		<!--Note. This map,-->
        		<!--Salicicola Help with Plant ID Service on the Massachusetts Map-->
        		<!--exists in two flavors, [1] &amp; [2], -->
        		<!-- [-was-] -->
        		<!--was last updated in February 2016.-->
      	

        		<!--
        		<b>Note</b>: this map, existed in two flavors,
        		[<a href="http://azinoviev.maps.arcgis.com/apps/Viewer/index.html?appid=71c58092c9fb4dbc98592798be591158">1</a>]
        		&amp;
        		[<a href="http://azinoviev.maps.arcgis.com/apps/Viewer/index.html?appid=628aea4b55594147b0f574a273a5672c">2</a>],
        		has not been updated since February 2016.
        		-->
		<!--</div> -->
        </div>
</div>
</xsl:template>

</xsl:stylesheet>

<!--
http://azinoviev.maps.arcgis.com/apps/Viewer/index.html?appid=71c58092c9fb4dbc98592798be591158
http://azinoviev.maps.arcgis.com/apps/Viewer/index.html?appid=628aea4b55594147b0f574a273a5672c
Feb 17 2016
http://azinoviev.maps.arcgis.com/apps/Viewer/index.html?appid=71c58092c9fb4dbc98592798be591158
https://www.arcgis.com/home/item.html?id=628aea4b55594147b0f574a273a5672c
https://www.google.com/search?q=Friends+of+MSSF+on+the+MA+Map&gws_rd=ssl#q=Friends+of+MSSF+on+the+Map
http://azinoviev.maps.arcgis.com/apps/Viewer/index.html?appid=628aea4b55594147b0f574a273a5672c

-->
