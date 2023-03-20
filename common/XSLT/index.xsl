<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0" xmlns:xs="http://www.w3.org/2001/XMLSchema">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" encoding="utf-8"/> 

	<xsl:variable name="color" select="'#8B0000'"/>
	<xsl:variable name="bgcolor" select="'#F0FFF0'"/>
	<xsl:variable name="updated" select="/*/@updated"/>
	<xsl:variable name="cal_year" select="/*/@year"/>
	<xsl:variable name="photos" select="/*/gallery/@photos"/>
	<xsl:variable name="species" select="/*/gallery/@plants"/>
	<xsl:variable name="reports" select="tokenize(/*/gallery/@reports, ' ')"/>
	<xsl:param name="page" select="'gallery'"/>

	<xsl:include href="index_style.xsl"/>
	<xsl:include href="index_checklists.xsl"/>
	<xsl:include href="index_invasive.xsl"/>
	<xsl:include href="index_quiz.xsl"/>
	<xsl:include href="index_que.xsl"/>
	<xsl:include href="index_events.xsl"/>
	<xsl:include href="index_events_current.xsl"/>
	<xsl:include href="index_translations.xsl"/>
	<xsl:include href="index_articles.xsl"/>
	<xsl:include href="index_stories.xsl"/>
	<xsl:include href="index_archive.xsl"/>
	<xsl:include href="index_other.xsl"/>
<xsl:include href="index_animals.xsl"/>
	<xsl:include href="index_slides.xsl"/>
	<xsl:include href="index_calendar.xsl"/>
	<xsl:include href="index_calendar_page.xsl"/>
	
	<xsl:template match="/">
	<html> 
	<head>	
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<title>Salicicola</title>
		<script type="text/javascript">
			var menu = {'gallery': 'Plant Gallery', 'checklists': 'Checklists', 'invasive': 'Invasive Plants', 'questions': 'Questions and Answers', 'quiz': 'Plant Quiz', 'events': 'Salicicola Past Events', 'translations': 'Translations', 'articles': 'Articles/Notes', 'stories':'Plant Stories', 'slides': 'Slide Shows', 'other': 'Animal Gallery', 'archive': 'Archive', 'calendar_page': 'Calendar'};
			var ids = ['gallery', 'checklists', 'invasive', 'questions', 'quiz', 'events', 'translations', 'articles', 'stories', 'slides', 'other', 'archive',  'calendar_page'];
			var active = '<xsl:value-of select="$page"/>';
			//alert('init embed, active= ' + active);
		</script>
		<script type="text/javascript" src="/static/scripts/index.js">
		// FIXME
		</script>
		<script type="text/javascript">
			<xsl:text disable-output-escaping="yes">
			<![CDATA[
			function switch_display(parent, name) {
				targets = parent.getElementsByTagName(name);
				for (i = 0; i < targets.length; i++) {
					target = targets[i];
					if (target.style.display == 'none') {
						target.style.display = 'block';
					}
					else {
						target.style.display = 'none';
					}
				};
			}
			]]>
			</xsl:text>	
		</script>
		<xsl:call-template name="style"/>
	</head>
<body>
<div id="wrapper">
	<div id="header">
		<img id="logo" src="/static/images/Salicicola_324_72.gif" alt="" height="72" width="324"/>
		<img id="bar" src="/static/photos/200611/20061111canon0260a.jpg" alt="" height="72"/>
	</div>
	<div id="sidebar"> 
		<h2 id="menu_gallery">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">gallery</xsl:with-param>
				<xsl:with-param name="long">Plant Gallery</xsl:with-param>
			</xsl:call-template>
		</h2>
		<h2 id="menu_checklists">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">checklists</xsl:with-param>
				<xsl:with-param name="long">Checklists</xsl:with-param>
			</xsl:call-template>
		</h2>
		<h2 id="menu_invasive">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">invasive</xsl:with-param>
				<xsl:with-param name="long">Invasive Plants</xsl:with-param>
			</xsl:call-template>
		</h2>
		<!--<h2 id="menu_questions">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">questions</xsl:with-param>
				<xsl:with-param name="long">Questions and Answers</xsl:with-param>
				<!- -<xsl:with-param name="url">http://fmssf.salicicola.com/questions</xsl:with-param>- ->
			</xsl:call-template>
		</h2>-->
		<h2 id="menu_quiz">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">quiz</xsl:with-param>
				<xsl:with-param name="long">Plant Quiz</xsl:with-param>
			</xsl:call-template>
		</h2>
