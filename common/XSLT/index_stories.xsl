<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
	<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />

<xsl:template name="stories">
   <div id="stories">
        <xsl:if test="not ($page='stories')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div style="float:right;margin-left:10px;">
		<img alt="" title="" onclick="openImage(this)" 
			src="/static/photos/201405/20140518ricoh1232a.jpg" align="right" border="1" width="300"/>
	</div>

	<div class="header">
		<h2>Salicicola-Lore</h2>
	</div>
			
	<div class="items">	
		<xsl:for-each select="//notes/note[position() &gt; 2]">
			<div class="item" style="margin-bottom:2ex">
				<a href="{@href}"><xsl:copy-of select="*|text()"/></a>
			</div>
		</xsl:for-each>
         </div>
    </div>
</xsl:template>

</xsl:stylesheet>

