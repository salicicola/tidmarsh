<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />
	<xsl:template name="invasive">
	   <div id="invasive">
			<xsl:if test="not ($page='invasive')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
		<div style="float:right;margin-left:10px;">
			<img align="right" alt="kudzu vine (Pueraria lobata) in Needham" title="kudzu vine (Pueraria lobata) in Needham" width="300" border="1" onclick="openImage(this)" src="/static/photos/200909/20090916canon0833c.jpg"/><!-- FIXME $ -->
		</div>
		<div class="header">
			<h2>Invasive Plants at Salicicola</h2>
		</div>
		<div class="section">
			<div class="section_header"><a href="http://salicicola.com/plants/invasive">Introduction</a></div>
		</div>	
		<div class="section">
			<div class="section_header">Listing by County</div>
			<div class="item">
				[<a href="http://salicicola.com/plants/invasive/invasiveA.html">alphabetical</a>]
				[<a href="http://salicicola.com/plants/invasive/invasiveT.html">taxonomical</a>]
				[<a href="http://salicicola.com/plants/invasive/invasiveF.html">by habit</a>] 
			</div>
		</div>
		<div class="section">
			<div class="section_header">Species Notes</div>
			<xsl:for-each select="/*/invasive/species_notes/note">
				<div class="item"><a href="http://172.104.19.75{@href}"><xsl:copy-of select="* | text()"/></a></div>
			</xsl:for-each>
		</div>
		<div class="section">
			<div class="section_header">Reports</div>
			<div class="item">
			 <a href="#">Archived</a><!--: /archive/#archive_invasive_reports
			 <xsl:for-each select="/*/invasive/reports_archived/*">
			 	[<a href="/archive/#{@id}"><xsl:copy-of select="*|text()"/></a>]
			 </xsl:for-each>-->
		</div>
	</div>
</div>
</xsl:template>
</xsl:stylesheet>