<!--
		<h2 id="menu_events">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">events</xsl:with-param>
				<xsl:with-param name="long">Salicicola Past Events</xsl:with-param>
			</xsl:call-template>
		</h2> -->
		<h2 id="menu_translations">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">translations</xsl:with-param>
				<xsl:with-param name="long">Translations</xsl:with-param>
			</xsl:call-template>
		</h2>
		<h2 id="menu_articles">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">articles</xsl:with-param>
				<xsl:with-param name="long">Articles/Notes</xsl:with-param>
			</xsl:call-template>
		</h2>
		<h2 id="menu_stories">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">stories</xsl:with-param>
				<xsl:with-param name="long">Plant Stories</xsl:with-param>
			</xsl:call-template>
		</h2>
		<h2 id="menu_slides">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">slides</xsl:with-param>
				<xsl:with-param name="long">Slide Shows</xsl:with-param>
			</xsl:call-template>
		</h2>

		<h2 id="menu_other">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">other</xsl:with-param>
				<xsl:with-param name="long">Animal Gallery</xsl:with-param>
			</xsl:call-template>
		</h2>
		<h2 id="menu_archive">
			<xsl:call-template name="select_menu">
				<xsl:with-param name="short">archive</xsl:with-param>
				<xsl:with-param name="long">Archive</xsl:with-param>
				<!--<xsl:with-param name="url">/archive/</xsl:with-param>-->
			</xsl:call-template>
		</h2>
	</div>
	<div id="content">
		<xsl:call-template name="gallery"/>
		<xsl:call-template name="checklists"/>
		<xsl:call-template name="invasive"/>
		<xsl:call-template name="questions"/>
		<!--<xsl:call-template name="questions"/> -->
		<!-- not in use (for now), but needed by scripts -->
		<xsl:call-template name="quiz"/>
		<xsl:call-template name="events"/>
		<xsl:call-template name="translations"/>
		<xsl:call-template name="articles"/>
		<xsl:call-template name="stories"/>
		<xsl:call-template name="slides"/>
		<xsl:call-template name="other"/> <!-- archive -->
<xsl:call-template name="archive"/>
		<!--		<xsl:call-template name="calendar_page"/> -->
	
	</div>
</div>
	<div id="footer">
		<hr/>
		<div style="float:left;"> <br/>
<!--  background-color:yellow Migrating from Java/XSLT to Python/Django (beta)-->
<!--		 
		<a href="/news/rss.xml" title="Subscribe to Salicicola News">RSS feeds</a>
		  -  
		<a href="/sitemap.html" title="site map (HTML)">site map (HTML)</a>
-->
		</div>
		<div style="float:right;">
			Last updated: <i><xsl:value-of select="$updated"/></i>
		</div>
	</div>
</body>
</html>
</xsl:template>

<xsl:template name="questions_with_url"> <!-- former version of questions -->
   <div id="questions">
        <xsl:if test="not ($page='questions')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div style="float:right;margin-left:10px;">
		<!-- img-->
	</div>
	<div style="margin-left:1em;margin-right:5px">
		Stub (not needed now)
		<div style="padding-left:2ex">
		   <br/>
		</div>
	</div>	
   </div>
</xsl:template>


<xsl:template name="gallery">
    <div id="gallery">
        <xsl:if test="not ($page='gallery')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div style="float:right;margin-left:10px;margin-top:0;padding-top:0;background-color:transparent">

<xsl:variable name="current_month" select="format-date(current-date(), '[MNn]')"/>
<xsl:variable name="current_image">
    <xsl:choose>
    <xsl:when test="$current_month = 'May'">poison ivy (Toxicodendron radicans)</xsl:when>
	<xsl:when test="$current_month = 'June'">grass-pink (Calopogon tuberosus)</xsl:when>
	<xsl:when test="$current_month = 'July'">waterschield (Brasenia schreberi)</xsl:when>
	<xsl:when test="$current_month = 'August'">catberry (Nemopanthus mucronatus = Ilex mucronata)</xsl:when>
<xsl:when test="$current_month = 'September'">New York ironweed (Vernonia noveboracensis)</xsl:when>
<xsl:when test="$current_month = 'October'">Round-fruited seedbox (Ludwigia sphaerocarpa)</xsl:when>
<xsl:when test="$current_month = 'November'"></xsl:when>
<xsl:when test="$current_month = 'December'"></xsl:when>
<xsl:when test="$current_month = 'January'">Wintergreen (Gaultheria  procumbens)</xsl:when>
<xsl:when test="$current_month = 'February'"></xsl:when>
<xsl:when test="$current_month = 'March'"></xsl:when>
<xsl:when test="$current_month = 'April'"></xsl:when>
        <xsl:otherwise/>
    </xsl:choose>
</xsl:variable>
	<img src="/static/images/{$current_month}.jpg" width="300" title="{$current_image}" style="margin-top:0;padding-top:0;width:300px;overflow:hidden;margin-bottom:2ex;"/><!-- 300 * 350 or more XXX margin-bottom:2ex; height:300px;-->
