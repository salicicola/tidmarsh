<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />

<xsl:template name="slides">
   <div id="slides">
        <xsl:if test="not ($page='slides')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div style="float:right;margin-left:10px;">
		<img align="right" alt="" title="" width="300" border="1" src="/static/photos/200808/20080802canon0151cs.jpg"/>
		<br clear="all"/>
		<img align="right" alt="" title="" width="300" border="1" src="/static/photos/200808/20080803canon0381cs.jpg" style="margin-top:5px"/>
	</div>
	<div class="header">
		<h2>Slide Shows</h2>
	</div>
	<div class="items">
		<xsl:for-each select="//slides/slide">
			<div class="item">
				<xsl:choose>
					<xsl:when test="@href">
						<a href="{@href}"><xsl:copy-of select="* | text()"/></a>
					</xsl:when>
					<xsl:otherwise>
						<xsl:copy-of select="* | text()"/>
					</xsl:otherwise>
				</xsl:choose>
			</div>
		</xsl:for-each>
        </div>    
 </div>
</xsl:template>

</xsl:stylesheet>
