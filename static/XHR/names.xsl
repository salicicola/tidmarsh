<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:param name="text" select="''"/>
	<xsl:template match="/">
			<xsl:for-each select="/*/*[contains(., $text)]">
				<option title="{authors}" value="{PNID}"><xsl:value-of select="latname"/></option>
			</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