<xsl:call-template name="make_calendar"/>
	<div style="text-align:center"><br/>   

</div>   


	</div>
	<div style="margin-left:1em;margin-right:5px">
		<a style="font-weight:bold" href="/photodb/vascular/gallery"><!--Eastern -->Massachusetts Vascular Plants</a>
		<div style="padding-left:2ex">
			<a id="replaceIT" href="/photodb/vascular/gallery">Contains a total of
			<xsl:value-of select="$photos"/> medium-sized images of 
			<xsl:value-of select="$species"/>
			taxa (<xsl:value-of select="/*/gallery/@flora"/> from the flora of Massachusetts).
			</a> <!--<b style="color:red"> to cache </b>-->
		</div>
	</div>



	<div style="margin-left:1em;padding-right:5px;padding-top:2ex">
		<a style="font-weight:bold">Salicicola Search Engine</a>
		<div style="padding-left:2ex">
			<a href="/photodb/search/">Search 
			for scientific or common names, towns, <!-- communities,--> 
			reservations, certain months, invasive plants, etc.</a>
		</div>
	</div>

<div style="margin-left:1em;padding-right:5px;padding-top:2ex">
		<a style="font-weight:bold">Vegetation Types</a>
		<div style="padding-left:2ex">
			<a href="http://salicicola.com/plantgallery/vegetation/">Most common vegetation types of eastern Massachusetts</a>
		</div>
	</div>

		<div style="margin-left:1em;padding-right:5px;padding-top:2ex" title="published: {/*/nonvasular/@updated}">
		<a style="font-weight:bold" href="http://salicicola.com/plants/nonvascular/">Non-Vascular Plants and Lichens</a>
		<div style="padding-left:2ex">
			<!-- XXX <xsl:value-of select="/*/nonvasular/@plants"/> species:-->
			[<a href="/photodb/nonvascular/">standard view</a>] 
			[<a href="/photodb/nonvascular/mobile/">mobile</a>]
			<!--
			/servlet/SaxonServlet?source=/XML/taxa.xml&amp;style=/XML/plants_indexWNewNonVas.xsl&amp;clear-stylesheet-cache=yes
			/servlet/SaxonServlet?source=/XML/taxa.xml&amp;style=/XML/non_vascular_mobile.xsl&amp;clear-stylesheet-cache=yes
			-->
		</div>
	</div>


<div style="margin-left:1em;padding-right:5px;padding-top:2ex">	
	<a style="font-weight:bold" href="http://salicicola.com/reviews/northeast_seed_mix_review.html">Northeast Pollinator Wildflower Seed Mix Analysis</a>
</div>

	<div style="margin-left:1em;padding-right:5px;padding-top:2ex">	
		<a style="font-weight:bold" href="/photodb/vascular/news/">What's New in the Gallery</a>
		<div style="padding-left:2ex"> 
			<a href="/photodb/vascular/news/">Recent additions to the gallery</a>
		</div>
	</div>
	<div style="margin-left:1em;padding-right:5px;padding-top:2ex">	
		<a style="font-weight:bold" href="/photodb/vascular/latnames/">Index of Latin Names</a>
	</div>
	<div style="margin-left:1em;padding-right:5px;padding-top:1ex">	
		<a style="font-weight:bold" href="/photodb/vascular/comnames/">Index of Common Names</a>	
	</div>
   </div>
</xsl:template>

<xsl:template name="select_menu">
	<xsl:param name="short" select="''"/>
	<xsl:param name="long" select="''"/>
	<xsl:param name="url" select="concat('/', $short, '/')"/>
	<xsl:choose>
	<xsl:when test="$page=$short">
		<xsl:attribute name="style">background-color:white</xsl:attribute>
		<xsl:value-of select="$long"/>
	</xsl:when>
	<xsl:otherwise>
		<xsl:attribute name="style">cursor:pointer</xsl:attribute>
		<xsl:attribute name="onmouseover">this.style.color='red'</xsl:attribute>
		<xsl:attribute name="onmouseout">this.style.color='<xsl:value-of select="$color"/>'</xsl:attribute>
		<xsl:choose>
			<xsl:when test="contains($url, 'http')">
				<a href="{$url}"><xsl:value-of select="$long"/></a>
			</xsl:when>
			<xsl:otherwise><!---->
				<a href="{$url}" onmousedown="fill_contents('{$short}')" onclick="fill_contents('{$short}');return false"><xsl:value-of select="$long"/></a>
			</xsl:otherwise>	
		</xsl:choose>
	</xsl:otherwise>
	</xsl:choose>
</xsl:template>

</xsl:stylesheet>
