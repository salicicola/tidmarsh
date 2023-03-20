<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />

<xsl:template name="archive">
   <div id="archive">
        <xsl:if test="not ($page='archive')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div class="header">
		<h2>Archive</h2>
	</div>
          <div class="section">
        	<div class="section_header">Memorable Dates</div>
 		<div class="item_compact">
 			<b>Alexey K. Skvortsov</b><br/>
			<!-- subitem-->			&#8226;  <a href="/announcements/Skvortsov_obituary.html">Obituary</a> (9 February 1920&#8212;8 May 2008)<br/>
<!-- subitem-->			&#8226;  <a href="/biblio/Skvortsov.html">List of publications (1947&#8212;2005)</a><br/>
			<!--&#8226;  <a href="/announcements/skvortsov90/">The 90th Anniversary (9 February 2010) &#8212; slideshow</a>-->
                </div>
 		<div class="item_compact">
			<a href="/announcements/Linnaeus300.html"><b>Carl Linnaeus</b> 300th anniversary (May 2007)</a>
                </div>
		<div class="item_compact">
			<b>A. N. Zhelochovtsev</b><br/>
<!-- subitem-->			&#8226; <a href="/announcements/zhelochovtsev100.html">Centennial anniversary (1903-2003)</a> (Sep 22, 2004)<br/>
<!-- subitem-->			&#8226; <a href="/announcements/zhelochovtsev_bibl.html">List of publications</a><br/>
<!-- subitem-->			&#8226; <a href="/announcements/zhelochovtsev_bibl.html">List of sawflies</a> described by A.N. Zhelochovtsev (1903-1976)
                </div>
       </div>
       <xsl:for-each select="//archive/section">
           <div class="section">
        	<div class="section_header"><xsl:value-of select="@title | @name"/></div>
        	<xsl:for-each select="*">
		<div  class="item_compact">
			<a href="{@href}"><xsl:value-of select="@title|@name"/>
				<xsl:choose>
					<xsl:when test="extra"></xsl:when>
					<xsl:otherwise>
						<xsl:copy-of select="*|text()"/>
					</xsl:otherwise>
				</xsl:choose>
			</a>
			<xsl:if test="@authors or @year">
			<xsl:text> </xsl:text>
			<i class="nowrap"><xsl:value-of select="@authors"/><xsl:text> </xsl:text><xsl:value-of select="@year"/></i>
			</xsl:if>
			<!--<xsl:message>btween if <xsl:copy-of select="."/></xsl:message>-->
			<xsl:if test="extra">
			<xsl:message>inside if</xsl:message>
				<xsl:text> </xsl:text>
				<a href="{extra/@href}"><xsl:copy-of select="extra/* | extra/text()"/></a>
			</xsl:if>
                </div>
        	</xsl:for-each>
           </div>
       </xsl:for-each>
      <div class="section" id="archive_invasive_reports">
		<div class="section_header">Invasive Plants. Reports</div>
		<xsl:for-each select="//archive/reports/report">
			<div class="item_compact" id="{@id}"><a href="{@href}"><xsl:copy-of select="*|text()"/></a></div>
		</xsl:for-each>
     </div>
</div>
</xsl:template>
</xsl:stylesheet>
