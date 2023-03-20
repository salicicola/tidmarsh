<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
<xsl:output method="xml" indent="no" omit-xml-declaration="yes" />
<xsl:template name="translations">
   <div id="translations">
        <xsl:if test="not ($page='translations')"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
	<div style="float:right;margin-left:10px;">
		<img alt="" title=""  src="/static/slides/skvortsov.jpg" align="right" border="1" width="300"/>
	</div>
	<div class="header">
		<h2>Translations</h2>
	</div>
	<div class="items">	
		<xsl:for-each select="//translations/translation">
			<div class="item">
				<a href="http://172.104.19.75{@href}"><xsl:copy-of select="* | text()"/></a>
			</div>
		</xsl:for-each>
	</div>
</div>
</xsl:template>

</xsl:stylesheet>
